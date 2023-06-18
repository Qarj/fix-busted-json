#! /bin/bash

rm -rf dist
rm -rf build
python setup.py sdist bdist_wheel
pip uninstall fix-busted-json -y
pip install -e .
python tests/tests.py
python examples/example_repair_json.py
