#! /bin/bash

rm -rf dist
rm -rf build
python setup.py sdist bdist_wheel
pip uninstall fix-busted-json -y
pip install -e .
python tests/tests.py
python examples/find.py
python examples/log_jsons.py
python examples/repair_json.py
python examples/to_array.py
python examples/llm.py

