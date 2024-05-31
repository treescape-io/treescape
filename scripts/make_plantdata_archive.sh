#!/bin/sh

# Get folder containing this one
PROJECT_PATH=$(cd $(dirname $0); cd ..; pwd -P)

cd $PROJECT_PATH

tar jvf treescape_plantdata.tar fixtures/ media/
