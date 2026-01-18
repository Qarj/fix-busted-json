# Publishing to PyPI

These steps assume you have already built the distributions in `dist/` (wheel and sdist).

## Using an API token via environment variables

```sh
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-<your-token-value>"  # e.g., the value of PYTHON_PUB_QARJ from PyPI
cd fix-busted-json
source .venv/bin/activate
python --version
python -m twine upload dist/*
```

## Using ~/.pypirc (preferred method)

```ini
[distutils]
index-servers =
  pypi

[pypi]
username = __token__
password = pypi-<your-token-value>
```

Then:

```sh
cd fix-busted-json
source .venv/bin/activate
python -m twine upload dist/*
```

Notes:

- The username must be `__token__` when using PyPI API tokens.
- Keep your token secure; do not commit it to source control.
- If Twine prompts “Enter your API token:”, you can paste the full token value starting with `pypi-...`.
