#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to automate the docker single arch image creation process

set -e

function usage() {
    echo ""
    echo "This script is used to build the OpenSearch Docker image with single architecture (x64 or arm64). It prepares the files required by the Dockerfile in a temporary directory, then builds and tags the Docker image."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v TAG_NAME\tSpecify the image tag name such as 'centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211019'"
    echo -e "-f DOCKERFILE\tSpecify the dockerfile full path, e.g. dockerfile/opensearch.al2.dockerfile."
    echo ""
    echo "Optional arguments:"
    echo -e "-h\t\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

while getopts ":hv:f:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            TAG_NAME=$OPTARG
            ;;
        f)
            DOCKERFILE=$OPTARG
            ;;
        :)
            echo "-${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

# Validate the required parameters to present
if [ -z "$TAG_NAME" ] || [ -z "$DOCKERFILE" ]; then
  echo "You must specify '-v TAG_NAME', '-f DOCKERFILE'"
  usage
  exit 1
else
  echo $TAG_NAME $DOCKERFILE
fi

# Docker build
docker build -f $DOCKERFILE $DIR -t opensearchstaging/ci-runner:$TAG_NAME .

