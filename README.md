# treescape
Accelerate agroforestry for a future worth living.

https://github.com/dokterbob/treescape/assets/22742/a146696b-5f87-4b80-9f2c-fcfa09aa45ae

## License
Treescape is published under a GNU Affero Public License (AGPL).
Other/commercial licensing available upon request.

## Features
* Plant species database, including family and genus, linked to GBIF Backbone Taxonomy.
* Included extendable list of ~500 species relevant for agroforestry.
* Automatic data enrichment based on Open Data from external sources.
* Django Admin for browsing species database.

## Roadmap
* Extensive species data (growth habits, climate zones, human uses, ecological roles) based on LLM-processed Wikipedia and other data.
* Extensive API with HTML frontend based on Django Rest Framework.
* Plant placement (design & inventory).
* QGIS and QField integration for design & inventory.

## Requirements
* [Python](https://www.python.org/downloads/) 3.10
* [Poetry](https://python-poetry.org/) 1.7.1

## Getting started
1. Setup virtual environment and install Python dependencies: `poetry install`
2. Activate virtual environment: `poetry shell`
3. Create database: `./manage.py migrate`
4. Create Django superuser: `./manage.py createsuperuser`
5. Login to Django Admin: `http://localhost:8080/admin/`

## Loading species data
A list of ~500 species relevant to agroforestry is provided, data for which is automatically loaded from various sources (currently GBIF and Wikipedia, soon: more).

`./manage.py load_species`

