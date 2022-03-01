import torch
from .load_reactor import load_reactor
import pickle
import pandas as pd


class Reactor:
    def __init__(self, variables, estimator=None):
        self._variables = variables
        self._reactor = load_reactor(
            max_length=variables["product_len"],
            model_path=variables["reactor_model_path"],
            device_id=variables["reactor_gpu_id"],
        )
        self._estimator = estimator
        self._gtm_model = pickle.load(open(variables["gtm_path"], "rb"))
        self._pool = None

    def pool_enrichment(self, x, x_fp, _pool):
        pool_addition = pd.DataFrame()
        pool_addition["SMILES"] = x["product"]
        pool_addition = pool_addition[~pool_addition.SMILES.isin(_pool["SMILES"])]
        x_fp = x_fp.loc[pool_addition.index]
        x = x.loc[pool_addition.index]
        pool_addition_mapping = self._gtm_model.transform(x_fp)
        pool_addition["map_x"] = [round(a[0] * 10) for a in pool_addition_mapping]
        pool_addition["map_y"] = [round(a[1] * 10) for a in pool_addition_mapping]
        pool_addition["parents"] = x["reactant_index"]
        pool_addition["generation"] = [
            _pool.loc[rein[0]]["generation"] + _pool.loc[rein[1]]["generation"]
            for rein in x["reactant_index"]
        ]
        _pool = pd.concat([_pool, pool_addition], ignore_index=True)
        return _pool

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
        if self._estimator:
            x, x_fp = self._estimator.estimate(x)
            return x, x_fp
        return x
