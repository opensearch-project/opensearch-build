- [Developer Guide](#developer-guide)
  - [Forking and Cloning](#forking-and-cloning)
  - [Build Tools](#build-tools)
    - [Install Prerequisites](#install-prerequisites)
      - [Pyenv](#pyenv)
      - [Python 3.7](#python-37)
      - [Pipenv](#pipenv)
      - [NVM and Node](#nvm-and-node)
      - [Yarn](#yarn)
    - [Install Dependencies](#install-dependencies)
    - [Run Tests](#run-tests)
    - [Build OpenSearch](#build-opensearch)
    - [Code Linting](#code-linting)
    - [Type Checking](#type-checking)
    - [Code Coverage](#code-coverage)
    - [Pre-Commit Cheatsheet](#pre-commit-cheatsheet)
  - [Jenkins Pipelines and Shared Libraries](#jenkins-pipelines-and-shared-libraries)
    - [Install Prerequisites](#install-prerequisites-1)
      - [Java](#java)
    - [Run Tests](#run-tests-1)
      - [Regression Tests](#regression-tests)
      - [Testing in Jenkins](#testing-in-jenkins)
      - [Integ Tests in Jenkins](#integ-tests-in-jenkins)

# Developer Guide

## Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.

## Build Tools

This project contains a collection of tools to build, test and release OpenSearch and OpenSearch Dashboards.

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

Install [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) to use the Node 14.18.2 version as it is required

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
nvm install v14.18.2
```

Add the lines below to the correct profile file (`~/.zshrc`, `~/.bashrc`, etc.).
```
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

#### Yarn

[Yarn](https://classic.yarnpkg.com/en/docs/install) is required for building and running the OpenSearch Dashboards and plugins

```
npm install -g yarn
```

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

This project uses [pytest](https://docs.pytest.org/en/6.x/) to ensure Python code quality. See [tests](tests).

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

This project uses a [pre-commit hook](https://pre-commit.com/) for linting Python code and YAML files.

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

This project uses [yamllint](https://yamllint.readthedocs.io/) to enforce formatting in YAML files.

Use [yamlfix](https://github.com/lyz-code/yamlfix) to auto-format your YAML files.

```
$ git status -s | grep -e "[MA?]\s.*.y[a]*ml" | xargs pipenv run yamlfix 
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

## Jenkins Pipelines and Shared Libraries

This project contains [Jenkins pipelines](jenkins) and [Jenkins shared libraries](src/jenkins) that execute the tools that build OpenSearch and OpenSearch Dashboards.

### Install Prerequisites

#### Java

Use Java 11 for Jenkins jobs CI. This means you must have a JDK 11 installed with the environment variable `JAVA_HOME` referencing the path to Java home for your JDK installation, e.g. `JAVA_HOME=/usr/lib/jvm/jdk-11`. Download Java 11 from [here](https://adoptium.net/releases.html?variant=openjdk11).

### Run Tests

This project uses [JenkinsPipelineUnit](https://github.com/jenkinsci/JenkinsPipelineUnit) to unit test Jenkins pipelines and shared libraries. See [tests/jenkins](tests/jenkins).

```
$ ./gradlew test

> Task :test
BUILD SUCCESSFUL in 7s
3 actionable tasks: 1 executed, 2 up-to-date
```

#### Regression Tests

Jenkins workflow regression tests typically output a .txt file into [tests/jenkins/jobs](tests/jenkins/jobs).
For example, [TestHello.groovy](tests/jenkins/TestHello.groovy) executes [Hello_Jenkinsfile](tests/jenkins/jobs/Hello_Jenkinsfile)
and outputs [Hello_Jenkinsfile.txt](tests/jenkins/jobs/Hello_Jenkinsfile.txt). If the job execution changes, the regression test will fail.

- To update the recorded .txt file run `./gradlew test -info -Ppipeline.stack.write=true` or update its value in [gradle.properties](gradle.properties).

- To run a specific test case, run `./gradlew test -info --tests=TestCaseClassName`

#### Tests for jenkins job
Each jenkins job should have a test case associated with it. 
Eg: [TestSignStandaloneArtifactsJob.groovy](tests/jenkins/TestSignStandaloneArtifactsJob.groovy)
- Save the regression file for the `jenkins-job` in `tests/jenkins/jenkinsjob-regression-files/<job-name>/<job-filename>`
- All tests for jenkins job should extend [BuildPipelineTest.groovy](tests/jenkins/BuildPipelineTest.groovy)
- All tests should have a `setUp()` which is used to set the variables associated with the job
- Add setups for all libraries used in the job using `this.registerLibTester` with appropriate values
(Eg: [TestDataPrepperReleaseArtifacts](tests/jenkins/TestDataPrepperReleaseArtifacts.groovy)) in `setUp()` before `super.setUp()` is called.

#### Tests for jenkins libraries

##### Lib Tester
Each jenkins library should have a lib tester associated with it. Eg: [SignArtifactsLibTester](tests/jenkins/lib-testers/SignArtifactsLibTester.groovy)
- Library tester should extend [LibFunctionTester.groovy](tests/jenkins/LibFunctionTester.groovy)
- implement `void configure(helper, bindings)` method which sets up all the variables used in the library
  - Note: This will not include the variables set using function arguments
- implement `void libFunctionName()`. This function will contain the name of function.
- implement `void parameterInvariantsAssertions()`. This function will contain assertions verifying the type and 
accepted values for the function parameters
- implement `void expectedParametersMatcher()`. This function will match args called in the job to expected values from 
the test

##### Library Test Case
Each jenkins library should have a test case associated with it. Eg: [TestSignArtifacts](tests/jenkins/TestSignArtifacts.groovy) <br>
- Jenkins' library test should extend [BuildPipelineTest.groovy](tests/jenkins/BuildPipelineTest.groovy)
- Create a dummy job such as [Hello_Jenkinsfile](tests/jenkins/jobs/Hello_Jenkinsfile) to call and test the function
  and output [Hello_Jenkinsfile.txt](tests/jenkins/jobs/Hello_Jenkinsfile.txt)
- If using remote libs from [opensearch-build-libraries](https://github.com/opensearch-project/opensearch-build-libraries) repository with tag (ex: 1.0.0), make sure
  both the Jenkins Test file as well as the Jenkins Job file are overriding the libs version with the same tag (ex: 1.0.0), or Jacoco test will fail to generate reports.
  This would happen if defaultVersion in BuildPipelineTest.groovy (default to 'main') have a different HEAD commit id compares to tag commit id you defined to use.
```
super.setUp()
......
helper.registerSharedLibrary(
    library().name('jenkins')
        .defaultVersion('1.0.0')
        .allowOverride(true)
        .implicit(true)
        .targetPath('vars')
        .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
        .build()
)
```

```
lib = library(identifier: 'jenkins@1.0.0', retriever: modernSCM([
    $class: 'GitSCMSource',
    remote: 'https://github.com/opensearch-project/opensearch-build-libraries.git',
]))
```

#### Testing in Jenkins
* [Build_OpenSearch_Dashboards_Jenkinsfile](tests/jenkins/jobs/Build_OpenSearch_Dashboards_Jenkinsfile): is similar to [OpenSearch Dashboards Jenkinsfile](jenkins/opensearch-dashboards/Jenkinsfile) w/o notifications.

Make your code changes in a branch, e.g. `jenkins-changes`, including to any of the above jobs. Create a pipeline in Jenkins with the following settings.

* GitHub Project: `https://github.com/[your username]/opensearch-build/`.
* Pipeline repository URL: `https://github.com/[your username]/opensearch-build`.
* Branch specifier: `refs/heads/jenkins-changes`.
* Script path: `tests/jenkins/jobs/Build_DryRun_Jenkinsfile`

You can now iterate by running the job in Jenkins, examining outputs, and pushing updates to GitHub.

#### Integ Tests in Jenkins
- Opensearch bundle build executes the integration tests for the opensearch as well as plugins. 
- To add integ tests for a new plugin, add the plugin in the latest version [test manifest](manifests/2.0.0/opensearch-2.0.0-test.yml).
- The test execution is triggered by the [integtest.sh](scripts/default/integtest.sh). In case a custom implementation is required, plugin owner can add that script in their own repo and [script_finder](src/paths/script_finder.py) will pick that up over the default script.
