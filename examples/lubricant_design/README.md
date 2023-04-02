<h1 align="center">
  
</h1>

<h4 align="center"> Scripts to implement the molecular design with lubricant-related properties as the target.</h4>

---
## Quick start

An example application in materials science. The task is to identify highly viscous lubricant
molecules. Using approximately 55,000 samples obtained from all-atom classical molecular dynamics
simulations, we predict the viscosity index (VI) and dynamic viscosity index (DVI) (properties that
describe the temperature dependence of viscosity) from the chemical structure of any given lubricant
molecule.

---
## Download materials

The forward property prediction models.
|Component|Description|
|----|----|
|[product_vi](https://figshare.com/ndownloader/files/39489250)|regression model that predicts the viscosity index values based on the product molecules|
|[product_dvi](https://figshare.com/ndownloader/files/39489253)|regression model that predicts the dynamic viscosity index values based on the product molecules|
|[reactant_vi](https://figshare.com/ndownloader/files/39489259)|regression model that predicts the viscosity index values based on the reactant molecules|
|[reactant_dvi](https://figshare.com/ndownloader/files/39489256)|regression model that predicts the dynamic viscosity index values based on the reactant molecules|

---
## Data
Refer to [Kajita et al.](https://www.nature.com/articles/s42005-020-0338-y#Sec14) for more details about the design of this experiment and the data used for model training.

---
## Properties in different steps
![property](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/properties.png)

---
## Designed synthetic path
<img "https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route1.png" width=300>
![path1](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route1.png)
![path2](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route2.png)
![path3](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route3.png)
![path4](https://github.com/qi-zh/Seq-Stack-Reaction/blob/main/examples/lubricant_design/synthetic_path/route4.png)

---

