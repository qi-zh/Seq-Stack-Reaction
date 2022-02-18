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

Download

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
