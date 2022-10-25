#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

export OPENSEARCH_HOME=`dirname $(realpath $0)`
export OPENSEARCH_PATH_CONF=$OPENSEARCH_HOME/config
cd $OPENSEARCH_HOME

KNN_LIB_DIR=$OPENSEARCH_HOME/plugins/opensearch-knn/lib
##Security Plugin
bash $OPENSEARCH_HOME/plugins/opensearch-security/tools/install_demo_configuration.sh -y -i -s

echo "done security"
PA_AGENT_JAVA_OPTS="-Dlog4j.configurationFile=$OPENSEARCH_PATH_CONF/opensearch-performance-analyzer/log4j2.xml \
              -Xms64M -Xmx64M -XX:+UseSerialGC -XX:CICompilerCount=1 -XX:-TieredCompilation -XX:InitialCodeCacheSize=4096 \
              -XX:MaxRAM=400m"

OPENSEARCH_MAIN_CLASS="org.opensearch.performanceanalyzer.PerformanceAnalyzerApp" \
OPENSEARCH_ADDITIONAL_CLASSPATH_DIRECTORIES=plugins/opensearch-performance-analyzer \
OPENSEARCH_JAVA_OPTS=$PA_AGENT_JAVA_OPTS

if ! grep -q '## OpenSearch Performance Analyzer' $OPENSEARCH_PATH_CONF/jvm.options; then
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> $OPENSEARCH_PATH_CONF/jvm.options
   echo '## OpenSearch Performance Analyzer' >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "-Djava.security.policy=$OPENSEARCH_PATH_CONF/opensearch-performance-analyzer/opensearch_security.policy" >> $OPENSEARCH_PATH_CONF/jvm.options
   echo "--add-opens=jdk.attach/sun.tools.attach=ALL-UNNAMED" >> $OPENSEARCH_PATH_CONF/jvm.options
fi
echo "done plugins"

##Set KNN Dylib Path for macOS and *nix systems
if echo "$OSTYPE" | grep -qi "darwin"; then
    if echo "$JAVA_LIBRARY_PATH" | grep -q "$KNN_LIB_DIR"; then
        echo "k-NN libraries found in JAVA_LIBRARY_PATH"
    else
        export JAVA_LIBRARY_PATH=$JAVA_LIBRARY_PATH:$KNN_LIB_DIR
        echo "k-NN libraries not found in JAVA_LIBRARY_PATH. Updating path to: $JAVA_LIBRARY_PATH." 
    fi
else
    if echo "$LD_LIBRARY_PATH" | grep -q "$KNN_LIB_DIR"; then
        echo "k-NN libraries found in LD_LIBRARY_PATH"
    else
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$KNN_LIB_DIR
        echo "k-NN libraries not found in LD_LIBRARY_PATH. Updating path to: $LD_LIBRARY_PATH."
    fi
fi

##Start OpenSearch
echo "Starting OpenSearch"
exec $OPENSEARCH_HOME/bin/opensearch "$@"
