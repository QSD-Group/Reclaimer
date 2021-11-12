# Reclaimer System

This repository contains the Python scripts used for techno-economic analysis (TEA) and life cycle assessment (LCA) for the liquid reclaimer system described in [Trotochaud et al., 2020](https://doi.org/10.1021/acs.est.0c03296).

- The `CSVforCode` folder contains `.csv` files needed for running the scripts.
- The `Results` folder contains archived results generated from running the scripts.
- `Country_Specific_Reclaimer.py` and `Country_Specific_Sensitivity.py` are used for TEA/LCA and sensitivity analysis using country-specific data.
- `doe_lhs.py` and `lhs_python.py` are used for Latin hypercube sampling.
- `TEA.py` and `Uncertainty_TEA.py` contain the codes for TEA under uncertainty.