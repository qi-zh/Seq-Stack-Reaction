#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 20:52:41 2022

@author: qizhang
"""
from .load_reactor import load_reactor
from .qspr import QSPR_model, QSPR_model_rdkit
import pandas as pd
import numpy as np
import pickle
import torch
import os
import time
import math
import pathlib


class Forward_model:
    def __init__(self, variables):
        self._variables = variables
        self._prefix = ""
        # self._id = reactor_id
        self._reactor = load_reactor(
            max_length=variables["product_len"],
            model_path=variables["reactor_model_path"],
            device_id=variables["reactor_gpu_id"],
        )
        self._estimator = QSPR_model_rdkit(variables=variables)
        self._gtm_model = pickle.load(open(variables["gtm_path"], "rb"))
        self._pool = None
        self._gpu_path = (
            self._variables["warehouse"] + "/" + self._variables["reactor_id"]
        )
        self._pool_max_size = 0

    def pick_generation(self):
        load = False
        while not load:
            try:
                generation_list = [
                    _
                    for _ in os.listdir(self._gpu_path)
                    if len(_) > 4 and _[-3:] == "csv"
                ]
                if len(generation_list) > 0:
                    generation = generation_list[0]
                    X_path = self._gpu_path + "/" + generation
                    X = pd.read_csv(X_path)
                    os.remove(X_path)
                    t = generation.split(".")[0]
                    load = True
            except:
                print("reactor pick warehouse error.")
            time.sleep(self._variables["refresh_rate"])

        return X, t

    def load_pool(self):
        pool_size = -1
        while pool_size < self._pool_max_size:
            try:
                self._pool = pd.read_csv(
                    self._variables["pool_updated_path"],
                    dtype={"map_x": int, "map_y": int, "generation": int},
                )
                pool_size = self._pool.shape[0]
            except:
                print("reactor: load pool again.")
            time.sleep(self._variables["refresh_rate"])
        self._pool_max_size = pool_size

    def load_smiles(self, X):
        _reactant_index = np.array(
            [[int(_) for _ in rid[1:-1].split(",")] for rid in X["reactant_index"]]
        )
        for i in range(self._variables["n_r"]):
            X["r" + str(i + 1) + "_id"] = _reactant_index[:, i]
            X["r" + str(i + 1)] = [
                self._pool.loc[rid]["SMILES"] for rid in X["r" + str(i + 1) + "_id"]
            ]
            X["r" + str(i + 1) + "_gen"] = [
                self._pool.loc[rid]["generation"] for rid in X["r" + str(i + 1) + "_id"]
            ]
        return X

    def unique(self, x):
        def count_freq(k):
            return x.loc[x[self._variables["unique_col"]] == k].shape[0]

        x_uni = x.drop_duplicates(subset=self._variables["unique_col"]).reset_index(
            drop=True
        )
        x_uni["freq"] = [*map(count_freq, x_uni[self._variables["unique_col"]])]
        return x_uni

    def react(self, x):
        for i in range(self._variables["n_r"] - 1):
            if i == 0:
                reactant_list = [
                    ".".join(R[0])
                    for R in zip(x[["r" + str(i + 1), "r" + str(i + 2)]].values)
                ]
            else:
                reactant_list = [
                    ".".join(R[0])
                    for R in zip(x[["p" + str(i), "r" + str(i + 2)]].values)
                ]

            x["p" + str(i + 1)] = self._reactor.react(reactant_list)
            torch.cuda.empty_cache()
        x["product"] = x["p" + str(self._variables["n_r"] - 1)]
        return x

    def compute_likelihood(self, X):
        X[self._prefix + "target"] = 1
        query_condition = " and ".join(
            [
                str(self._variables["target_region"][y][0])
                + " < "
                + self._prefix
                + y
                + " < "
                + str(self._variables["target_region"][y][1])
                for y in self._variables["y_list"]
            ]
        )
        X.at[X.query(query_condition).index, self._prefix + "target"] = 0
        ll = X.apply(
            lambda row: math.exp(
                self._variables["target_temperature"] * row[self._prefix + "target"]
                + self._variables["generation_temperature"]
                * sum(
                    [
                        row["r" + str(i + 1) + "_gen"]
                        for i in range(self._variables["n_r"])
                    ]
                )
            ),
            axis=1,
        )
        ll_sum = sum(ll)
        X[self._prefix + "ll"] = [l / ll_sum for l in ll]
        return X

    def save_new_number(self, t, n_new):
        df_path = self._variables["model_df_path"] + str(t)
        pathlib.Path(df_path).mkdir(parents=True, exist_ok=True)
        with open(df_path + "/n_new.txt", "w") as f:
            f.write(str(n_new))

    def save_df(self, X, t):
        if not self._variables["surrogate"]:
            df_path = self._variables["model_df_path"] + str(t)
            pathlib.Path(df_path).mkdir(parents=True, exist_ok=True)
            X.to_csv(df_path + "/df.csv", index=False)

    def pool_enrichment(self, X, X_fp, t):

        done = False
        while not done:
            try:
                self.load_pool()
                pool_addition = pd.DataFrame()
                pool_addition["SMILES"] = X["product"]
                pool_addition_fp = X_fp.loc[pool_addition.index]
                pool_addition["parents"] = [
                    tuple([int(_) for _ in rid[1:-1].split(",")])
                    for rid in X.loc[pool_addition.index]["reactant_index"]
                ]
                pool_addition_mapping = self._gtm_model.transform(pool_addition_fp)
                pool_addition["map_x"] = [
                    round(a[0] * 10) for a in pool_addition_mapping
                ]
                pool_addition["map_y"] = [
                    round(a[1] * 10) for a in pool_addition_mapping
                ]
                pool_addition["generation"] = [
                    sum(
                        [
                            self._pool.loc[parent_id]["generation"]
                            for parent_id in parents
                        ]
                    )
                    for parents in pool_addition["parents"]
                ]
                pool_addition.to_csv(
                    self._variables["pool_folder"] + "/addition/" + str(t) + ".csv",
                    index=False,
                )

                done = True
            except:
                print("reactor update pool error.")
            time.sleep(self._variables["refresh_rate"])

    def single_step(self):
        pool_loaded = False
        X, t = self.pick_generation()
        while not pool_loaded:
            try:
                self.load_pool()
                X = self.load_smiles(X)
                pool_loaded = True
            except:
                time.sleep(self._variables["refresh_rate"])
        X = self.unique(X)
        X = self.react(X)
        X, X_fp = self._estimator.predict(X)
        X = self.compute_likelihood(X)
        self.save_df(X, t)
        self.pool_enrichment(X, X_fp, t)

        X_target = X.loc[X[self._prefix + "target"] == 0]
        X_target_new = X_target.loc[X_target["is_new"]]
        n_target = len(set(X_target["product"]))
        n_target_new = len(set(X_target_new["product"]))
        self.save_new_number(t, n_target_new)
        print(
            "SMC: Step {}, target {}, new target {}, max rgen {}".format(
                t, n_target, n_target_new, X["r1_gen"].max()
            )
        )

    def __call__(self):
        count = 0
        while True:
            print("Work number: {}".format(count))
            self.single_step()
            count += 1
