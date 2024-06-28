# Project Structure Builder

`project_structure_builder` is a Python package that automatically creates a predefined directory structure for a backend project. This tool helps you quickly set up the necessary folders and `__init__.py` files for a Python project.

## Features

- Creates a `backend` directory with the following subdirectories:
  - `api/controller`
  - `client`
  - `custom_enum`
  - `dao`
  - `db`
  - `dto`
  - `routes`
  - `service`
  - `utils`
  - `vo`

## Installation

You can install the package via pip:

```bash
pip install project_structure_builder

After installing project_structure_builder run the following command:-
create_structure /path/to/desired/location
 
