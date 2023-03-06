import json

with open("./setting.json") as f:
    variables = json.load(f)
main_path = variables["main_path"]
variables_addition = {
    "reactor_id": "0",
    "initial_pool_path": main_path + "data/pool.csv",
    "gtm_path": main_path + "model/GTM/enamine_gtm",
    "reactor_model_path": main_path + "model/molecular_transformer.pt",
    "sample_column": [
        "reactant",
        "product",
        "reactant_index",
        "ll",
        "surrogate_ll",
        "c_label",
        "freq",
        "target",
        "surrogate_target",
        "is_new",
    ],
    "surrogate_forward_model_path": {
        "vi": main_path + "model/QSPR/reactant_vi",
        "dvi": main_path + "model/QSPR/reactant_dvi",
    },
    "forward_model_path": {
        "vi": main_path + "model/QSPR/product_vi",
        "dvi": main_path + "model/QSPR/product_dvi",
    },
    "unique_col": "reactant_index",
    "black": "False",
}
variables.update(variables_addition)
variables["model_name"] = "SMC-RECUR_GTM_SR_PL"
from datetime import date

variables["experiment_date"] = str(date.today())
variables["n_r"] = variables["n_r"] + 1

import warnings

warnings.filterwarnings("ignore")


for i in range(variables["n_r"]):
    variables["sample_column"].append("r" + str(i + 1))
    variables["sample_column"].append("r" + str(i + 1) + "_id")
    variables["sample_column"].append("r" + str(i + 1) + "_gen")
    if i > 0:
        variables["sample_column"].append("p" + str(i))
for y in variables["y_list"]:
    variables["sample_column"].append(y)
    variables["sample_column"].append("surrogate_" + y)
variables["generation_temperature"] = -1 / variables["generation_threshold"] * 2

model_result_path = (
    main_path
    + "results/"
    + variables["experiment_date"]
    + "/"
    + variables["model_name"]
)
variables["model_df_path"] = model_result_path + "/dfs/"
variables["warehouse"] = model_result_path + "/warehouse"
variables["warehouse_key"] = variables["warehouse"] + "/key"

variables["pool_folder"] = model_result_path + "/pool_folder"
variables["pool_folder_key"] = variables["pool_folder"] + "/key"
variables["pool_updated_marker"] = variables["pool_folder"] + "/updated_marker"
variables["pool_updated_path"] = variables["pool_folder"] + "/updated_pool.csv"

variables["surrogate"] = False

from ssr import Forward_model



if __name__ == "__main__":
    forward = Forward_model(variables)
    forward()
