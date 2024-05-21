#!/bin/sh -ex

pyright
./manage.py check
./manage.py test
