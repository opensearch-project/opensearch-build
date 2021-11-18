#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is used to generate pkgs by using fpm
# It does not run by itself and required to be executed by `./assemble.sh <builds manifest file> --distribution deb/rpm`
# As of now it only supports building packages correctly on LINUX host for deb/rpm.

set -e

# Setup root
ROOT=`dirname $(realpath $0)`; echo $ROOT; cd $ROOT

function usage() {
    echo ""
    echo "This script is used to build the OpenSearch related packages."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v VERSION\tSpecify the package version number, e.g. 1.1.0"
    echo -e "-t TYPE\t\tSpecify the package type, e.g. deb/rpm."
    echo -e "-p PRODUCT\tSpecify the package product, e.g. opensearch / opensearch_dashboards, etc."
    echo -e "-a ARCHITECTURE\tSpecify the package architecture, e.g. x64 or arm64."
    echo -e "-i INPUT_DIR\tSpecify output directory of the content that fpm can use to generate a pkg."
    echo ""
    echo "Optional arguments:"
    echo -e "-o OUTPUT_DIR\tSpecify output directory of that fpm can use to output the generated pkg. Defaults to \$ROOT if not set specifically."
    echo -e "-n NAME\tSpecify package name, defaults to \$PRODUCT-\$VERSION.\$TYPE."
    echo -e "-h\t\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

while getopts ":hv:t:p:a:i:o:n:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
            ;;
        t)
            TYPE=$OPTARG
            ;;
        p)
            PRODUCT=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
            ;;
        i)
            INPUT_DIR=$OPTARG
            ;;
        o)
            OUTPUT_DIR=$OPTARG
            ;;
        n)
            NAME=$OPTARG
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

# Check parameters
if [ -z "$VERSION" ] || [ -z "$TYPE" ] || [ -z "$PRODUCT" ] || [ -z "$ARCHITECTURE" ] || [ -z "$INPUT_DIR" ]
then
    echo "You must specify '-v VERSION', '-t TYPE', '-p PRODUCT', '-a ARCHITECTURE', '-i INPUT_DIR'"
    exit 1
else
    echo $VERSION $TYPE $PRODUCT $ARCHITECTURE $INPUT_DIR $OUTPUT_DIR $NAME
fi

# Check architecture
if [ "$ARCHITECTURE" = "x64" ]
then
    ARCHITECTURE_ALT_rpm="x86_64"
    ARCHITECTURE_ALT_deb="amd64"
elif [ "$ARCHITECTURE" = "arm64" ]
then
    ARCHITECTURE_ALT_rpm="aarch64"
    ARCHITECTURE_ALT_deb="arm64"
else
    echo "User enter wrong architecture, choose among x64/arm64"
    exit 1
fi

# Check type
if [ "$TYPE" != "deb" ] && [ "$TYPE" != "rpm" ]
then
    echo "User enter wrong pkg type, choose among deb/rpm"
    exit 1
fi

# Check product
if [ "$PRODUCT" != "opensearch" ] && [ "$PRODUCT" != "opensearch_dashboards" ]
then
    echo "User enter wrong product, choose among opensearch/opensearch_dashboards"
    exit 1
fi

if [ -z "$OUTPUT_DIR" ]
then
    OUTPUT_DIR=$ROOT
fi

if [ -z "$NAME" ]
then
    NAME=NAME-$VERSION.TYPE
fi

# Setup directory
DIR=`realpath $INPUT_DIR`
echo "List content in $DIR for $PRODUCT $VERSION"
mkdir -p $DIR/data/
cp -v scripts/systemd-entrypoint $DIR/bin/systemd-entrypoint
ls -l $DIR
ARCHITECTURE_FINAL=`eval echo '$'ARCHITECTURE_ALT_${TYPE}`

fpm --force \
    --verbose \
    --input-type dir \
    --package $OUTPUT_DIR/$NAME \
    --output-type $TYPE \
    --name $PRODUCT \
    --description "$PRODUCT $TYPE $VERSION" \
    --version $VERSION \
    --url https://opensearch.org/ \
    --vendor "OpenSearch" \
    --maintainer "OpenSearch" \
    --license "ASL 2.0" \
    --before-install $ROOT/scripts/pre_install.sh \
    --before-remove $ROOT/scripts/pre_remove.sh \
    --after-install $ROOT/scripts/post_install.sh \
    --after-remove $ROOT/scripts/post_remove.sh \
    --config-files /etc/$PRODUCT/$PRODUCT.yml \
    --template-value product=$PRODUCT \
    --template-value user=$PRODUCT \
    --template-value group=$PRODUCT \
    --template-value homeDir=/usr/share/$PRODUCT \
    --template-value configDir=/etc/$PRODUCT \
    --template-value pluginsDir=/usr/share/$PRODUCT/plugins \
    --template-value dataDir=/var/lib/$PRODUCT \
    --exclude usr/share/$PRODUCT/data \
    --exclude usr/share/$PRODUCT/config \
    --architecture $ARCHITECTURE_FINAL \
    $DIR/=/usr/share/$PRODUCT/ \
    $DIR/config/=/etc/$PRODUCT/ \
    $DIR/data/=/var/lib/$PRODUCT/ \
    $ROOT/service_templates/$PRODUCT/systemd/etc/=/etc/
