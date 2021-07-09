#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# This script is to automate the docker image creation process of OpenSearch and OpenSearch-Dashboards

set -e

function usage() {
    echo ""
    echo "This script is used to build the OpenSearch Docker image. It prepares the files required by the Dockerfile in a temporary directory, then builds and tags the Docker image."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v VERSION\tSpecify the OpenSearch version number that you are building, e.g. '1.0.0' or '1.0.0-beta1'. This will be used to label the Docker image. If you do not use the '-o' option then this tool will download a public OPENSEARCH release matching this version."
    echo -e "-f DOCKERFILE\tSpecify the dockerfile full path, e.g. dockerfile/opensearch.al2.dockerfile."
    echo -e "-p PRODUCT\tSpecify the product, e.g. opensearch or opensearch-dashboards, make sure this is the name of your config folder and the name of your .tgz defined in dockerfile."
    echo ""
    echo "Optional arguments:"
    echo -e "-o FILENAME\tSpecify a local OPENSEARCH tarball. You still need to specify the version - this tool does not attempt to parse the filename."
    echo -e "-h\t\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

while getopts ":ho:v:f:p:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        o)
            TARBALL=`realpath $OPTARG`
            ;;
        v)
            VERSION=$OPTARG
            ;;
        f)
            DOCKERFILE=$OPTARG
            ;;
        p)
            PRODUCT=$OPTARG
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
if [ -z "$VERSION" ] || [ -z "$DOCKERFILE" ] || [ -z "$PRODUCT" ]; then
  echo "You must specify '-v VERSION', '-f DOCKERFILE', '-p PRODUCT'"
  usage
  exit 1
else
  echo $VERSION $DOCKERFILE $PRODUCT
fi

# Create temp workdirectory
DIR=`mktemp -d`
echo "Creating Docker workspace in $DIR"
trap '{ echo Removing Docker workspace in "$DIR"; rm -rf -- "$DIR"; }' TERM INT EXIT

# Copy configs
cp -v config/${PRODUCT}/* $DIR/
cp -v ../../scripts/opensearch-onetime-setup.sh $DIR/

# Copy TGZ
if [ -z "$TARBALL" ]; then
    # No tarball file specified so download one
    URL="https://artifacts.opensearch.org/releases/bundle/${PRODUCT}/${VERSION}/${PRODUCT}-${VERSION}-linux-x64.tar.gz"
    echo "Downloading ${PRODUCT} version ${VERSION} from ${URL}"
    curl -f $URL -o $DIR/$PRODUCT.tgz || exit 1
    ls -l $DIR
else
    cp -v $TARBALL $DIR/$PRODUCT.tgz
fi

# Docker build
docker build --build-arg VERSION=$VERSION --build-arg BUILD_DATE=`date -u +%Y-%m-%dT%H:%M:%SZ` -f $DOCKERFILE $DIR -t opensearchproject/$PRODUCT:$VERSION
docker tag opensearchproject/$PRODUCT:$VERSION opensearchproject/$PRODUCT:latest

