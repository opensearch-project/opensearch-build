#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

# This script specify the entrypoint startup actions for opensearch
# It will start both opensearch and performance analyzer plugin cli
# If either process failed, the entire docker container will be removed
# in favor of a newly started container

# Export OpenSearch Home
export OPENSEARCH_HOME=/usr/share/opensearch

# Files created by OpenSearch should always be group writable too
umask 0002

if [[ "$(id -u)" == "0" ]]; then
    echo "OpenSearch cannot run as root. Please start your container as another user."
    exit 1
fi

# Parse Docker env vars to customize OpenSearch
#
# e.g. Setting the env var cluster.name=testcluster
#
# will cause OpenSearch to be invoked with -Ecluster.name=testcluster

declare -a opensearch_opts

while IFS='=' read -r envvar_key envvar_value
do
    # OpenSearch settings need to have at least two dot separated lowercase
    # words, e.g. `cluster.name`, except for `processors` which we handle
    # specially
    if [[ "$envvar_key" =~ ^[a-z0-9_]+\.[a-z0-9_]+ || "$envvar_key" == "processors" ]]; then
        if [[ ! -z $envvar_value ]]; then
          opensearch_opt="-E${envvar_key}=${envvar_value}"
          opensearch_opts+=("${opensearch_opt}")
        fi
    fi
done < <(env)

# The virtual file /proc/self/cgroup should list the current cgroup
# membership. For each hierarchy, you can follow the cgroup path from
# this file to the cgroup filesystem (usually /sys/fs/cgroup/) and
# introspect the statistics for the cgroup for the given
# hierarchy. Alas, Docker breaks this by mounting the container
# statistics at the root while leaving the cgroup paths as the actual
# paths. Therefore, OpenSearch provides a mechanism to override
# reading the cgroup path from /proc/self/cgroup and instead uses the
# cgroup path defined the JVM system property
# opensearch.cgroups.hierarchy.override. Therefore, we set this value here so
# that cgroup statistics are available for the container this process
# will run in.
export OPENSEARCH_JAVA_OPTS="-Dopensearch.cgroups.hierarchy.override=/ $OPENSEARCH_JAVA_OPTS"

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

# Start up the opensearch and performance analyzer agent processes.
# When either of them halts, this script exits, or we receive a SIGTERM or SIGINT signal then we want to kill both these processes.

function terminateProcesses {
    if kill -0 $OPENSEARCH_PID >& /dev/null; then
        echo "Killing opensearch process $OPENSEARCH_PID"
        kill -TERM $OPENSEARCH_PID
        wait $OPENSEARCH_PID
    fi
    if kill -0 $PA_PID >& /dev/null; then
        echo "Killing performance analyzer process $PA_PID"
        kill -TERM $PA_PID
        wait $PA_PID
    fi
}

# Enable job control so we receive SIGCHLD when a child process terminates
set -m

# Make sure we terminate the child processes in the event of us received TERM (e.g. "docker container stop"), INT (e.g. ctrl-C), EXIT (this script terminates for an unexpected reason), or CHLD (one of the processes terminated unexpectedly)
trap terminateProcesses TERM INT EXIT CHLD

# Start opensearch
$OPENSEARCH_HOME/bin/opensearch "${opensearch_opts[@]}" &
OPENSEARCH_PID=$!

# Start performance analyzer agent
$OPENSEARCH_HOME/bin/performance-analyzer-agent-cli > $OPENSEARCH_HOME/logs/performance-analyzer.log 2>&1 &
PA_PID=$!

# Wait for the child processes to terminate
wait $OPENSEARCH_PID
echo "OpenSearch exited with code $?"
wait $PA_PID
echo "Performance analyzer exited with code $?"
