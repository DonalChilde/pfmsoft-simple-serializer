#!/usr/bin/env bash

# Run from the project directory

# After code changes, and
# before each release at a minimum,
# generate the api files for autodoc.
./.venv/bin/sphinx-apidoc -f -o ./docs/source/documentation/api-generated/ ./src/pfmsoft_simple_serializer/

# build the docs
./.venv/bin/sphinx-build -M html ./docs/source ./docs/build --fail-on-warning
