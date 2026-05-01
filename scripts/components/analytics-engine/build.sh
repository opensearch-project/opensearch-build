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

../../gradlew assemble -Dbuild.snapshot="$SNAPSHOT" -Dbuild.version_qualifier=$QUALIFIER -Dsandbox.enabled=true -PrustRelease -Pcrypto.standard=FIPS-140-3

[ -z "$OUTPUT" ] && OUTPUT=artifacts
mkdir -p $OUTPUT/plugins
cp -v analytics-engine/build/distributions/analytics-engine-$VERSION.zip $OUTPUT/plugins/
#cp -v analytics-engine/build/distributions/analytics-engine-$VERSION.zip $OUTPUT/plugins/analytics-engine-$VERSION.0.zip

#echo "Building (sandbox) core plugins, save in same dir as core plugins..."
#cd sandbox/plugins
#../../gradlew assemble -Dbuild.snapshot="$SNAPSHOT" -Dbuild.version_qualifier=$QUALIFIER -Dsandbox.enabled=true -PrustRelease -Pcrypto.standard=FIPS-140-3
#cd ../../
#touch ./sandbox-core-plugins.txt
#for plugin in sandbox/plugins/*; do
#  PLUGIN_NAME=$(basename "$plugin")
#  if [ -d "$plugin" ] && [ "examples" != "$PLUGIN_NAME" ]; then
#    PLUGIN_ARTIFACT_BUILD_NAME=`ls "$plugin"/build/distributions/ | grep "$PLUGIN_NAME.*$IDENTIFIER.zip"`
#    cp -v "$plugin"/build/distributions/"$PLUGIN_ARTIFACT_BUILD_NAME" "${OUTPUT}"/core-plugins/"$PLUGIN_ARTIFACT_BUILD_NAME"
#    echo $PLUGIN_ARTIFACT_BUILD_NAME >> ./sandbox-core-plugins.txt
#  fi
#done
#cp -v ./sandbox-core-plugins.txt "${OUTPUT}"/core-plugins/
#
#echo "Both core-plugins and (sandbox) core-plugins are built now"
