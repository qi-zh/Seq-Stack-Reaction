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
#### The following table list some core packages in SSR images.
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

refer to the following folder hierarchy, move each model and data to its folder.

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

---
## Customize experiment

---
## Copyright and license

---
## References
