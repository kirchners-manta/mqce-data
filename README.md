# mqce-data
---

This repository contains the data for our paper on the mQCE theory. 
This paper is currently under review.
The data is organized as follows:
* [`clusters`](./clusters): contains the clusters used in the paper.
* [`qce`](./qce): contains the data for the bulk phase QCE calculations.
* [`qce0`](./qce0): contains the data for the gas phase QCE calculations.

For every cluster, a `.flist` and `.xyz` file is provided, containing the list of frequencies and the geometry of the cluster, respectively. 
The `.clusterset` files are required as input by PEACEMAKER.

In the QCE and QCE0 directories, the exact PEACEMAKER inputs and outputs are provided for every calculated composition.
The composition is denoted by `c_m_w`, where `c`, `m`, and `w` denote the mole fraction of chloroform, methanol, and water, respectively.
