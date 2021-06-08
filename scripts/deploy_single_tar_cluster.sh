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

# This script is to automate the single cluster deployment process of OpenSearch and OpenSearch-Dashboards

set -e
CURR_DIR=`pwd`
ROOT=`dirname $(realpath $0)`; echo $ROOT; cd $ROOT

function usage() {
    echo ""
    echo "This script is used to deploy OpenSearch and OpenSearch-Dashboards single node cluster. It downloads the latest artifacts or specified ones per user, extract them, and deploy to the localhost to start the cluster."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v VERSION\t(1.0.0 | 1.0.0-beta1 | etc.) Specify the OpenSearch version number that you are building. This will be used to download the artifacts."
    echo -e "-t TYPE\t(snapshots | releases) Specify the OpenSearch Type of artifacts to use, snapshots or releases."
    echo ""
    echo "Optional arguments:"
    echo -e "-c \tCleanup Existing deployment only without new deployment."
    echo -e "-s ENABLE_SECURITY\t(true | false) Specify whether you want to enable security plugin or not. Default to true."
    echo -e "-h\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

function cleanup() {
    echo ""
    echo Clean Up
    echo Kill Existing OpenSearch/Dashboards Process
    (kill -9 `ps -ef | grep -i [o]pensearch | awk '{print $2}'` > /dev/null 2>&1) || echo -e "\tClear OpenSearch Process"
    (kill -9 `ps -ef | grep -i [n]ode | awk '{print $2}'` > /dev/null 2>&1) || echo -e "\tClear Dashboards Process"
    (kill -9 `ps -ef | grep -i [p]erformance | awk '{print $2}'` > /dev/null 2>&1) || echo -e "\tClear PerformanceAnalyzer Process"

    echo Check PID List
    (ps -ef | grep -i [o]pensearch) || echo -e "\tNo OpenSearch PIDs"
    (ps -ef | grep -i [n]ode) || echo -e "\tNo Dashboards PIDs"
    (ps -ef | grep -i [p]erformance) || echo -e "\tNo PerformanceAnalyzer PIDs"

    echo Remove Old Deployments
    if [ -z "$TMPDIR" ]
    then
      rm -rf /tmp/*_INTEGTEST_WORKSPACE
    else
      rm -rf $TMPDIR/*_INTEGTEST_WORKSPACE
    fi
}


while getopts ":hct:v:s:" arg; do
    case $arg in
        v)
            VERSION=$OPTARG
            ;;
        c)
            cleanup
	    exit
            ;;
	t)
            TYPE=$OPTARG
	    ;;
        s)
            ENABLE_SECURITY=$OPTARG
            ;;
        h)
            usage
            exit 1
            ;;
        :)
            echo "-${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${OPTARG}"
            exit 1
            ;;
    esac
done

# Validate the required parameters to present
if [ -z "$VERSION" ] || [ -z "$TYPE" ]; then
  echo -e "\nERROR: You must specify '-v VERSION', '-t TYPE'"
  usage
  exit 1
else
  echo VERSION:$VERSION TYPE:$TYPE ENABLE_SECURITY:$ENABLE_SECURITY
fi

# Setup Work Directory
cleanup
DIR=$(mktemp --suffix=_INTEGTEST_WORKSPACE -d)
mkdir -p $DIR/opensearch $DIR/opensearch-dashboards
cp opensearch-onetime-setup.sh $DIR/opensearch
cd $DIR; echo; echo New Deployment: $DIR

# Download Artifacts
echo -e "\nDownloading Artifacts Now"
OPENSEARCH_URL="https://artifacts.opensearch.org/${TYPE}/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz"
DASHBOARDS_URL="https://artifacts.opensearch.org/${TYPE}/bundle/opensearch-dashboards/${VERSION}/opensearch-dashboards-${VERSION}-linux-x64.tar.gz"
echo $OPENSEARCH_URL
echo $DASHBOARDS_URL
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
$ROOT/opensearch-onetime-setup.sh $DIR/opensearch
sed -i /^node.max_local_storage_nodes/d ./config/opensearch.yml
echo "path.repo: [\"$PWD/backup_snapshots\"]" >> config/opensearch.yml
echo "node.name: init-master" >> config/opensearch.yml
echo "cluster.initial_master_nodes: [\"init-master\"]" >> config/opensearch.yml
echo "cluster.name: opensearch-${VERSION}-linux-x64" >> config/opensearch.yml
echo "network.host: 0.0.0.0" >> config/opensearch.yml
echo "plugins.destination.host.deny_list: [\"10.0.0.0/8\", \"127.0.0.1\"]" >> config/opensearch.yml
echo "script.context.field.max_compilations_rate: 1000/1m" >> config/opensearch.yml
echo "webservice-bind-host = 0.0.0.0" >> plugins/opensearch-performance-analyzer/pa_config/performance-analyzer.properties
if [ "$ENABLE_SECURITY" == "false" ]
then
  echo Remove OpenSearch Security
  #./bin/opensearch-plugin remove opensearch-security
  echo "plugins.security.disabled: true" >> config/opensearch.yml
fi

# Start OpenSearch
echo -e "\nStart OpenSearch"
cd $DIR/opensearch
nohup ./opensearch-tar-install.sh > opensearch.log 2>&1 &
sleep 30

# Setup Dashboards
echo -e "\nSetup Dashboards"
cd $DIR/opensearch-dashboards
echo "server.host: 0.0.0.0" >> config/opensearch_dashboards.yml
if [ "$ENABLE_SECURITY" == "false" ]
then
  echo Remove Dashboards Security
  ./bin/opensearch-dashboards-plugin remove security-dashboards
  sed -i /^opensearch_security/d config/opensearch_dashboards.yml
  sed -i 's/https/http/' config/opensearch_dashboards.yml
fi

# Start Dashboards
echo -e "\nStart Dashboards"
cd $DIR/opensearch-dashboards/bin
nohup ./opensearch-dashboards > opensearch-dashboards.log 2>&1 &

# Wait for start
echo -e "\nSleep 30"
sleep 30
echo Security Plugin: $ENABLE_SECURITY
echo Startup OpenSearch/Dashboards Complete



