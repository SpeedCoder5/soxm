# Social Exploit Matrix (SoXM) (soxm)

Social Exploit Matrix with LLMs

## Project Organization

```
.
| .gitattributes         <- be check-in friendly to both Windows and Linux
| .gitignore             <- don't check this stuff in
| activate               <- activate `venv` with `source activate`
| LICENSE                <- currently blank, TODO: include license before public release
| Makefile               <- make venv / build /publish package
| pytest.ini             <- pytest settings
| README.md              <- this readme
| requirements-torch.txt <- pytorch requirements
| requirements.txt       <- venv requirements
| setup.cfg              <- module package config
| setup.py               <- runtime requirements
| test_environment.py    <- verify venv works, run `source activate` first
| tox.ini                <- tox file with settings for running tox; see tox.testrun.org
├── data               <- symlink to ../../data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
├── models             <- Trained and serialized models, model predictions, or model summaries
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   └── soxm           <- python module source code
│       └─ __init__.py <- makes it a python module with a specific version
├── test               <- Pytest test code for use in this project.
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
```

## Python virtual environment (venv) commands

Create the venv

    make venv

to activate the venv:

    source activate

to deactivate the venv:

    deactivate

to clean the venv:

    make clean-all

## Make commands

```{bash}
make help

help      This help
clean     Removes build artifacts
clean-all Remove the virtual environment and build artifacts
venv      Create/update project's virtual environment. To activate, run: source activate.sh
test      Run unit tests
dist      Create python package and run unit tests
publish   Create/publish python package to local pypi repo
```

## Source

[https://github.sandbox-asrcfederal.com/data-science/soxm.git](https://github.sandbox-asrcfederal.com/data-science/soxm.git).


## Debugging

Debuging requires using the python virtual environment (venv) for the project.  The venv must first be created and activated.

## Build and publish the package

Follow these steps to build artifacts such as a wheel and tar, including a `__version__`.  Artifacts will get created in `./dist`.

### 1. Set version

The first step in building the package is to modify the version.  Edit `src/soxm/__init__.py` and set the version to something like:

```{python}
__version__='2022.9.21'
```

### 2. Configure local pypi repo for publishing

Follow these steps to publish the package.  First, per [Nexus repo instructions](https://confluence.avde.net/display/GSWA/AVDE+Nexus+Repository#AVDENexusRepository-PyPi), `~/.pypirc` must be configured with to point to the correct repo in which to publish.

Create `$HOME/.pypirc` with the following contents:

```{text}
[distutils]
index-servers =
    ds-pypi-artifacts

[ds-pypi-artifacts]
repository = https://nexusrepo.avde.net/repository/ds-pypi-artifacts/
username = <your username>
password = <your password>
```

Do not forget to `chmod 600 ~/.pypirc`.

### 3. Build and publish the package

Use make to build and publish the package.

```{bash}
make publish
```

### 4. Verify package publication

Verify twine uploaded the correct package version by browsing and examining the appropriate repository link at the top of this page.

## Shout outs

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Created on 2024-07-29.
