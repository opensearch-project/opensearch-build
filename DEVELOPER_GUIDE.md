- [Developer Guide](#developer-guide)
  - [Forking and Cloning](#forking-and-cloning)
  - [Install Prerequisites](#install-prerequisites)
    - [Pyenv](#pyenv)
    - [Python 3.7](#python-37)
    - [Pipenv](#pipenv)
  - [Install Dependencies](#install-dependencies)
  - [Run Tests](#run-tests)
  - [Run bundle-workflow](#run-bundle-workflow)
  - [Code Linting](#code-linting)

## Developer Guide

### Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.

### Install Prerequisites

#### Pyenv

Use pyenv to manage multiple versions of Python. This can be easily installed with [pyenv-installer](https://github.com/pyenv/pyenv-installer).

#### Python 3.7

Python projects in this repository, including the [bundle-workflow](./bundle-workflow) project, use Python 3.7. See the [Python Beginners Guide](https://wiki.python.org/moin/BeginnersGuide) if you have never worked with the language. 

```
$ python3 --version
Python 3.7.11
```

If you are using pyenv.

```
$ pyenv install 3.7.11
```

#### Pipenv

This project uses [pipenv](https://pipenv.pypa.io/en/latest/), which is typically installed with `pip install --user pipenv`. Pipenv automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your `Pipfile` as you install/uninstall packages. It also generates the ever-important `Pipfile.lock`, which is used to produce deterministic builds.

```
$ pipenv --version
pipenv, version 19.0
```

### Install Dependencies

Install dependencies. 

```
cd bundle-workflow
~/.../bundle-workflow $ pipenv install
Installing dependencies from Pipfile.lock (1f4869)...
 🐍  ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run. 
```

### Run Tests

This project uses [pytest](https://docs.pytest.org/en/6.x/) to ensure code quality. See [bundle-workflow/tests](bundle-workflow).

```
~/.../bundle-workflow $ pipenv run pytest
2 passed in 02s
```

### Run bundle-workflow

Try running `./build.sh` from [bundle-workflow](./bundle-workflow). It should complete and show usage.

```
$ ./build.sh 
Installing dependencies in . ...
Installing dependencies from Pipfile.lock (41aca1)…
 🐍  ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 14/14 — 00:00:01
To activate this project's virtualenv, run the following:
 $ pipenv shell
Running ./src/build.py ...
usage: build.py [-h] [-s] [-c COMPONENT] [--keep] manifest
build.py: error: the following arguments are required: manifest
```

### Code Linting

This project uses [isort](https://github.com/PyCQA/isort) to ensure that imports are sorted, and [flake8](https://flake8.pycqa.org/en/latest/) to enforce code style. 

```
$ pipenv run flake8
./src/assemble_workflow/bundle_recorder.py:30:13: W503 line break before binary operator
```

Use `isort .` to fix any sorting order.

```
$ pipenv run isort .
Fixing bundle-workflow/tests/system/test_arch.py
```

Use [black](https://black.readthedocs.io/en/stable/) to auto-format your code.

```
$ pipenv run black .
All done! ✨ 🍰 ✨
23 files left unchanged.
```

If your code isn't properly formatted, don't worry, [a CI workflow](./github/workflows/test-bundle-workflow.yml) will make sure to remind you. 