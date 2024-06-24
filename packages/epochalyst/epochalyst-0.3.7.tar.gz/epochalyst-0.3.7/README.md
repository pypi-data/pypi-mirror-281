![image](./docs/_static/images/logo/Epochalyst_Logo_Dark.png#gh-light-mode-only)
![image](./docs/_static/images/logo/Epochalyst_Logo_Light.png#gh-dark-mode-only)

[![PyPI Latest Release](https://img.shields.io/pypi/v/epochalyst.svg)](https://pypi.org/project/epochalyst/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/epochalyst.svg?label=PyPI%20downloads)](https://pypi.org/project/epochalyst/)

Epochalyst is the base for [Team Epoch](https://teamepoch.ai/) competitions.

This package contains many modules and classes necessary to construct the src code for machine learning competitions.

Epochalyst: A fusion of "Epoch" and "Catalyst," this name positions your pipeline as a catalyst in the field of machine learning, sparking significant advancements and transformations.

## Installation

Install `epochalyst` via pip:

```shell
pip install epochalyst
```

Or using [Poetry](https://python-poetry.org/):

```shell
poetry add epochalyst
```

## Pytest coverage report

To generate pytest coverage report run

```python
python -m pytest --cov=epochalyst --cov-branch --cov-report=html:coverage_re
```

## Imports

### Caching

For caching some imports are only required, these have to be manually installed when needed

- dask >= 2023.12.0 & dask-expr
- pandas >= 1.3.0
- polars
- pyarrow >= 6.0.0 (Read parquet files)
- annotated-types >= 0.6.0

### Model

There is support for using timm models. To be able to do so the user must manually install timm.
- timm >= 0.9.16

### Augmentation

There is also implementations of augmentations that are not in commonly used packages. Most of these are for time series data but there are implmenetations for CutMix and MixUp for images that can be used in the pipeline. To be able to use these the user must manually install kornia.

- kornia >= 0.7.2

## Documentation

Documentation is generated using [Sphinx](https://www.sphinx-doc.org/en/master/).

To make the documentation, run `make html` with `docs` as the working directory. The documentation can then be found in `docs/_build/html/index.html`.

Here's a short command to make the documentation and open it in the browser:

```shell
cd ./docs/;
./make.bat html; start chrome file://$PWD/_build/html/index.html
cd ../
```
