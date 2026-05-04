#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

export OPENSEARCH_HOME=`dirname $(realpath $0)`
export OPENSEARCH_PATH_CONF=$OPENSEARCH_HOME/config
cd $OPENSEARCH_HOME

KNN_LIB_DIR=$OPENSEARCH_HOME/plugins/opensearch-knn/lib
DATAFUSION_LIB_DIR=$OPENSEARCH_HOME/plugins/analytics-backend-datafusion/lib
PARQUET_LIB_DIR=$OPENSEARCH_HOME/plugins/parquet-data-format/lib
##Security Plugin
if [ -d "$OPENSEARCH_HOME/plugins/opensearch-security" ]; then
        echo -e "OpenSearch 2.12.0 onwards, the OpenSearch Security Plugin introduces a change that requires an initial password for 'admin' user. \nPlease define an environment variable 'OPENSEARCH_INITIAL_ADMIN_PASSWORD' with a strong password string. \nIf a password is not provided, the setup will quit. \nFor more details, please visit: https://opensearch.org/docs/latest/install-and-configure/install-opensearch/tar/"
        bash $OPENSEARCH_HOME/plugins/opensearch-security/tools/install_demo_configuration.sh -y -i -s || exit 1
        echo "done security"
fi

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

##Set native library paths for macOS and *nix systems
NATIVE_LIB_DIRS="$KNN_LIB_DIR $DATAFUSION_LIB_DIR $PARQUET_LIB_DIR"

for LIB_DIR in $NATIVE_LIB_DIRS; do
    if [ ! -d "$LIB_DIR" ]; then
        continue
    fi
    if echo "$OSTYPE" | grep -qi "darwin"; then
        if ! echo "$JAVA_LIBRARY_PATH" | grep -q "$LIB_DIR"; then
            export JAVA_LIBRARY_PATH=$JAVA_LIBRARY_PATH:$LIB_DIR
            echo "Added $LIB_DIR to JAVA_LIBRARY_PATH"
        fi
    else
        if ! echo "$LD_LIBRARY_PATH" | grep -q "$LIB_DIR"; then
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIB_DIR
            echo "Added $LIB_DIR to LD_LIBRARY_PATH"
        fi
    fi
done

##Start OpenSearch
echo "Starting OpenSearch"
exec $OPENSEARCH_HOME/bin/opensearch "$@"
