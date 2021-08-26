#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a temporary measure before we have maven central setup
# Assume this script is in the root directory of OpenSearch repository for $1=opensearch
# Assume this script is in the root directory of common-utils repository for $1=common-utils
# Assume this script is in the root directory of job-scheduler repository for $1=job-scheduler
#     which itself is a subdirectory of the plugin repository that need to run the integTest for $1=js
#     Example: anomaly-detection (plugin repo root that needs to run integTest)
#                - job-schedular (run $1=js here)
# Assume this script is in the root directory of alerting repository for $1=alerting


# https://github.com/opensearch-project/OpenSearch
# https://github.com/opensearch-project/common-utils
# https://github.com/opensearch-project/job-scheduler
# https://github.com/opensearch-project/alerting
# $1 is the local repo that needs deployment
# $2 is the version number such as 1.0.0, 2.0.0
# $3 is the version qualifier such as beta1, rc1

if [ -z "$1" ] || [ -z "$2" ]
then
  echo "You must specify parameters 'ACTION VERSION [QUALIFIER]'"
  echo "Example OpenSearch Mavenlocal: $0 opensearch 1.0.0"
  echo "Example Job-Scheduler Mavenlocal: $0 job-scheduler 1.0.0"
fi

if [ -z "$3" ]
then
    REVISION=$2
else
    REVISION=$2-$3
fi

echo REVISION $REVISION


if [ "$1" = "opensearch" ]
then
    if [ -z "$3" ]
    then
        ./gradlew publishToMavenLocal -Dbuild.snapshot=false --console=plain
    else
        ./gradlew publishToMavenLocal -Dbuild.version_qualifier=$3 -Dbuild.snapshot=false --console=plain
    fi
elif [ "$1" = "common-utils" ]
then
        ./gradlew publishToMavenLocal -Dopensearch.version=$REVISION -Dbuild.snapshot=false --console=plain
elif [ "$1" = "job-scheduler" ]
then
   ./gradlew publishToMavenLocal -Dopensearch.version=$REVISION -Dbuild.snapshot=false --console=plain
   ./gradlew assemble -Dopensearch.version=$REVISION -Dbuild.snapshot=false

    echo "Creating ../src/test/resources/job-scheduler ..."
    mkdir -p ../src/test/resources/job-scheduler
    pwd
    echo "Copying ./build/distributions/*.zip to ../src/test/resources/job-scheduler ..."
    ls ./build/distributions/
    rm -rf -v ../src/test/resources/job-scheduler/*.zip
    cp -v ./build/distributions/*.zip ../src/test/resources/job-scheduler
    echo "Copied ./build/distributions/*.zip to ../src/test/resources/job-scheduler ..."
    ls ../src/test/resources/job-scheduler
elif [ "$1" = "alerting" ]
then
    ./gradlew :alerting-notification:publishToMavenLocal -Dopensearch.version=$REVISION -Dbuild.snapshot=false --console=plain
fi
