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
    echo -e "-p PRODUCT\tSpecify the product, e.g. opensearch or opensearch-dashboards, make sure this is the name of your .tgz defined in dockerfile."
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

if [ -z "$VERSION" ] || [ -z "$DOCKERFILE" ] || [ -z "$PRODUCT" ]; then
    echo "You must specify '-v VERSION', '-f DOCKERFILE', '-p PRODUCT'"
    usage
    exit 1
fi

echo $DOCKERFILE

DIR=`mktemp -d`

echo "Creating Docker workspace in $DIR"
trap '{ echo Removing Docker workspace in "$DIR"; rm -rf -- "$DIR"; }' TERM INT EXIT

if [ -z "$TARBALL" ]; then
    # No tarball file specified so download one
    URL="https://artifacts.opensearch.org/releases/bundle/${PRODUCT}/${VERSION}/${PRODUCT}-${VERSION}-linux-x64.tar.gz"
    echo "Downloading ${PRODUCT} version ${VERSION} from ${URL}"
    curl -f $URL -o $DIR/$PRODUCT.tgz || exit 1
    ls -l $DIR
else
    cp -v $TARBALL $DIR/$PRODUCT.tgz
fi

cp -v ${PRODUCT}-config/* $DIR/

docker build --build-arg VERSION=$VERSION --build-arg BUILD_DATE=`date -u +%Y-%m-%dT%H:%M:%SZ` -f $DOCKERFILE $DIR -t opensearchproject/$PRODUCT:$VERSION

rm -rf $DIR
