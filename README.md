[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380+/)
[![Read the Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](bit.ly/treat_sim)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6860711.svg)](https://doi.org/10.5281/zenodo.6860711)
[![License: MIT](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![License: MIT](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

# 💫 Treatment Simulation Model deployed via Streamlit

> 💫 Please note that this work has been merged into the [**S**haring **T**ools and **A**rtifacts for **R**eproducible **S**imulations (STARS) in healthcare project](https://github.com/pythonhealthdatascience).  A more up-to-date example of this app is available: https://github.com/pythonhealthdatascience/stars-streamlit-example 💫

## Overview

The code in this repo occompanies the conference paper:

> Monks, T. and Harper. A, (2023) **A framework to share healthcare simulations on the web using free and open source tools and python**

The code focusses on the Streamlit deployment of the model.  

## Author ORCIDs

[![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

## Write up of study

A preprint is being prepared. Methods, and Results are regularly updated in our online Jupyter Book [https://tommonks.github.io/treatment-centre-sim](https://tommonks.github.io/treatment-centre-sim)

## Aims of the study

The overarching aim of our study is to identify robust ways that python discrete-event simulation models can be shared with other health researchers and NHS care providers.

Specific objectives of the study that this code supports are:

1. Outline a straightforward framework for deploying a simulation developed in Python on the web for users of varying technical skills;
2. Provide an applied simulation example implementing our framework;
3. Provide guidance for modellers to **begin** haring models built using FOSS via the web.

## Funding

This code is part of independent research supported by the National Institute for Health Research Applied Research Collaboration South West Peninsula. The views expressed in this publication are those of the author(s) and not necessarily those of the National Institute for Health Research or the Department of Health and Social Care.

## Streamlit community cloud deployment of the code

* https://treat-sim.streamlit.app

## Cite this model

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6860711.svg)](https://doi.org/10.5281/zenodo.6860711)

```bibtex
@software{monks_thomas_2022_6860711,
  author       = {Monks, Thomas and
                  Harper, Alison},
  title        = {TomMonks/treat\_sim\_streamlit: v1.0.0},
  month        = jul,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.6860711},
  url          = {https://doi.org/10.5281/zenodo.6860711}
}
```

## Dependencies

[![Python 3.9+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380+/)

All dependencies can be found in [`binder/environment.yml`]() and are pulled from conda-forge.  To run the code locally, we recommend install [mini-conda](https://docs.conda.io/en/latest/miniconda.html); navigating your terminal (or cmd prompt) to the directory containing the repo and issuing the following command:

> `conda env create -f binder/environment.yml`

## Docker container

A containerised version of the model is available from Dockerhub.  Follow the link and the instructions provided.  Note tht you will need docker installed in order to pull and run the container.

* https://hub.docker.com/r/tommonks01/streamlit_sim


