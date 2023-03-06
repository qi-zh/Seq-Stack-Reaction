<h1 align="center">
  <br>
  Seq-Stack-Reaction
  <br>
</h1>

<h4 align="center">Software for "A Bayesian Method for Concurrently Designing Molecules and Synthetic Reaction Networks"</h4>

---

## Table of contents
1. [Installation](#installation)
2. [Download materials](#download-materials)
3. [Quick start](#quick-start)
4. [Customize experiment](#customize-experiment)
5. [Copyright and license](#Copyright-and-license)
6. [References](#References)

---

## Installation

#### STEP 1: Get source code.
```shell
# Step 1: Get sources from GitHub
$ git clone git@github.com:qi-zh/Seq-Statck-Reaction.git
```
#### STEP 2: Create conda environment.

Make sure you have [Conda](https://docs.conda.io/projects/conda/en/latest/) installed.
```shell
# Step 2: Create conda environment
$ cd conda_env
$ conda env create -f ssr.yml
$ conda activate ssr
```
#### The following table lists some core packages in SSR images.
<table>
  <tr>
    <td nowrap><strong>Pytorch</strong></td>
    <td>1.7.1</td>
  </tr>
  <tr>
    <td nowrap><strong>OpenNMT</strong></td>
    <td>1.2.0</td>
  </tr>
  <tr>
    <td nowrap><strong>rdkit</strong></td>
    <td>2020.03.1</td>
  </tr>
  <tr>
    <td nowrap><strong>ugtm</strong></td>
    <td>2.0.0</td>
  </tr>
</table>

---
## Download materials

Download the following components.
|Component|Description|
|----|----|
|[pool.csv](https://figshare.com/articles/dataset/Enamine_SMILES/19249589)|initial reactant pool consists of [Enamine building block catalog lobal stock](https://enamine.net/building-blocks)|
|[molecular_transformer.pt](https://figshare.com/articles/software/Molecular_transformer/19249523)|Molecular Transformer model that predicts the product SMILES based on the reactant SMILES|
|[enamine_gtm](https://figshare.com/articles/software/enamine_gtm/19249493)|Generative Topographic Maps model for dimensionality reduction and clustering|
|[product_logp](https://figshare.com/articles/software/Property_prediction_model/19249526)|regression model that predicts the log P values based on the product molecules|
|[product_qed](https://figshare.com/articles/software/Property_prediction_model/19249526)|regression model that predicts the QED values based on the product molecules|
|[reactant_logp](https://figshare.com/articles/software/Property_prediction_model/19249526n)|regression model that predicts the log P values based on the reactant molecules|
|[reactant_qed](https://figshare.com/articles/software/Property_prediction_model/19249526)|regression model that predicts the QED values based on the reactant molecules|

Refer to the following folder hierarchy and move each model and data to its folder.

```shell
─SSR
 ├─ssr
 │ └─*.py
 ├─data
 │ └─pool.csv
 ├─model
 │ ├─molecular_transformer.pt
 │ ├─GTM
 │ │ └─enamine_gtm
 │ └─QSPR
 │   ├─product_logp
 │   ├─product_qed
 │   ├─reactant_logp
 │   └─reactant_qed
 ├─conda_env
 │ └─ssr.yml
 ├─*.py
 └─*.ipynb
```

---
## Quick start

quick implementation of molecular design

#### STEP 1: Launch the forward prediction module.
```shell
# Run the following command in a shell session.
$ python launch_forward.py
```
#### STEP 2: Launch the Sequential Monte Carlo module.
```shell
# Run the following command in another shell session.
$ python launch_smc.py
```
---
## Customize experiment

#### customize parameters
The following parameters are adjustable in the `ssr/setting.json` file.

|Parameter|Description|
|----|----|
|reactor_gpu_id|index of GPU, -1 for CPU|
|n_forward|number of forward prediction modules|
|n_smc_steps|total number of Sequential Monte Carlo steps|
|n|number of particles in each Sequential Monte Carlo step|
|n_r|number of reaction steps, larger than 1|
|generation_threshold|the threshold for filtering the reactant, 1 for only using initial reactants, larger value result to more complex reaction|
|product_len|maxmum length of the product SMILES|
|p_exploitation|proportion of particles for "exploitation"|
|refresh_rate|the refresh time by which the forward prediction module check the ourput of the Sequential Monte Carlo module|
|target_region|region of the properties of interest|

#### customize models
Seq-Stack-Reaction provides a scaffolding for molecular design, where users can plug-in arbitrary reaction prediction models, property prediction models, and a set of commercial compounds.

To use your property prediction models and the set of commercial compounds, simply modify the model/data path in the `ssr/setting.json` file.

To use your customized reaction prediction model, see this [guidence](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/customization.ipynb).

---
## Application 1: design of drug-like molecules

---
## [Application 2: design of highly viscous lubricant molecules](https://github.com/qi-zh/Seq-Stack-Reaction/tree/main/examples/lubricant_design)

---
### Introduction

An example application in materials science. The task is to identify highly viscous lubricant
molecules. Using approximately 55,000 samples obtained from all-atom classical molecular dynamics
simulations, we predict the viscosity index (VI) and dynamic viscosity index (DVI) (properties that
describe the temperature dependence of viscosity) from the chemical structure of any given lubricant
molecule.

---
### Download materials

The forward property prediction models.
|Component|Description|
|----|----|
|[product_vi](https://figshare.com/ndownloader/files/39489250)|regression model that predicts the viscosity index values based on the product molecules|
|[product_dvi](https://figshare.com/ndownloader/files/39489253)|regression model that predicts the dynamic viscosity index values based on the product molecules|
|[reactant_vi](https://figshare.com/ndownloader/files/39489259)|regression model that predicts the viscosity index values based on the reactant molecules|
|[reactant_dvi](https://figshare.com/ndownloader/files/39489256)|regression model that predicts the dynamic viscosity index values based on the reactant molecules|

---
### Data
Refer to [Kajita et al.](https://www.nature.com/articles/s42005-020-0338-y#Sec14) for more details about the design of this experiment and the data used for model training.
---
## Copyright and license

---
## References
