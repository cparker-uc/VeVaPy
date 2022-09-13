# VeVaPy Instructions

## Table of Contents
1. [Installation](#install)
2. [Binder Setup](#binderSetup)
3. [Model Selection](#modelSelection)
4. [Dependencies Required to Run Models Locally](#localDependencies)
5. [General Instructions](#generalInstructions)

## Installation <a name="install"/>

The VeVaPy modules (without the demonstration model notebooks) are most easily installed with the command

    pip install VeVaPy

However, they can also be downloaded directly from Github and placed in the directory of the model files you wish to test. In this case, see [Dependencies Required to Run Models Locally](#localDependencies) for the packages you'll need. You can also download only the Jupyter notebooks for the demonstration models you are interested in and use pip to install the VeVaPy modules and dependencies.

In order to avoid downloading anything to your local machine, you can also use a virtual Jupyter environment through Binder. See [Binder Setup](#binderSetup) for instructions.

## Binder Setup <a name="binderSetup"/>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cparker-uc/VeVaPy/HEAD)

Clicking the "Launch Binder" link above will open this repository in Binder, which allows you to run all of the Jupyter notebook files in your web browser without needing to have any software installed.

The Binder environment will already have all of the necessary Python modules ready, so all you need to do is open a model file and start running simulations.

## Model Selection <a name="modelSelection" />
This repository contains five different models and a general template for creating new ones, each in their own Jupyter notebook file. Below is a table listing all of the models included with short descriptions of them.

| Filename                              | Authors                                                                                                          | Year | Model Description                                                                                                                                                                                                              |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bairagi-2008.ipynb                    | N. Bairagi, S. Chatterjee & J. Chattopadhyay                                                                     | 2008 | One of the five models described in my paper.                                                                                                                                                                                   |
| Bangsgaard-Ottesen-2017.ipynb         | E.O. Bangsgaard & J.T. Ottesen                                                                                   | 2017 | One of the five models described in my paper.                                                                                                                                                                                   |
| Malek-2015.ipynb                      | H. Malek, M.H. Ebadzadeh, R. Safabakhsh, A. Razavi & J. Zaringhalam                                              | 2015 | One of the five models described in my paper.                                                                                                                                                                                   |
| Somvanshi-2020.ipynb                  | P.R. Somvanshi, S.H. Mellon, R. Yehuda, J.D. Flory, L. Bierer, I. Makotkine, C. Marmar, M. Jett & F.J. Doyle III | 2020 | One of the five models described in my paper.                                                                                                                                                                                   |
| Sriram-2012.ipynb                     | K. Sriram, M. Rodriguez-Fernandez & F.J. Doyle III                                                               | 2012 | One of the five models described in my paper.                                                                                                                                                                                   |
| VeVaPy Model Template.ipynb           | Christopher Parker                                                                                               | 2022 | Basic template for editing to easily verify and validate mathematical models of the Hypothalamic-Pituitary-Adrenal axis                   |

## Dependencies Required to Run Models Locally <a name="localDependencies" />
If you would prefer to run the models on your local machine, rather than in a Binder environment, the requirements listed in the following table will need to be met.

| Software   | Version | URL                                                         |
|------------|---------|-------------------------------------------------------------|
| Python     | 3.7.7   | https://www.python.org/downloads/                           |
| Jupyterlab | 2.1.5   | https://www.jupyter.org/install                             |
| NumPy      | 1.21.5  | https://numpy.org/install/                                  |
| matplotlib | 3.0.1   | https://matplotlib.org/stable/users/installing/index.html   |
| pandas     | 0.23.4  | https://pandas.pydata.org/docs/getting_started/install.html |
| mpld3      | 0.5.7   | https://mpld3.github.io/install.html                        |
| SciPy      | 1.1.0   | https://scipy.org/install/                                  |
| tabulate   | 0.8.9   | https://pypi.org/project/tabulate/                          |

## General Instructions <a name="generalInstructions" />
Once you have set up a Binder environment or installed all of the dependencies locally, open any of the five models discussed in the paper and select "Instructions" from the Table of Contents. Each model has instructions tailored to its specific needs, although they are largely the same. Good luck, and have fun!
