#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# This is a temporary measure before we have maven central setup
# Assume this script is in the root directory of OpenSearch repository
# https://github.com/opensearch-project/OpenSearch
# $1 is the local repo that needs deployment
# $2 is the version number such as 1.0.0, 2.0.0
# $3 is the version qualifier such as beta1, rc1

if [ -z "$1" ] || [ -z "$2" ]
then
  echo "You must specify parameters 'ACTION VERSION [QUALIFIER]'"
  echo "Example: $0 os 1.0.0"
  echo "Example: $0 js 1.0.0 rc1"
fi

if [ -z "$3" ]
then
    REVISION=$2
else
    REVISION=$2-$3
fi


if [ "$1" == "os" ]
then
    if [ -z "$3" ]
    then
        ./gradlew publishToMavenLocal -Dbuild.snapshot=false --console=plain
    else
        ./gradlew publishToMavenLocal -Dbuild.version_qualifier=$3 -Dbuild.snapshot=false --console=plain
    fi
elif [ "$1" == "cu" ]
then
        ./gradlew publishToMavenLocal -Dopensearch.version=$REVISION -Dbuild.snapshot=false --console=plain
elif [ "$1" == "js" ]
then
   ./gradlew publishToMavenLocal -Dopensearch.version=$REVISION -Dbuild.snapshot=false --console=plain
   ./gradlew assemble -Dopensearch.version=$REVISION -Dbuild.snapshot=false

    echo "Creating ../src/test/resources/job-scheduler ..."
    mkdir -p ../src/test/resources/job-scheduler
    pwd
    echo "Copying ./build/distributions/*.zip to ../src/test/resources/job-scheduler ..."
    ls ./build/distributions/
    cp ./build/distributions/*.zip ../src/test/resources/job-scheduler
    echo "Copied ./build/distributions/*.zip to ../src/test/resources/job-scheduler ..."
    ls ../src/test/resources/job-scheduler
fi
