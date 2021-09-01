#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, ignored."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}

while getopts ":h:v:s:o:a:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
            ;;
        s)
            SNAPSHOT=$OPTARG
            ;;
        o)
            OUTPUT=$OPTARG
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

[[ "$SNAPSHOT" == "true" ]] && VERSION=$VERSION-SNAPSHOT
[ -z "$OUTPUT" ] && OUTPUT=artifacts

# see https://github.com/opensearch-project/security/pull/1409
PLUGIN_VERSION=$(cat plugin-descriptor.properties | grep ^version= | cut -d= -f2 | sed "s/-SNAPSHOT//")
[[ "$SNAPSHOT" == "true" ]] && PLUGIN_VERSION=$PLUGIN_VERSION-SNAPSHOT

sed -i "s/\(^opensearch\.version=\).*\$/\1${VERSION}/" plugin-descriptor.properties
sed -i "s/\(^version=\).*\$/\1${PLUGIN_VERSION}/" plugin-descriptor.properties
sed -i "s/\(<opensearch.version>\).*\(<\/opensearch.version>\)/\1${VERSION}\2/g" pom.xml
sed -i -e "1,/<version>/s/\(<version>\).*\(<\/version>\)/\1${PLUGIN_VERSION}\2/g" pom.xml

mvn -B clean package -Padvanced -DskipTests
artifact_zip=$(ls $(pwd)/target/releases/opensearch-security-*.zip | grep -v admin-standalone)
./gradlew assemble --no-daemon -ParchivePath=$artifact_zip -Dopensearch.version=$VERSION -Dbuild.snapshot=$SNAPSHOT

mkdir -p $OUTPUT/plugins
cp $artifact_zip $OUTPUT/plugins
