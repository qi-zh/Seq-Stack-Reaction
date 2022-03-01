from rdkit import Chem
from rdkit.Chem import MACCSkeys as MAC
from rdkit.Chem import rdMolDescriptors as rdMol
import numpy as np
import pandas as pd
import pickle


def Featurizer_list(smiles_list):
    def RDKFP(smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [np.nan] * 3239
        return (
            list(Chem.RDKFingerprint(mol, fpSize=2048, nBitsPerHash=2))
            + list(MAC.GenMACCSKeys(mol))
            + list(rdMol.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=1024))
        )

    return np.array([RDKFP(s) for s in smiles_list])


class Featurizer_Df:
    def __init__(self, featurizer_list, column_list):
        assert (
            len(column_list) > 0
        ), "featurizer_df: column_list should contain at least one column name."
        self._featurizer_list = featurizer_list
        self._column_list = column_list

    def featurize_col(self, smiles_list):
        return np.concatenate(
            [featurizer(smiles_list) for featurizer in self._featurizer_list], axis=1
        )

    def featurize(self, x):
        assert all(
            [col in x.columns for col in self._column_list]
        ), "featurizer_df: input dataframe x does not contain specific column_list."
        fp_list = [self.featurize_col(x[col]) for col in self._column_list]
        x_fp = sum(fp for fp in fp_list)
        x_fp[x_fp > 1] = 1
        return pd.DataFrame(x_fp)


class QSPR_model:
    def __init__(self, variables):

        self._variables = variables
        self._estimator_dic = {}
        if variables["surrogate"]:
            self._prefix = "surrogate_"
            self._target_col = ["r" + str(i + 1) for i in range(variables["n_r"])]
        else:
            self._prefix = ""
            self._target_col = ["product"]
        self._featurizer = Featurizer_Df(
            featurizer_list=[Featurizer_list], column_list=self._target_col
        )
        for y in self._variables["y_list"]:
            self._estimator_dic[y] = pickle.load(
                open(self._variables[self._prefix + "forward_model_path"][y], "rb")
            )


    def predict(self, x):
        x_fp = self._featurizer.featurize(x).replace([np.inf, -np.inf], np.nan).dropna()
        x = x.loc[x_fp.index].reset_index(drop=True)
        x_fp.reset_index(drop=True, inplace=True)
        assert (
            x.shape[0] == x_fp.shape[0]
        ), "number of fingerprint does not mach the number of particles, invalid product may exhist."
        for y in self._variables["y_list"]:
            x[self._prefix + y] = self._estimator_dic[y].predict(x_fp)
        return x, x_fp


from rdkit.Chem import QED, MolFromSmiles, Crippen


class QSPR_model_rdkit:
    def __init__(self, variables):
        self._variables = variables
        self._featurizer = Featurizer_Df(
            featurizer_list=[Featurizer_list], column_list=["product"]
        )

    def predict(self, x):
        print("QSPR by RDKit")
        valid_list = []
        qed_list = []
        logp_list = []
        for p in x["product"]:
            mol = MolFromSmiles(p)
            if mol is None:
                valid_list.append(False)
            else:
                valid_list.append(True)
                qed_list.append(QED.qed(mol))
                logp_list.append(Crippen.MolLogP(mol))
        x["valid"] = valid_list
        x = x.loc[x["valid"]].reset_index(drop=True)
        x_fp = self._featurizer.featurize(x).replace([np.inf, -np.inf], np.nan).dropna()
        x["qed"] = qed_list
        x["logp"] = logp_list
        assert x.shape[0] == x_fp.shape[0]
        return x, x_fp
