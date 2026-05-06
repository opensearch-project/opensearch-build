#!/bin/bash

#
# Copyright OpenSearch Contributors
#
# SPDX-License-Identifier: Apache-2.0
#

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-q QUALIFIER\t[Optional] Build qualifier."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-p PLATFORM\t[Optional] Platform, ignored."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, ignored."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}

while getopts ":h:v:q:s:o:p:a:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
            ;;
        q)
            QUALIFIER=$OPTARG
            ;;
        s)
            SNAPSHOT=$OPTARG
            ;;
        o)
            OUTPUT=$OPTARG
            ;;
        p)
            PLATFORM=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "Error: You must specify the OpenSearch version"
    usage
    exit 1
fi

[[ ! -z "$QUALIFIER" ]] && VERSION=$VERSION-$QUALIFIER
[[ "$SNAPSHOT" == "true" ]] && VERSION=$VERSION-SNAPSHOT
[ -z "$OUTPUT" ] && OUTPUT=artifacts

pwd

# Setup paths
mkdir -p "${OUTPUT}"
OUTPUT_REAL=`realpath ${OUTPUT}`
echo OUTPUT_REAL $OUTPUT_REAL
mkdir -p "${OUTPUT_REAL}"/plugins
mkdir -p "${OUTPUT_REAL}"/dist/

# Copy arrow as it is needed before analytics-engine
DIR="$(dirname "$0")"
echo $DIR
cd $DIR
cp -v ../../../tar/builds/opensearch/core-plugins/arrow-flight-rpc-$VERSION.zip \
    "${OUTPUT_REAL}"/plugins/0-arrow-flight-rpc-$VERSION.zip || \
cp -v ../../../zip/builds/opensearch/core-plugins/arrow-flight-rpc-$VERSION.zip \
    "${OUTPUT_REAL}"/plugins/0-arrow-flight-rpc-$VERSION.zip

cd -

# Sandbox Plugins
echo "Building sandbox plugins..."
../../gradlew assemble -Dbuild.snapshot="$SNAPSHOT" -Dbuild.version_qualifier=$QUALIFIER -Dsandbox.enabled=true -PrustRelease -Pcrypto.standard=FIPS-140-3
INSTALL_ORDER=1
for plugin in ./*; do
  PLUGIN_NAME=$(basename "$plugin")
  echo $PLUGIN_NAME
  if [ -d "$plugin" ] && [ "builds" != "$PLUGIN_NAME" ]; then
    if [ "$PLUGIN_NAME" = "analytics-engine" ] ||
       [ "$PLUGIN_NAME" = "analytics-backend-datafusion" ] ||
       [ "$PLUGIN_NAME" = "analytics-backend-lucene" ] ||
       [ "$PLUGIN_NAME" = "composite-engine" ] ||
       [ "$PLUGIN_NAME" = "dsl-query-executor" ] ||
       [ "$PLUGIN_NAME" = "parquet-data-format" ]; then
      PLUGIN_ARTIFACT_BUILD_NAME=`ls "$plugin"/build/distributions/ | grep "$PLUGIN_NAME-$VERSION.zip"`
      if [ "$PLUGIN_NAME" = "analytics-engine" ]; then
        PLUGIN_NAME=$INSTALL_ORDER-$PLUGIN_NAME
        INSTALL_ORDER=$((INSTALL_ORDER + 1))
      fi
      cp -v "$plugin"/build/distributions/"$PLUGIN_ARTIFACT_BUILD_NAME" "${OUTPUT_REAL}"/plugins/"$PLUGIN_NAME-$VERSION.zip"
    else
      echo "Ignore $PLUGIN_NAME as it is not in the required list"
    fi
  fi
done

# Rustlib
cd ../
echo "Specifically saving rustlib..."
../gradlew :sandbox:libs:dataformat-native:buildRustLibrary -Dbuild.snapshot="$SNAPSHOT" -Dbuild.version_qualifier=$QUALIFIER -Dsandbox.enabled=true -PrustRelease -Pcrypto.standard=FIPS-140-3
for libext in so dylib dll; do
  cp -v ./libs/dataformat-native/rust/target/release/libopensearch_native."$libext" "${OUTPUT_REAL}"/dist/ || echo "$libext not found"
done

if ! (ls "${OUTPUT_REAL}"/dist/ | grep libopensearch_native); then
  echo "libopensearch_native lib not found, exit 1"
  exit 1
fi
