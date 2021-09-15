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

work_dir=$PWD
mkdir -p $OUTPUT/libs

# Pull library submodule explicitly. While "cmake ." actually pulls the submodule if its not there, we 
# need to pull it before calling cmake. Also, we need to call it from the root git directory.
# Otherwise, the submodule update call may fail on earlier versions of git.
git submodule update --init -- jni/external/nmslib

# Build knnlib and copy it to libs
cd jni

# For x64, generalize arch so library is compatible for processors without simd instruction extensions
if [ "$ARCHITECTURE" = "x64" ]; then 
    sed -i 's/-march=native/-march=x86-64/g' external/nmslib/similarity_search/CMakeLists.txt
fi

cmake .
make

cd $work_dir
cp ./jni/release/libKNNIndexV2_0_11* ./$OUTPUT/libs

./gradlew assemble --no-daemon --refresh-dependencies -DskipTests=true -Dopensearch.version=$VERSION -Dbuild.snapshot=$SNAPSHOT

zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"

echo "COPY ${distributions}/*.zip"
mkdir -p $OUTPUT/plugins
cp ${distributions}/*.zip ./$OUTPUT/plugins
