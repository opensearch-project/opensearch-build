#!/bin/sh

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Description:
# Post-install script to set up the environment.

set -e
echo start post install

case $1 in
  configure)
    if ! getent group "<%= group %>" >/dev/null; then
      addgroup --quiet --system "<%= group %>"
    fi

    if ! getent passwd "<%= user %>" >/dev/null; then
      adduser --quiet --system --no-create-home --disabled-password \
      --ingroup "<%= group %>" --shell /bin/false "<%= user %>"
    fi
  ;;
  abort-deconfigure|abort-upgrade|abort-remove)
  ;;

  # Setup for RPMs environment
  1|2)
    if ! getent group "<%= group %>" >/dev/null; then
      groupadd -r "<%= group %>"
    fi

    if ! getent passwd "<%= user %>" >/dev/null; then
      useradd -r -g "<%= group %>" -M -s /sbin/nologin \
      -c "service user" "<%= user %>"
    fi
  ;;

  *)
      echo "post install script called with unknown argument \`$1'" >&2
      exit 1
  ;;
esac

chown <%= user %>:<%= group %> <%= dataDir %>
chown <%= user %>:<%= group %> <%= pluginsDir %>

############ Additional System Settings ############
OPENSEARCH_HOME=<%= homeDir %>
OPENSEARCH_DATA_DIR=<%= dataDir %>
OPENSEARCH_CONFIG_DIR=<%= configDir %>
OPENSEARCH_LOG_DIR=<%= logDir %>
PRODUCT=<%= product %>

mkdir -p $OPENSEARCH_HOME/data
mkdir -p $OPENSEARCH_CONFIG_DIR
mkdir -p /var/run/$PRODUCT
mkdir -p $OPENSEARCH_LOG_DIR

############ Additional Plugins Settings ############

function pluginSettings() {
    echo Apply Security Settings
    sh $OPENSEARCH_HOME/plugins/opensearch-security/tools/install_demo_configuration.sh -y -i -s

    echo Apply PerformanceAnalyzer Settings
    echo 'true' > "$OPENSEARCH_HOME"/data/rca_enabled.conf
    echo 'true' > $OPENSEARCH_CONFIG_DIR/performance_analyzer_enabled.conf
    echo 'true' > $OPENSEARCH_CONFIG_DIR/rca_enabled.conf
    chown -R <%= user %>:<%= group %> $OPENSEARCH_HOME
    chown -R <%= user %>:<%= group %> $OPENSEARCH_CONFIG_DIR
    chmod a+rw /tmp
    
    if ! grep -q '## OpenSearch Performance Analyzer' $OPENSEARCH_CONFIG_DIR/jvm.options; then
       echo Add Performance Analyzer settings in $OPENSEARCH_CONFIG_DIR/jvm.options
       CLK_TCK=`/usr/bin/getconf CLK_TCK`
       echo >> $OPENSEARCH_CONFIG_DIR/jvm.options
       echo '## OpenSearch Performance Analyzer' >> $OPENSEARCH_CONFIG_DIR/jvm.options
       echo "-Dclk.tck=$CLK_TCK" >> $OPENSEARCH_CONFIG_DIR/jvm.options
       echo "-Djdk.attach.allowAttachSelf=true" >> $OPENSEARCH_CONFIG_DIR/jvm.options
       echo "-Djava.security.policy=file:///usr/share/opensearch/plugins/opensearch-performance-analyzer/pa_config/opensearch_security.policy" >> $OPENSEARCH_CONFIG_DIR/jvm.options
    fi

    if command -v systemctl > /dev/null; then
        echo '# Enabling OpenSearch performance analyzer to start and stop along with opensearch.service'
        systemctl daemon-reload
        #systemctl enable opensearch-performance-analyzer.service || true
    fi

}

if [ "$PRODUCT" = "opensearch" ]
then
    echo Product is OpenSearch, apply additional settings

    # Redirect Logs
    echo "path.logs: $OPENSEARCH_LOG_DIR" >> $OPENSEARCH_CONFIG_DIR/opensearch.yml

    # Plugin Settings
    pluginSettings || echo plugin settings failed
elif [ "$PRODUCT" = "opensearch-dashboards" ]
then
    echo Product is OpenSearch-Dashboards, apply additional settings

    # Redirect Logs
    echo "logging.dest: $OPENSEARCH_LOG_DIR/opensearch-dashboards.log" >> $OPENSEARCH_CONFIG_DIR/opensearch_dashboards.yml

fi

chown -R <%= user %>:<%= group %> $OPENSEARCH_HOME
chown -R <%= user %>:<%= group %> $OPENSEARCH_DATA_DIR
chown -R <%= user %>:<%= group %> $OPENSEARCH_CONFIG_DIR
chown -R <%= user %>:<%= group %> $OPENSEARCH_LOG_DIR
chown -R <%= user %>:<%= group %> "/var/run/$PRODUCT"
