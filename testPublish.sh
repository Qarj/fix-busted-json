#! /bin/bash

# Uses different credentials to publish to TestPyPI for testing purposes.
# Ensure you have a .pypirc file with a [testpypi] section configured,
# or set TWINE_USERNAME and TWINE_PASSWORD environment variables accordingly.

python -m twine upload --repository testpypi dist/*
