#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to automate the docker multi arch image creation process

set -e

# Import libs
. ../../lib/shell/file_management.sh

# Variable
OLDIFS=$IFS
BUILDER_NUM=`date +%s`
BUILDER_NAME="multiarch_${BUILDER_NUM}"
DIR=""

function usage() {
    echo ""
    echo "This script is used to build the Docker image with multi architecture (x64 + arm64). It prepares the files required by the Dockerfile in a temporary directory, then builds and tags the Docker image."
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

function cleanup_docker_buildx() {
    # Cleanup docker buildx
    echo -e "\n* Cleanup docker buildx"
    docker buildx use default
    docker buildx rm $BUILDER_NAME > /dev/null 2>&1
}

function cleanup_all() {
    cleanup_docker_buildx
    File_Delete $DIR
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

# Warning docker desktop
if (! docker buildx version)
then
    echo -e "\n* You MUST have Docker Desktop to use buildx for multi-arch images."
    exit 1
fi

# Prepare docker buildx
trap cleanup_all TERM INT EXIT
DIR=`Temp_Folder_Create`
echo New workspace $DIR
echo -e "\n* Prepare docker buildx"
docker buildx use default
docker buildx create --name $BUILDER_NAME --use
docker buildx inspect --bootstrap

# Check buildx status
echo -e "\n* Check buildx status"
docker buildx ls | grep $BUILDER_NAME
docker ps | grep $BUILDER_NAME

# Build multi-arch images
docker buildx build --platform linux/amd64,linux/arm64 -t opensearchstaging/ci-runner:${TAG_NAME} -f $DOCKERFILE --push .

