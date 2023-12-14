:: SPDX-License-Identifier: Apache-2.0
:: Copyright OpenSearch Contributors

@echo off

:: Set variables and cd into the location of the batch script
PUSHD "%~dp0"
SET "OPENSEARCH_HOME=%CD%"
SET "OPENSEARCH_PATH_CONF=%OPENSEARCH_HOME%\config"

:: Echo User Inputs
ECHO "OPENSEARCH_HOME: %OPENSEARCH_HOME%"
ECHO "OPENSEARCH_PATH_CONF: %OPENSEARCH_PATH_CONF%"

:: Security Plugin Setups
IF EXIST "%OPENSEARCH_HOME%\plugins\opensearch-security" (
    ECHO "Running Security Plugin Install Demo Configuration"
    ECHO "OpenSearch 2.12.0 onwards, the OpenSearch Security Plugin a change that requires an initial password for 'admin' user."
    ECHO "Please define an environment variable 'OPENSEARCH_INITIAL_ADMIN_PASSWORD' with a strong password string."
    ECHO "If a password is not provided, the setup will quit."
    CALL "%OPENSEARCH_HOME%\plugins\opensearch-security\tools\install_demo_configuration.bat" -y -i -s || exit /b 1
)

:: k-NN Plugin Setups
ECHO "Set KNN Dylib Path for Windows systems"
SET "PATH=%PATH%;%OPENSEARCH_HOME%/plugins/opensearch-knn/lib"

:: Start OpenSearch
ECHO Start OpenSearch
IF "%~1" == "" (
    CALL "%OPENSEARCH_HOME%\bin\opensearch.bat"
    ) ELSE (
    CALL "%OPENSEARCH_HOME%\bin\opensearch.bat" "%*"
    )

