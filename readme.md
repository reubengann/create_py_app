# create_py_app

This package is made to scaffold Python applications.

## Features

- create a folder structure with testing set up
- generate requirements, readme
- initialize git

Optionally will generate

- a main entry point
- argument parsing
- logging
- reading settings from env (using Pydantic)
- fastapi routes
- sqlalchemy models
- job scheduler

and more.

## Installation

Clone the repository or download the zip file. Then

```bash
pip install ./create_py_app.zip
```

## Usage

```bash
create_py_app projectname
```

This will create the project in the subdirectory `projectname`
