#!/bin/sh

# Get folder containing this one
PROJECT_PATH=$(cd $(dirname $0); cd ..; pwd -P)

$PROJECT_PATH/manage.py dumpdata --natural-primary --natural-foreign  \
	plant_species species_data | \
	bzip2 > fixtures/plant_species_data.json.bz2
