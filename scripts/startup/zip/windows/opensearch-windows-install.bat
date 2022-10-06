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

:: Start OpenSearch
ECHO Start OpenSearch
IF "%~1" == "" (
    CALL "%OPENSEARCH_HOME%\bin\opensearch.bat"
    ) ELSE (
    CALL "%OPENSEARCH_HOME%\bin\opensearch.bat" "%*"
    )

