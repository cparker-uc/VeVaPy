#  Instructions for Use of Models

## Table of Contents
1. [Binder Setup](#binderSetup)
2. [Model Selection](#modelSelection)
3. [General Instructions](#generalInstructions)
4. [Requirements to Run Models Locally](#localRequirements)

## Binder Setup <a name="binderSetup"/>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cparker-uc/PTSD/HEAD)

Clicking the link above will open this repository in Binder, which allows you to run all of the Jupyter notebook files in your web browser without needing to have any software installed.

However, the Binder environment will require some setup in order to get the models running properly (I apologize if these instructions are too long-winded, but I want to make sure that anyone can use my code!). Once the environment has fully loaded, you will see the home screen with the file browser on the left and the Launcher on the right. In the bottom row of Launcher icons, there is a black box with $\_ shown in it, and it says Terminal--click on it.

Now that you have a Terminal session open, there should be a prompt with a bunch of random characters that ends with :~$ and a blinking black cursor. Copy and paste the following into the Terminal and press Enter:

```
pip install numpy matplotlib scipy mpld3 tabulate pandas
```
This will install all of the necessary Python modules to run all of the models included in this repository, and you can now close the Terminal tab and select any model from the file browser on the left. This setup will need to be performed each time you restart the Binder environment, unfortunately.

## Model Selection <a name="modelSelection" />
This repository contains quite a few different models, each in their own Jupyter notebook file. Below is a table listing all of the models included with short descriptions of them.

| Filename                              | Authors                                                                                                          | Year | Model Description                                                                                                                                                                                                              |   |   |   |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---|---|
| Andersen-Vinther-Ottesen-2013.ipynb   | M. Andersen, F. Vinther & J.T. Ottesen                                                                           | 2013 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Bairagi-2008.ipynb                    | N. Bairagi, S. Chatterjee & J. Chattopadhyay                                                                     | 2008 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Bangsgaard-Ottesen-2017.ipynb         | E.O. Bangsgaard & J.T. Ottesen                                                                                   | 2017 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Best-2010.ipynb                       | J. Best, H.F. Nijhout & M. Reed                                                                                  | 2010 | Describes serotonin synthesis and release (we were hoping to include this behavior in a systems biology approach to studying MDD and/or PTSD, but couldn't find experimental data to validate the model).                      |   |   |   |
| Gudmand-Hoeyer-Blood-Model-2018.ipynb | J. Gudmand-Hoeyer & J.T. Ottesen                                                                                 | 2018 | A chemical reaction-based model of free and bound cortisol in blood.                                                                                                                                                           |   |   |   |
| Kim-DOrsogna-Chou-2017.ipynb          | L.U. Kim, M.R. D'Orsogna & T. Chou                                                                               | 2017 | The authors did not include all necessary parameters and initial conditions to run the dimensional version of the model, and I have been unable to get the model running smoothly.                                             |   |   |   |
| Malek-2015.ipynb                      | H. Malek, M.H. Ebadzadeh, R. Safabakhsh, A. Razavi & J. Zaringhalam                                              | 2015 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Savic-2000.ipynb                      | D. Savic, G. Knezevic & G. Opacic                                                                                | 2000 | Attempted to model the HPA system under stress, but is unable to match real-world data well at all.                                                                                                                            |   |   |   |
| Somvanshi-2020.ipynb                  | P.R. Somvanshi, S.H. Mellon, R. Yehuda, J.D. Flory, L. Bierer, I. Makotkine, C. Marmar, M. Jett & F.J. Doyle III | 2020 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Sriram-2012.ipynb                     | K. Sriram, M. Rodriguez-Fernandez & F.J. Doyle III                                                               | 2012 | One of the six models described in my paper.                                                                                                                                                                                   |   |   |   |
| Stanojevic-2018.ipynb                 | A. Stanojevic, V.M. Markovic, Z. Cupic, L. Kolar-Anic & V. Vukojevic                                             | 2018 | Chemical reaction-based system of ODEs. This model was created with concentration units in moles per liter, which required conversion of the real-world data units to match.                                                   |   |   |   |
| Stanojevic-2018-micromolar.ipynb      | A. Stanojevic, V.M. Markovic, Z. Cupic, L. Kolar-Anic & V. Vukojevic                                             | 2018 | Same as Stanojevic-2018.ipynb but with units converted to micromolar for increased accuracy when computing cost function (because molar units lead to very small concentration values which introduced extra rounding errors). |   |   |   |
| Stanojevic-2018-nanomolar.ipynb       | A. Stanojevic, V.M. Markovic, Z. Cupic, L. Kolar-Anic & V. Vukojevic                                             | 2018 | Same as Stanojevic-2018.ipynb but with units converted to nanomolar for increased accuracy when computing cost function (because molar units lead to very small concentration values which introduced extra rounding errors).  |   |   |   |
| Vinther-2011.ipynb                    | F. Vinther, M. Andersen & J.T. Ottesen                                                                           | 2011 | Described by the authors as the "Minimal Model of the HPA Axis," this is a very bare-bones model and thus does not perform well on validation against real-world basal data (haven't tested with TSST data).                   |   |   |   |
## General Instructions <a name="generalInstructions" />

## Requirements to Run Models Locally <a name="localRequirements" />
