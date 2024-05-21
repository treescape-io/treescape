#!/bin/sh -ex

ruff check
pyright
./manage.py check
./manage.py test
