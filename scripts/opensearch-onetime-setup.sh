#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script performs one-time setup for the OpenSearch tarball distribution.
# It installs a demo security config and sets up the performance analyzer

OPENSEARCH_HOME=`dirname $(realpath $0)`; cd $OPENSEARCH_HOME

##Security Plugin
SECURITY_PLUGIN="opensearch-security"
if [ -d "$OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN" ]; then
    if [ "$DISABLE_INSTALL_DEMO_CONFIG" = "true" ]; then
        echo "Disabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
    else
        echo "Enabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
        bash $OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN/tools/install_demo_configuration.sh -y -i -s
    fi

    if [ "$DISABLE_SECURITY_PLUGIN" = "true" ]; then
        echo "Disabling OpenSearch Security Plugin"
        sed -i '/plugins.security.disabled/d' $OPENSEARCH_HOME/config/opensearch.yml
        echo "plugins.security.disabled: true" >> $OPENSEARCH_HOME/config/opensearch.yml
    else
        echo "Enabling OpenSearch Security Plugin"
        sed -i '/plugins.security.disabled/d' $OPENSEARCH_HOME/config/opensearch.yml
    fi
fi

##Perf Plugin
PA_PLUGIN="opensearch-performance-analyzer"

if [ -d $OPENSEARCH_HOME/plugins/$PA_PLUGIN ]; then
    chmod 755 $OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_bin/performance-analyzer-agent
    chmod 755 $OPENSEARCH_HOME/bin/performance-analyzer-agent-cli
fi

if ! grep -q '## OpenDistro Performance Analyzer' $OPENSEARCH_HOME/config/jvm.options; then
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> $OPENSEARCH_HOME/config/jvm.options
   echo '## OpenDistro Performance Analyzer' >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_HOME/config/jvm.options
   echo "-Djava.security.policy=$OPENSEARCH_HOME/plugins/$PA_PLUGIN/pa_config/opensearch_security.policy" >> $OPENSEARCH_HOME/config/jvm.options
fi

