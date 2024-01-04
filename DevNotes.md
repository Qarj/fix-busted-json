# DevNotes

https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-7be9dd5d6dcd
https://builtin.com/data-science/how-to-publish-python-code-pypi

## One time setup

```sh
python -m pip install --user --upgrade setuptools wheel
python -m pip install --user --upgrade twine
.
ERROR: requests 2.23.0 has requirement urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1, but you'll have urllib3 2.0.3 which is incompatible.
```

Create a file named `~/.pypirc` with the following contents:

```sh
code $HOME/.pypirc
```

```txt
[testpypi]
  username = __token__
  password = pypi-Ag...j
[pypi]
  username = __token__
  password = pypi-Ag...w
```

## Generate distribution files

```sh
python setup.py sdist bdist_wheel
```

## Install the package on the local machine

```sh
pip uninstall fix-busted-json
pip install -e .
```

## Upload to TestPyPI

```sh
python -m twine upload --repository testpypi dist/*
.
Uploading distributions to https://test.pypi.org/legacy/
Uploading fix_busted_json-0.0.1-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.9/5.9 kB • 00:00 • ?
Uploading fix-busted-json-0.0.1.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.2/8.2 kB • 00:00 • ?

View at:
https://test.pypi.org/project/fix-busted-json/0.0.1/
```

## Install from TestPyPI

```sh
pip uninstall fix-busted-json -y
pip install -i https://test.pypi.org/simple/ fix-busted-json==0.0.6
```

## Upload to PyPI

```sh
python -m twine upload dist/*
```

## Install from PyPI

```sh
pip uninstall fix-busted-json -y
pip install fix-busted-json
```

## Test

```sh
./test.sh
```

## Publish new version

-   bump version in `setup.py`
-   run `./build.sh`
-   run `./testPublish.sh`
-   run `./publish.sh`
