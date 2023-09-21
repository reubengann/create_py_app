# {{project_name}}

## Setup

To only run the program

```bash
conda create -n {{project_name}} python=3.11
conda activate {{project_name}}
pip install -r requirements.txt
```

To do development, run

```bash
conda create -n {{project_name}} python=3.11
conda activate {{project_name}}
pip install -r requirements.in
pip install -r requirements-dev.in
```
{% if parse_args %}
## Command line arguments

`cmd1`
Do command 1

`cmd2`
Do command 2
{% endif %}
## Freezing requirements

```bash
python -m piptools compile
```

This will generate requirements.txt with run requirements only (not dev reqs). To update the requirements.txt after it has been built, first check which packages are out of date:

```bash
pip list --outdated
```

Upgrade the packages you want to update, and then run the tests to make sure nothing breaks:

```bash
pip install packagename --upgrade
pip-compile --upgrade-package packagename
```

## Code coverage

`pytest --cov=src test/ --cov-report term-missing`

