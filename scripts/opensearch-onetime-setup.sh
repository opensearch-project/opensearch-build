#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# This script performs one-time setup for the OpenSearch tarball distribution.
# It installs a demo security config and sets up the performance analyzer

OPENSEARCH_HOME=`dirname $(realpath $0)`; cd $OPENSEARCH_HOME

##Security Plugin
SECURITY_PLUGIN="opensearch-security"
bash $OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN/tools/install_demo_configuration.sh -y -i -s

##Perf Plugin
PA_PLUGIN="opensearch-performance-analyzer"
chmod 755 $OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_bin/performance-analyzer-agent
chmod 755 $OPENSEARCH_HOME/bin/performance-analyzer-agent-cli

if ! grep -q '## OpenDistro Performance Analyzer' $OPENSEARCH_HOME/config/jvm.options; then
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> $OPENSEARCH_HOME/config/jvm.options
   echo '## OpenDistro Performance Analyzer' >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djava.security.policy=$OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_config/opensearch_security.policy" >> $OPENSEARCH_HOME/config/jvm.options
fi

