<h1 align="center">
  <br>
  Seq-Stack-Reaction
  <br>
</h1>

<h4 align="center">A software for "Bayesian sequential stacking algorithm for concurrently designing molecules and syntheticreaction networks".</h4>

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
|[pool.csv](https://github.com/qi-zh/Seq-Statck-Reaction)|Initial reactant pool consists of [Enamine building block catalog lobal stock](https://enamine.net/building-blocks).|
|[molecular_transformer.pt](https://github.com/qi-zh/Seq-Statck-Reaction)|A Molecular Transformer model that predicts the product SMILES based on the reactant SMILES.|
|[enamine_gtm](https://github.com/qi-zh/Seq-Statck-Reaction)|A Generative Topographic Maps model for dimensionality reduction and clustering.|
|[product_logp](https://github.com/qi-zh/Seq-Statck-Reaction)|A regression model that predicts the log P values based on the product molecules.|
|[product_qed](https://github.com/qi-zh/Seq-Statck-Reaction)|A regression model that predicts the QED values based on the product molecules.|
|[reactant_logp](https://github.com/qi-zh/Seq-Statck-Reaction)|A regression model that predicts the log P values based on the reactant molecules.|
|[reactant_qed](https://github.com/qi-zh/Seq-Statck-Reaction)|A regression model that predicts the QED values based on the reactant molecules.|

Refer to the following folder hierarchy, move each model and data to its folder.

```shell
─SSR
 ├─ssr
 │ └─*.csv
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
 └─conda_env
   └─ssr.yml
```

---
## Quick start

A quick implementation of molecular design.

#### STEP 1: Launch the forward prediction module.
```shell
# Run the following command in a shell session.
$ python ssr/forward.py
```
#### STEP 2: Launch the Sequential Monte Carlo module.
```shell
# Run the following command in another shell session.
$ python ssr/smc.py
```
---
## Customize experiment

The following parameters are adjustable in the `ssr/setting.json` file.

|Parameter|Description|
|----|----|
|reactor_gpu_id|Index of GPU, -1 for CPU.|
|n_forward|Number of forward prediction modules.|
|n_smc_steps|Total number of Sequential Monte Carlo steps.|
|n|Number of particles in each Sequential Monte Carlo step.|
|n_r|Number of reaction steps, larger than 1.|
|generation_threshold|The threshold for filtering the reactant, 1 for only using initial reactants, larger value result to more complex reaction.|
|product_len|Maxmum length of the product SMILES.|
|p_exploitation|Proportion of particles for "exploitation".|
|refresh_rate|The refresh time by which the forward prediction module check the ourput of the Sequential Monte Carlo module.|
|target_region|A region of the properties of interest.|

---
## Copyright and license

---
## References
