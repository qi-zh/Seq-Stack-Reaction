import json
import pathlib
from datetime import date
from ssr import SMC
import pandas as pd
from ssr import Reactor

import warnings
warnings.filterwarnings("ignore")

with open("./setting.json") as f:
    variables = json.load(f)
main_path = variables["main_path"]

variables_addition = {
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


variables["experiment_date"] = str(date.today())
variables["n_r"] = variables["n_r"] + 1



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

if variables["model_name"] == "SMC-RECUR_GTM":
    variables["SMC_reactor"] = True
    variables["surrogate"] = False
    variables["SMC_enrich"] = True
    variables["reactor_enrich"] = False
    variables["optimization"] = True
elif variables["model_name"] == "SMC-RECUR_GTM_SR_PL":
    variables["SMC_reactor"] = False
    variables["surrogate"] = True
    variables["SMC_enrich"] = False
    variables["reactor_enrich"] = True
    variables["optimization"] = True
elif variables["model_name"][:-1] == "SMC_":
    variables["SMC_reactor"] = True
    variables["surrogate"] = False
    variables["SMC_enrich"] = False
    variables["reactor_enrich"] = False
    variables["n_r"] = int(variables["model_name"][4:])
    variables["optimization"] = True
elif variables["model_name"] == "Random":
    variables["SMC_reactor"] = True
    variables["surrogate"] = False
    variables["SMC_enrich"] = False
    variables["reactor_enrich"] = False
    variables["p_exploitation"] = 0
    variables["optimization"] = False
elif variables["model_name"] == "Random_RECUR":
    variables["SMC_reactor"] = True
    variables["surrogate"] = False
    variables["SMC_enrich"] = True
    variables["reactor_enrich"] = False
    variables["p_exploitation"] = 0
    variables["optimization"] = False
else:
    raise Exception("wrong model name: {}".format(variables["model_name"]))

model_result_path = (
    main_path
    + "results/"
    + variables["experiment_date"]
    + "/"
    + variables["model_name"]
)
variables["model_df_path"] = model_result_path + "/dfs/"
if variables["reactor_enrich"]:
    variables["warehouse"] = model_result_path + "/warehouse"
    variables["warehouse_key"] = variables["warehouse"] + "/key"
    pathlib.Path(variables["warehouse"]).mkdir(parents=True, exist_ok=True)
    open(variables["warehouse_key"], "a").close()
    variables["pool_folder"] = model_result_path + "/pool_folder"
    variables["pool_folder_key"] = variables["pool_folder"] + "/key"
    variables["pool_updated_marker"] = variables["pool_folder"] + "/updated_marker"
    variables["pool_updated_path"] = variables["pool_folder"] + "/updated_pool.csv"
    pathlib.Path(variables["pool_folder"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(variables["pool_folder"] + "/addition").mkdir(
        parents=True, exist_ok=True
    )
    open(variables["pool_folder_key"], "a").close()

if __name__ == "__main__":
    initial_reactant_pool = pd.read_csv(variables["initial_pool_path"])
    print("SMC: initial pool size: {}".format(initial_reactant_pool.shape[0]))
    
    if variables["SMC_reactor"]:
        reactor = Reactor(variables=variables)
    else:
        reactor = None
            
    SMC_instance = SMC(variables=variables, pool=initial_reactant_pool, reactor=reactor)
    SMC_instance()
