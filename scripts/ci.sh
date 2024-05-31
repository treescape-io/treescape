#!/bin/sh -ex
#!/bin/sh

# Get folder containing this one
PROJECT_PATH=$(cd $(dirname $0); cd ..; pwd -P)

cd $PROJECT_PATH
ruff check
pyright
./manage.py check
./manage.py test
