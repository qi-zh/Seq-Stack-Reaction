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
5. [Applications](#Applications)
6. [Copyright and license](#Copyright-and-license)
7. [References](#References)

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
|reactor_gpu_id|Index of GPU, -1 for CPU|
|n_forward|Number of forward prediction modules|
|n_smc_steps|Total number of Sequential Monte Carlo steps|
|n|Number of particles in each Sequential Monte Carlo step|
|n_r|Number of reaction steps, larger than 1|
|generation_threshold|The threshold for filtering the reactant, 1 for only using initial reactants, larger value result to more complex reaction|
|product_len|Maxmum length of the product SMILES|
|p_exploitation|Proportion of particles for "exploitation"|
|refresh_rate|The refresh time by which the forward prediction module check the ourput of the Sequential Monte Carlo module|
|target_region|Region of the properties of interest|

#### customize models
Seq-Stack-Reaction provides a scaffolding for molecular design, where users can plug-in arbitrary reaction prediction models, property prediction models, and a set of commercial compounds.

To use your property prediction models and the set of commercial compounds, simply modify the model/data path in the `ssr/setting.json` file.

To use your customized reaction prediction model, see this [guidence](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/customization.ipynb).

---
## Applications
---
## Application 1: design of drug-like molecules
### Introduction

The task is to design drug-like molecules with any given region of drug-likeness (QED) score and logP.

### Download materials

Download the following components.
|Component|Description|
|----|----|
|[pool.csv](https://figshare.com/articles/dataset/Enamine_SMILES/19249589)|Initial reactant pool consists of [Enamine building block catalog lobal stock](https://enamine.net/building-blocks)|
|[molecular_transformer.pt](https://figshare.com/articles/software/Molecular_transformer/19249523)|Molecular Transformer model that predicts the product SMILES based on the reactant SMILES|
|[enamine_gtm](https://figshare.com/articles/software/enamine_gtm/19249493)|Generative Topographic Maps model for dimensionality reduction and clustering|
|[product_logp](https://figshare.com/articles/software/Property_prediction_model/19249526)|Regression model that predicts the log P value for a given product molecule|
|[product_qed](https://figshare.com/articles/software/Property_prediction_model/19249526)|Regression model that predicts the QED value for a given product molecule|
|[reactant_logp](https://figshare.com/articles/software/Property_prediction_model/19249526n)|Regression model that predicts the log P value for a given reactant set|
|[reactant_qed](https://figshare.com/articles/software/Property_prediction_model/19249526)|Regression model that predicts the QED value for a given reactant set|

---
## Application 2: design of highly viscous lubricant molecules

---
### Introduction

An example application in materials science. The task is to identify highly viscous lubricant
molecules. Using approximately 55,000 samples obtained from all-atom classical molecular dynamics
simulations, we predict the viscosity index (VI) and dynamic viscosity index (DVI) (properties that
describe the temperature dependence of viscosity) from the chemical structure of any given lubricant
molecule.

### Summary

First, forward models predicting VI and DVI are constructed. An input molecule is transformed into a binary descriptor vector of dimension 3239 with the concatenation of [RDKit fingerprints](http://rdkit.org/) (length 2048), [Molecular ACCess System keys](https://www.semanticscholar.org/paper/Reoptimization-of-MDL-Keys-for-Use-in-Drug-Durant-Leland/ad40b25e38314f39a82f193dc4806e6a1c2c6b69) (length 167), and [Morgan fingerprints](https://pubs.acs.org/doi/10.1021/c160017a018) of radius 2 (length 1024). The gradient boosting regression is applied to learn a mapping from any given fingerprinted molecule to VI or DVI. As a reaction prediction model, we employed the [Molecular Transformer](https://pubmed.ncbi.nlm.nih.gov/31572784/). This attention-based neural translation model defines a translation between the SMILES strings of reactants and their products. We use a subset of the Enamine building block catalog global stock as the set of commercially available reactants by which virtual molecules are synthesized. The design task is to identify highly synthesizable products showing higher VI and DVI that can be synthesized with the Molecular Transformer using with the set of commercially available reactants. In the example code, we perform SMC-RECUR-GTM-SR-PL in which the number of iterations is set to T=500, the number of particles is set to m=100, the exploration-exploitation trade-off parameter of the proposal distribution is set to alpha = 0.8. We illustrate the change of the joint distribution of predicted VI and DVI for increasing steps of SMC [here](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/properties.png). Four examples of synthetic products exhibiting high VI and DVI and their designed reaction pathways are illustrated [here](https://github.com/qi-zh/Seq-Stack-Reaction/tree/main/examples/lubricant_design/synthetic_path)

---
### Property refinements in different steps
![property](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/properties.png)

---
### Designed synthetic route pathways
- <img src="https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route1.png" width=500>
- <img src="https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route2.png" width=500>
- <img src="https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route3.png" width=500>
- <img src="https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route4.png" width=500>
- 
---
### Download materials

Download Python pre-trained model.
|Component|Description|
|----|----|
|[product_vi](https://figshare.com/ndownloader/files/39489250)|Regression model that predicts the viscosity index value for a given product molecule|
|[product_dvi](https://figshare.com/ndownloader/files/39489253)|Regression model that predicts the dynamic viscosity index value for a given product molecule|
|[reactant_vi](https://figshare.com/ndownloader/files/39489259)|Regression model that predicts the viscosity index value for a reactant set|
|[reactant_dvi](https://figshare.com/ndownloader/files/39489256)|Regression model that predicts the dynamic viscosity index value for a reactant set|

---
### Data
##### Refer to [Kajita et al.](https://www.nature.com/articles/s42005-020-0338-y#Sec14) for more details about the design of this experiment and the data used for model training.
---
## Copyright and license

---
## References
Landrum, G. et al. RDKit: Open-source cheminformatics (2006). http://rdkit.org/

Durant, J. L., Leland, B.A., Henry, D.R., et al. Reoptimization of MDL keys for use in drug discovery. J Chem Inf Comput Sci 42, 6. 1273–1280 (2002). https://www.semanticscholar.org/paper/Reoptimization-of-MDL-Keys-for-Use-in-Drug-Durant-Leland/ad40b25e38314f39a82f193dc4806e6a1c2c6b69

Morgan, H.L. The generation of a unique machine description for chemical structures-a technique developed at chemical abstracts service. J Chem Doc 5, 107–113 (1965). https://pubs.acs.org/doi/10.1021/c160017a018

Schwaller, P. et al. Molecular Transformer: a model for uncertainty-calibrated chemical reaction prediction. ACS Cent Sci 5, 9 1572-1583 (2019).

Kajita, S., Kinjo, T., Nishi, T. Autonomous molecular design by Monte-Carlo tree search and rapid evaluations using molecular dynamics simulations. Commun Phys 3, 77 (2020). https://doi.org/10.1038/s42005-020-0338-y
