#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to return the latest ci docker images

set -e

function usage() {
    echo ""
    echo "This script is used to return the latest ci docker images (mostly used in distribution build or integtest pipelines)"
    echo "This script will not return any older images, please check 'manifests' directory for those images"
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-p PLATFORM\tSpecify the ci image target platform, e.g. 'rockylinux8(default)', 'centos7', 'ubuntu2004' or 'windows2019-servercore'"
    echo -e "-u USAGE\tSpecify the ci image target usage, e.g. 'opensearch(default)' or 'opensearch-dashboards' or 'systemd-base'"
    echo -e "-t TYPE\tSpecify the usages ci image target type, e.g. 'build(default)' or 'integtest'"
    echo ""
    echo "Optional arguments:"
    echo -e "-h\t\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

while getopts ":hp:u:t:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        p)
            PLATFORM=$OPTARG
            ;;
        u)
            USAGE=$OPTARG
            ;;
        t)
            TYPE=$OPTARG
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
if [ -z "$PLATFORM" ]; then
    PLATFORM="rockylinux8"
fi

if [ -z "$USAGE" ]; then
    USAGE="opensearch"
fi

if [ -z "$TYPE" ]; then
    TYPE="build"
fi

# Run script
crane ls public.ecr.aws/opensearchstaging/ci-runner | grep -Eo '.*v[0-9]' | sort -r | uniq | grep $PLATFORM-$USAGE-$TYPE | sed 's/^/public.ecr.aws\/opensearchstaging\/ci-runner\:/g'
