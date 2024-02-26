# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile

# This image can only by built on a Windows2019 server or higher version

ARG ServerCoreRepo=mcr.microsoft.com/windows

FROM ${ServerCoreRepo}:ltsc2019

USER ContainerAdministrator

COPY config/windows-setup.ps1 ./

RUN powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

RUN powershell ./windows-setup.ps1 

RUN powershell -Command Remove-Item './windows-setup.ps1' -Force

RUN bash.exe -c "curl https://ci.opensearch.org > /dev/null 2>&1 || echo add certificates"

RUN bash.exe -c "curl https://artifacts.opensearch.org > /dev/null 2>&1 || echo add certificates"

WORKDIR "C:/Users/ContainerAdministrator"

CMD ["powershell.exe"]
