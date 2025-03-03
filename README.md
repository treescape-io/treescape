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
* Use uuid4 as primary keys to facilitate offline editing.
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
### Geospatial requirements
In order to do mapping, we're using geospatial libraries which, annoyingly, have to be installed on your system.

Luckily, there are [Installation Instructions](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/#geospatial-libraries). You might also want to install a spatial database, although the default, Spatialite, _might_ just work out of the box.

### Docker
We're explicitly open to Pull Requests for a docker-compose setup.

### Nix
We're also explicitly open to a PR for a NixOS package.

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
3. Copy `.env.dist` to `.env` and update local settings. At minimum, set `SECRET_KEY`, `DEBUG=True` and `OPENAI_API_KEY`.
4. Create and/or migrate database:
   ```sh
   ./manage.py migrate
   ```
5. Load species data (see 'Load pre-generated data') or generate it ('Generating species data').
6. Create Django superuser:
   ```sh
   ./manage.py createsuperuser
   ```
7. Start the Django development server:
   ```sh
   ./manage.py runserver
   ```
8. Navigate to http://localhost:8000/admin/ to access the Django
   Admin or to http://localhost:8000/api/ to play with the API.

### QGIS
In the `qgis_project` folder, a `forest_design.qgs` template is maintained, which can be directly opened by QGIS.We attempt to keep the QGIS project in sync, as a template, ready to start forest design.

When opening QGIS, make sure to click 'Enable macros' in the notification to enable UI customizations in QGIS.

## Configuration
We're using [django-environ](https://django-environ.readthedocs.io/en/latest/index.html) for configuration, which reads environment variables from a local `.env`, which is not checked into version control -- as to guard secrets and keep differences between environments clear.

The following variables can be defined:
* `DATABASE_URL`: https://django-environ.readthedocs.io/en/latest/api.html#environ.Env.db_url
* `OPENAI_API_KEY`: Required for enrichment.
* `SECRET_KEY`: Used for security cookies etc. [Generate here](https://djecrety.ir/)
* `DEBUG`: Set to `True` for local debugging.

### Authentication Configuration
The API supports OAuth authentication for mobile applications using django-allauth and dj-rest-auth. To set up authentication:

1. First, configure the Site model for OAuth callbacks:
   ```sh
   # Access Django shell
   ./manage.py shell
   
   # In the shell, set up the site
   from django.contrib.sites.models import Site
   site = Site.objects.get(pk=1)
   site.domain = "yourdomain.com"  # Set to your domain or localhost:8000 for testing
   site.name = "Treescape"
   site.save()
   ```

2. Configure OAuth provider(s) in your `.env` file. For example, to use Google OAuth:
   ```
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-secret
   ```

3. To use other providers, add the appropriate provider package to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       "allauth.socialaccount.providers.google",  # Already included by default
       "allauth.socialaccount.providers.microsoft",  # Example additional provider
       "allauth.socialaccount.providers.apple",  # Example additional provider
   ]
   ```

4. Then add provider configuration to SOCIALACCOUNT_PROVIDERS in settings.py:
   ```python
   SOCIALACCOUNT_PROVIDERS = {
       "google": {
           "APP": {
               "client_id": env("GOOGLE_CLIENT_ID", default=""),
               "secret": env("GOOGLE_CLIENT_SECRET", default=""),
           },
       },
       "microsoft": {
           "APP": {
               "client_id": env("MICROSOFT_CLIENT_ID", default=""),
               "secret": env("MICROSOFT_CLIENT_SECRET", default=""),
           },
       },
   }
   ```

Mobile apps can authenticate using the following endpoints:
- `api/v1/auth/` - Token authentication endpoints
- `api/v1/auth/registration/` - Registration endpoints  
- `accounts/` - Social authentication callbacks

### For Frontend/Mobile App Developers

This API uses standard JWT authentication with the following specifics:

1. **Available Authentication Endpoints**:
   - Login: `POST /api/v1/auth/login/`
   - Social auth (e.g., Google): `POST /api/v1/auth/google/`
   - Token refresh: `POST /api/v1/auth/token/refresh/`
   - Logout: `POST /api/v1/auth/logout/`

2. **Authentication Headers**:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

3. **Token Handling**:
   - Access tokens expire after 60 minutes
   - Refresh tokens are valid for 30 days
   - The API uses refresh token rotation for security

For a complete reference on working with the dj-rest-auth and JWT authentication, see:
- [dj-rest-auth documentation](https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html)
- [djangorestframework-simplejwt documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)


## Managing species data
### Load pre-generated data
A pre-generated dataset is maintained for your convenience, which, due to their >5 GB size, are distributed separately. They can be loaded as follows:

1. Ensure the database is fully migrated:
   ```sh
   ./manage.py migrate
   ```
2. Download species data from https://drive.google.com/file/d/1FvZKHtlWXP682dMa1pvhINqdhml5kI_t/view

3. Unarchive data (images and fixtures):
   ```sh
   tar xvf plant_species_data.tar
   ```
4. Load data:
   ```sh
   ./manage.py loaddata plant_species_data
   ```
5. Optionally, delete fixtures to free disk space:
   ```sh
   rm plant_species_data.tar fixtures/plant_species_data.json
   ```

### Creating species fixture
To archive current species data, yielding `plant_species_data.tar`:

```sh
./scripts/export_species_data.sh
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

This requires you to configure `OPENAI_API_KEY` in `.env`.
