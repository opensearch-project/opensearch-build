#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to automate the single cluster deployment process of OpenSearch and OpenSearch-Dashboards

set -e

# Source lib
. ../lib/shell/file_management.sh
. ../lib/shell/process_control.sh


ROOT=`dirname $(realpath $0)`; echo $ROOT; cd $ROOT
CURR_DIR=`pwd`

function usage() {
    echo ""
    echo "This script is used to deploy OpenSearch and OpenSearch-Dashboards single node cluster. It downloads the latest artifacts or specified ones per user, extract them, and deploy to the localhost to start the cluster."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v VERSION\t(1.0.0 | 1.0.0-beta1 | etc.) Specify the OpenSearch version number that you are building. This will be used to download the artifacts."
    echo -e "-t TYPE\t(snapshots | releases) Specify the OpenSearch Type of artifacts to use, snapshots or releases."
    echo -e "-a ARCHITECTURE\t(x64 | arm64) Specify the CPU architecture of the artifacts."
    echo -e "-s ENABLE_SECURITY\t(true | false) Specify whether you want to enable security plugin or not."
    echo ""
    echo "Optional arguments:"
    echo -e "-h\tPrint this message."
    echo "--------------------------------------------------------------------------"
}


while getopts ":hv:t:a:s:" arg; do
    case $arg in
        v)
            VERSION=$OPTARG
            ;;
        t)
            TYPE=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
            ;;
        s)
            ENABLE_SECURITY=$OPTARG
            ;;
        h)
            usage
            exit 1
            ;;
        :)
            echo -e "\nERROR: '-${OPTARG}' requires an argument"
            echo "'$0 -h' for usage details of this script"
            exit 1
            ;;
        ?)
            echo -e "\nERROR: Invalid option '-${OPTARG}'"
            echo "'$0 -h' for usage details of this script"
            exit 1
            ;;
    esac
done

# Validate the required parameters to present
if [ -z "$VERSION" ] || [ -z "$TYPE" ] || [ -z "$ARCHITECTURE" ] || [ -z "$ENABLE_SECURITY" ]; then
    echo -e "\nERROR: You must specify '-v VERSION', '-t TYPE', '-a ARCHITECTURE', '-s ENABLE_SECURITY'"
    echo "'$0 -h' for usage details of this script"
    exit 1
else
    echo VERSION:$VERSION TYPE:$TYPE ARCHITECTURE:$ARCHITECTURE ENABLE_SECURITY:$ENABLE_SECURITY
fi

# Setup Work Directory
DIR=`Temp_Folder_Create`
Trap_File_Delete_No_Sigchld $DIR
echo New workspace $DIR


# Create subfolders for both opensearch and dashboards
mkdir -p $DIR/opensearch $DIR/opensearch-dashboards
cp -v opensearch-onetime-setup.sh $DIR/opensearch
cd $DIR

# Download Artifacts
echo -e "\nDownloading Artifacts Now"
OPENSEARCH_URL="https://artifacts.opensearch.org/${TYPE}/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-${ARCHITECTURE}.tar.gz"
DASHBOARDS_URL="https://artifacts.opensearch.org/${TYPE}/bundle/opensearch-dashboards/${VERSION}/opensearch-dashboards-${VERSION}-linux-${ARCHITECTURE}.tar.gz"
echo -e "\t$OPENSEARCH_URL"
echo -e "\t$DASHBOARDS_URL"
curl -s -f $OPENSEARCH_URL -o opensearch.tgz || exit 1
curl -s -f $DASHBOARDS_URL -o opensearch-dashboards.tgz || exit 1
ls $DIR

# Extract Artifacts
echo -e "\nExtract Artifacts Now"
tar -xzf opensearch.tgz -C opensearch/ --strip-components=1
tar -xzf opensearch-dashboards.tgz -C opensearch-dashboards/ --strip-components=1

# Setup OpenSearch
echo -e "\nSetup OpenSearch"
cd $DIR/opensearch && mkdir -p backup_snapshots
./opensearch-onetime-setup.sh
sed -i /^node.max_local_storage_nodes/d ./config/opensearch.yml
# Required for IM
echo "path.repo: [\"$PWD/backup_snapshots\"]" >> config/opensearch.yml
echo "node.name: init-master" >> config/opensearch.yml
echo "cluster.initial_master_nodes: [\"init-master\"]" >> config/opensearch.yml
echo "cluster.name: opensearch-${VERSION}-linux-${ARCHITECTURE}" >> config/opensearch.yml
echo "network.host: 0.0.0.0" >> config/opensearch.yml
echo "plugins.destination.host.deny_list: [\"10.0.0.0/8\", \"127.0.0.1\"]" >> config/opensearch.yml
# Required for SQL
echo "script.context.field.max_compilations_rate: 1000/1m" >> config/opensearch.yml
# Required for Security
echo "plugins.security.unsupported.restapi.allow_securityconfig_modification: true" >> config/opensearch.yml
# Required for PA
echo "webservice-bind-host = 0.0.0.0" >> config/opensearch-performance-analyzer/performance-analyzer.properties
# Security setup
if [ "$ENABLE_SECURITY" == "false" ]
then
    echo -e "\tRemove OpenSearch Security"
    #./bin/opensearch-plugin remove opensearch-security
    echo "plugins.security.disabled: true" >> config/opensearch.yml
fi

# Setup Dashboards
echo -e "\nSetup Dashboards"
cd $DIR/opensearch-dashboards
echo "server.host: 0.0.0.0" >> config/opensearch_dashboards.yml
# Security Setup
if [ "$ENABLE_SECURITY" == "false" ]
then
    echo -e "\tRemove Dashboards Security"
    ./bin/opensearch-dashboards-plugin remove securityDashboards
    sed -i /^opensearch_security/d config/opensearch_dashboards.yml
    sed -i 's/https/http/' config/opensearch_dashboards.yml
fi

# Start OpenSearch
echo -e "\nStart OpenSearch"
cd $DIR/opensearch
Spawn_Process_And_Save_PID "./opensearch-tar-install.sh > opensearch.log 2>&1 &"

# Start Dashboards
echo -e "\nStart Dashboards"
cd $DIR/opensearch-dashboards/bin
Spawn_Process_And_Save_PID "./opensearch-dashboards > opensearch-dashboards.log 2>&1 &"

# Startup Complete so trap the processes
echo -e "\nPlease wait for 40 seconds for everything to startup"
Trap_Wait_Term_Cleanup $DIR



