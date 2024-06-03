#!/bin/sh -ex

# Get folder containing this one
PROJECT_PATH=$(cd $(dirname $0); cd ..; pwd -P)

cd $PROJECT_PATH

echo "Getting data out of the DB"
./manage.py dumpdata --natural-primary --natural-foreign  \
	plant_species species_data | \
	bzip2 > fixtures/plant_species_data.json.bz2

echo "Creating a tarball"
tar cvf treescape_plant_species_data.tar fixtures/plant_species_data.json.bz2 media/plant_species
