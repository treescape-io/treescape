# treescape
Accelerate agroforestry for a future worth living.

https://github.com/dokterbob/treescape/assets/22742/a146696b-5f87-4b80-9f2c-fcfa09aa45ae

## License
Treescape is published under a GNU Affero Public License (AGPL).
Other/commercial licensing available upon request.

## Features
### Forest design
* Deep QGIS (desktop)/QField (mobile) integration for forest design.
* Plant placement with extensive species data directly available and editable in QGIS.
* Flexible data model to define arbitrary zoning for forest designs.
* Offline-first approach; Spatilalite as storage backend.

### Species data
* Plant species database, including family and genus, linked to GBIF Backbone Taxonomy and Wikipedia.
* Included extendable list of ~500 species relevant for agroforestry.
* Extended ontology for species data, including climate zones, growth habits, human uses and ecological roles.
* Automated data enrichment using GPT 3.5 based on Wikipedia data.
* Django Admin for browsing species database.
* Minimal REST API to species data.

## Roadmap
* Import existing forest design.
* User-friendly web frontend for plant data and forest designs, consider https://wq.io/.
* Multiple data sources, where high confidence trumps low confidence.
* Input data chunking: large context support.
* Improved JSON validation and automated correction.
* Additional sources of plant data:
  - [USDA Plant Data](https://plants.usda.gov/home/plantProfile?symbol=ABLA), specifically [USDA Plant Guides](https://plants.usda.gov/DocumentLibrary/plantguide/doc/pg_abla.docx).
  - [Trefle](https://trefle.io/) API data (including source traversal).
  - [Perplexity](https://docs.perplexity.ai/docs/model-cards) plus citations.
  - [EU Plant Variety Database](https://ec.europa.eu/food/plant-variety-portal/)
  - [FOREMATIS (Forest Reproductive Material Information System)](https://ec.europa.eu/forematis/)
  - [FRUMATIS (Fruit Reproductive Material Information System)](https://ec.europa.eu/frumatis/)
* Model additional plant data:
  - WRB soil types, including accessible explanations.
  - Bioclimatics (rainfall, temperature, sun hours).
  - Lifetime and production durations.
  - Biotic interactions (plant-plant).
  - Plant reproduction methods.
  - Plant fertilization vectors.
  - Fruiting, planting and other seasonal data.
  - Extended varieties ontology and data.

## Requirements
* [Python](https://www.python.org/downloads/) 3.10
* [Poetry](https://python-poetry.org/) 1.7.1

## Getting started
### Django
The data structure and web-interface are managed as a [Django](https://www.djangoproject.com/) project. All the commands in these instructions are to be executing from within the repository's root.

1. Setup virtual environment and install Python dependencies:
   ```sh
   poetry install
   ```
2. Activate virtual environment:
   ```sh
   poetry shell
   ```
3. Create database:
   ```sh
   ./manage.py migrate
   ```
4. Load species data (see 'Load pre-generated data') or generate it ('Generating species data').
5. Create Django superuser:
   ```sh
   ./manage.py createsuperuser
   ```
6. Start the Django development server:
   ```sh
   ./manage.py runserver
   ```
9. Navigate to http://localhost:8080/admin/ to access the Django Admin.

### QGIS
In the `qgis_project` folder, a `forest_design.qgs` template is maintained, which can be directly opened by QGIS.We attempt to keep the QGIS project in sync, as a template, ready to start forest design.

When opening QGIS, make sure to click 'Enable macros' in the notification to enable UI customizations in QGIS.

## Managing species data
### Load pre-generated data
A pre-generated dataset is maintained for your convenience, which, due to their >2 GB size, are distributed separately. They can be loaded as follows:

1. Ensure the database is fully migrated:
   ```sh
   ./manage.py migrate
   ```
2. Download species data from https://drive.google.com/uc?export=download&id=132foZhPNVBdgbRL_Vva4G2QDRYKpBcDQ

3. Unarchive data (images and fixtures):
   ```sh
   tar xvf plant_species_data.tbz2
   ```
4. Load data:
   ```sh
   ./manage.py loaddata plant_species_data
   ```
5. Optionally, delete fixtures to free disk space:
   ```sh
   rm plant_species_data.tbz2 fixtures/plant_species_data.json
   ```

### Creating species fixture
To archive current species data, yielding `plant_species_data.tar`:

```sh
./manage.py dumpdata plant_species species_data | bzip2 > fixtures/plant_species_data.json.bz2
tar cvf plant_species_data.tar fixtures media
```

## Generating species data
### Load species list
A list of ~500 species relevant to agroforestry is provided, data for which is automatically loaded from various sources (currently GBIF and Wikipedia, soon: more). The command below will add the species, genus and family.

`./manage.py load_species species_list.txt`

Note that loading species is idempotent, meaning that no action is performed trying to load a species twice.

Code for this lives in: `plant_species/enrichment`.
Images are automatically downloaded to `media/plant_species/images`.

Your Pull Requests with additional species are greatly appreciated!

### Enrich species data
Retrieve data from textual sources (currently Wikipedia), process them into structurede data using LLM's:

`./manage.py enrich_species_data`

This requires you to export `OPENAI_API_KEY` in your environment:

`export OPENAI_API_KEY=sk-<xxxxxx>`

