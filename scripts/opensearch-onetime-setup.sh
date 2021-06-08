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


# This script performs one-time setup for the OpenSearch tarball distribution.
# It installs a demo security config and sets up the performance analyzer

OPENSEARCH_HOME=$1
if [ -z "$OPENSEARCH_HOME" ]
then
  OPENSEARCH_HOME=`dirname $(realpath $0)`; cd $OPENSEARCH_HOME
fi
echo $OPENSEARCH_HOME

##Security Plugin
SECURITY_PLUGIN="opensearch-security"
bash $OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN/tools/install_demo_configuration.sh -y -i -s

##Perf Plugin
PA_PLUGIN="opensearch-performance-analyzer"
chmod 755 $OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_bin/performance-analyzer-agent
chmod -R 755 /dev/shm
chmod 755 $OPENSEARCH_HOME/bin/performance-analyzer-agent-cli

if ! grep -q '## OpenDistro Performance Analyzer' $OPENSEARCH_HOME/config/jvm.options; then
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> $OPENSEARCH_HOME/config/jvm.options
   echo '## OpenDistro Performance Analyzer' >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djava.security.policy=$OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_config/opensearch_security.policy" >> $OPENSEARCH_HOME/config/jvm.options
fi

