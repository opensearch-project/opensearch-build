- [Developer Guide](#developer-guide)
  - [Forking and Cloning](#forking-and-cloning)
  - [Install Prerequisites](#install-prerequisites)
    - [Pyenv](#pyenv)
    - [Python 3.7](#python-37)
    - [Pipenv](#pipenv)
    - [NVM and Node](#nvm-and-node)
    - [Yarn](#yarn)
    - [Java](#java)
  - [Install Dependencies](#install-dependencies)
  - [Run Tests](#run-tests)
  - [Build OpenSearch](#build-opensearch)
  - [Code Linting](#code-linting)
  - [Type Checking](#type-checking)
  - [Code Coverage](#code-coverage)
  - [Pre-Commit Cheatsheet](#pre-commit-cheatsheet)

## Developer Guide

### Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.

### Install Prerequisites

#### Pyenv

Use pyenv to manage multiple versions of Python. This can be installed with [pyenv-installer](https://github.com/pyenv/pyenv-installer) on Linux and MacOS, and [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) on Windows.

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

#### Python 3.7

Python projects in this repository use Python 3.7. See the [Python Beginners Guide](https://wiki.python.org/moin/BeginnersGuide) if you have never worked with the language.

```
$ python3 --version
Python 3.7.11
```

If you are using pyenv.

```
pyenv install 3.7.12 # use 3.7.9 on Windows, the latest at the time of writing this
pyenv global 3.7.12
```

#### Pipenv

This project uses [pipenv](https://pipenv.pypa.io/en/latest/), which is typically installed with `pip install --user pipenv`. Pipenv automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your `Pipfile` as you install/uninstall packages. It also generates the ever-important `Pipfile.lock`, which is used to produce deterministic builds.

```
$ pip install pipenv

$ pipenv --version
pipenv, version 19.0
```

On Windows, run `pyenv rehash` if `pipenv` cannot be found. This rehashes pyenv shims, creating a `pipenv` file in `/.pyenv/pyenv-win/shims/`.

#### NVM and Node

Install [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) to use the Node 10.24.1 version as it is required

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
nvm install v10.24.1
```

#### Yarn

[Yarn](https://classic.yarnpkg.com/en/docs/install) is required for building and running the OpenSearch Dashboards and plugins

```
npm install -g yarn
```

#### Java

This project recommends Java 11 for Jenkins jobs CI. This means you must have a JDK 11 installed with the environment variable `JAVA_HOME` referencing the path to Java home for your JDK installation, e.g. `JAVA_HOME=/usr/lib/jvm/jdk-11`. Download Java 11 from [here](https://adoptium.net/releases.html?variant=openjdk11).

### Install Dependencies

Install dependencies. 

```
$ pipenv install
Installing dependencies from Pipfile.lock (1f4869)...
 🐍  ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run. 
```

### Run Tests

This project uses [pytest](https://docs.pytest.org/en/6.x/) to ensure Python code quality, and [JUnit](https://junit.org/) for Groovy code. See [tests](tests).

```
$ pipenv run pytest
2 passed in 02s
```

```
$ ./gradlew test

> Task :test
BUILD SUCCESSFUL in 7s
3 actionable tasks: 1 executed, 2 up-to-date
```

### Build OpenSearch

Try running `./build.sh`. It should complete and show usage.

```
$ ./build.sh 
Installing dependencies in . ...
Installing dependencies from Pipfile.lock (41aca1)…
 🐍  ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 14/14 — 00:00:01
To activate this project's virtualenv, run the following:
 $ pipenv shell
Running ./src/run_build.py ...
usage: build.sh [-h] [-s] [-c COMPONENT] [--keep] manifest
build.sh: error: the following arguments are required: manifest
```

### Code Linting

This project uses a [pre-commit hook](https://pre-commit.com/) for linting Python code.

```
$ pipenv run pre-commit install
$ pipenv run pre-commit run --all-files
```
Pre-commit hook will run isort, flake8, mypy and pytest before making a commit.

This project uses [isort](https://github.com/PyCQA/isort) to ensure that imports are sorted, and [flake8](https://flake8.pycqa.org/en/latest/) to enforce code style. 

```
$ pipenv run flake8
./src/assemble_workflow/bundle_recorder.py:30:13: W503 line break before binary operator
```

Use `isort .` to fix any sorting order.

```
$ pipenv run isort .
Fixing tests/system/test_arch.py
```

Use [black](https://black.readthedocs.io/en/stable/) to auto-format your code.

```
$ pipenv run black .
All done! ✨ 🍰 ✨
23 files left unchanged.
```

If your code isn't properly formatted, don't worry, [a CI workflow](./github/workflows/tests.yml) will make sure to remind you. 

### Type Checking

This project uses [mypy](https://github.com/python/mypy) as an optional static type checker.

```
pipenv run mypy .
src/assemble.py:14: error: Cannot find implementation or library stub for module named "assemble_workflow.bundle"
```

### Code Coverage

This project uses [codecov](https://about.codecov.io/) for code coverage. Use `pipenv run codecov` to run codecov locally.

```
$ pipenv run coverage run -m pytest
47 passed in 5.89s

$ pipenv run coverage report
TOTAL 23491 12295 48%
```

### Pre-Commit Cheatsheet

The pre-commit hook checks for imports, type, style and test.

```
pipenv run pre-commit run --all-files
```

Auto-fix format and sort imports by running.

```
git status -s | grep -e "[MA?]\s.*.py" | cut -c4- | xargs pipenv run black
pipenv run isort .
```
