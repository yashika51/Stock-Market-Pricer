#!/usr/bin/env bash

set -e


_TARGETS="."

echo '[FORMAT START]'
echo ''
echo 'Running isort first pass...'
python -m isort ${_TARGETS}
echo 'Running autoflake...'
python -m autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive ${_TARGETS}
echo 'Running black...'
# shellcheck disable=SC1001
echo 'Running flake8...'
python -m flake8 ${_TARGETS}
echo 'Running MyPy...'
python -m mypy --warn-unused-configs ${_TARGETS}

echo ''
echo '[FORMAT FINISHED]'
