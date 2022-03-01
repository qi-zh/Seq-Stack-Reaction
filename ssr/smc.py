import math
import os
import time
import pickle
import random
import numpy as np
import pandas as pd
import pathlib
from .qspr import QSPR_model, QSPR_model_rdkit



class SMC:
    def __init__(self, variables, pool, reactor=None):

        self._variables = variables
        self._reactor = reactor
        if variables["SMC_enrich"]:
            self._gtm_model = pickle.load(open(variables["gtm_path"], "rb"))
        self._pool = pool
        if variables["surrogate"]:
            self._prefix = "surrogate_"
            self._estimator = QSPR_model(variables=variables)
        else:
            self._prefix = ""
            self._estimator = QSPR_model_rdkit(variables=variables)
        self._black_list = set()

    def update_pool(self):
        if self._variables["reactor_enrich"]:
            addition_list = [
                _
                for _ in os.listdir(self._variables["pool_folder"] + "/addition")
                if len(_) > 4 and _[-3:] == "csv"
            ]
            if len(addition_list) > 0:
                pool_addition = pd.concat(
                    [
                        pd.read_csv(
                            self._variables["pool_folder"] + "/addition/" + addition,
                            dtype={"map_x": int, "map_y": int, "generation": int},
                        )
                        for addition in addition_list
                    ],
                    ignore_index=True,
                )
                pool_addition = pool_addition[
                    ~pool_addition.SMILES.isin(self._pool["SMILES"])
                ]
                pool_addition["parents"] = [
                    tuple([int(_) for _ in rid[1:-1].split(",")])
                    for rid in pool_addition["parents"]
                ]
                self._pool = pd.concat([self._pool, pool_addition], ignore_index=True)
                self._pool.to_csv(self._variables["pool_updated_path"], index=False)
                print("SMC: pool updated: {}".format(self._pool.shape[0]))
            else:
                print("SMC: pool is up to date.")

    def random_initialize(self):
        random_index_list = random.choices(
            self._pool.loc[
                self._pool["generation"] <= self._variables["generation_threshold"]
            ].index.to_list(),
            k=self._variables["n"] * self._variables["n_r"],
        )
        random_index_sets = np.array(random_index_list).reshape(
            (self._variables["n"], self._variables["n_r"])
        )
        X = pd.DataFrame(columns=self._variables["sample_column"])
        X["reactant_index"] = [tuple(_) for _ in random_index_sets]
        return X

    def in_black(self, X):
        def if_new(R_index):
            if R_index in self._black_list:
                return False
            return True

        X["is_new"] = X["reactant_index"].apply(if_new)
        self._black_list = self._black_list.union(set(X["reactant_index"]))
        return X

    def load_smiles(self, X):
        _reactant_index = np.array([list(_) for _ in X["reactant_index"]])
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

    def react(self, X):
        if self._variables["SMC_reactor"]:
            X = self._reactor.react(X)
        return X

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
        if not self._variables["surrogate"]:
            df_path = self._variables["model_df_path"] + str(t)
            pathlib.Path(df_path).mkdir(parents=True, exist_ok=True)
            with open(df_path + "/n_new.txt", "w") as f:
                f.write(str(n_new))

    def save_df(self, X, t):
        if not self._variables["surrogate"]:
            df_path = self._variables["model_df_path"] + str(t)
            pathlib.Path(df_path).mkdir(parents=True, exist_ok=True)
            X.to_csv(df_path + "/df.csv", index=False)

    def save_time(self, t, time_cost):
        df_path = self._variables["model_df_path"] + str(t)
        pathlib.Path(df_path).mkdir(parents=True, exist_ok=True)
        with open(df_path + "/time.txt", "w") as f:
            f.write(str(time_cost))

    def resample(self, X):
        if self._variables["optimization"]:
            X_resample = X.sample(
                n=self._variables["n"], replace=True, weights=X[self._prefix + "ll"]
            ).reset_index(drop=True)
            return X_resample
        return X

    def proposal(self, X_resample):
        def single_proposal(row):
            if row["is_new"] and row[self._prefix + "target"] == 0:
                exploit = True
            else:
                exploit = False
            if exploit:
                R_index = list(row["reactant_index"])
                r_i = random.choice(list(range(self._variables["n_r"])))
                r_index = R_index[r_i]
                assert (
                    r_index in self._pool.index
                ), "proposal: reactant pool does not contains target reactant: {} in {}".format(
                    r_index, self._pool.shape[0]
                )
                r_map_x = self._pool.loc[r_index]["map_x"]
                r_map_y = self._pool.loc[r_index]["map_y"]
                generation_threshold = self._variables["generation_threshold"]
                sim_col = self._pool.query(
                    "map_x == @r_map_x & map_y == @r_map_y & generation <= @generation_threshold"
                )
                if sim_col.shape[0] > 1:
                    sim_index = sim_col.index.to_list()
                else:
                    sim_index = self._pool.loc[
                        self._pool["generation"]
                        <= self._variables["generation_threshold"]
                    ].index.to_list()
                r_new = random.choice(sim_index)
                R_index[r_i] = r_new
            else:
                R_index = random.choices(
                    self._pool.loc[
                        self._pool["generation"]
                        <= self._variables["generation_threshold"]
                    ].index,
                    k=self._variables["n_r"],
                )
            return tuple(R_index)

        if self._variables["optimization"]:
            X_new = pd.DataFrame(columns=self._variables["sample_column"])
            X_new["reactant_index"] = X_resample.apply(single_proposal, axis=1)
        else:
            X_new = self.random_initialize()
        return X_new

    def pool_enrichment(self, X, X_fp):
        if self._variables["SMC_enrich"]:
            pool_addition = pd.DataFrame()
            pool_addition["SMILES"] = X["product"]
            pool_addition = pool_addition[
                ~pool_addition.SMILES.isin(self._pool["SMILES"])
            ]
            pool_addition_fp = X_fp.loc[pool_addition.index]
            pool_addition["parents"] = X.loc[pool_addition.index]["reactant_index"]
            pool_addition_mapping = self._gtm_model.transform(pool_addition_fp)
            pool_addition["map_x"] = [round(a[0] * 10) for a in pool_addition_mapping]
            pool_addition["map_y"] = [round(a[1] * 10) for a in pool_addition_mapping]
            pool_addition["generation"] = [
                sum([self._pool.loc[parent_id]["generation"] for parent_id in parents])
                for parents in pool_addition["parents"]
            ]
            pool_n_old = self._pool.shape[0]
            self._pool = pd.concat([self._pool, pool_addition], ignore_index=True)
            print("SMC: pool size {} -> {}".format(pool_n_old, self._pool.shape[0]))

    def in_storage(self, X, t):
        if self._variables["reactor_enrich"]:
            gpu_i = t % self._variables["n_forward"]
            gpu_path = self._variables["warehouse"] + "/" + str(gpu_i)
            pathlib.Path(gpu_path).mkdir(parents=True, exist_ok=True)
            done = False
            while not done:
                try:
                    X.to_csv(gpu_path + "/" + str(t) + ".csv", index=False)
                    print("SMC: put {} into storage.".format(t))
                    done = True
                except:
                    print("SMC in storage error.")

    def single_step(self, X, t):
        self.update_pool()
        X_resample = self.resample(X)
        X = self.proposal(X_resample)
        X = self.load_smiles(X)
        X = self.unique(X)
        X = self.react(X)
        X, X_fp = self._estimator.predict(X)
        X = self.compute_likelihood(X)
        X = self.in_black(X)
        self.save_df(X, t)
        self.in_storage(X, t)
        self.pool_enrichment(X, X_fp)
        return X

    def __call__(self):
        if self._variables["reactor_enrich"]:
            self._pool.to_csv(self._variables["pool_updated_path"], index=False)

        X = self.random_initialize()
        X = self.load_smiles(X)
        X = self.unique(X)
        X = self.react(X)
        X, X_fp = self._estimator.predict(X)
        X = self.compute_likelihood(X)
        X = self.in_black(X)
        for t in range(self._variables["n_smc_steps"]):
            start = time.time()
            X = self.single_step(X, t)
            time_cost = time.time() - start
            self.save_time(t, time_cost)
            X_target = X.loc[X[self._prefix + "target"] == 0]
            X_target_new = X_target.loc[X_target["is_new"]]
            n_target = len(set(X_target["reactant_index"]))
            n_target_new = len(set(X_target_new["reactant_index"]))
            self.save_new_number(t, n_target_new)
            print(
                "SMC: Step {}, target {}, new target {}, max rgen {}".format(
                    t, n_target, n_target_new, X["r1_gen"].max()
                )
            )
