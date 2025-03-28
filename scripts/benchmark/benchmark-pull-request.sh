#!/bin/bash

# Copyright OpenSearch Contributors

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is used in OpenSearch Core repo github actions
# To trigger Jenkins Gradle Check from a PR

# Default values
JENKINS_URL="https://build.ci.opensearch.org"
TRIGGER_TOKEN=""
GITHUB_USER=""
GITHUB_TOKEN=""

while getopts "u:t:p:" opt; do
  case $opt in
    t)
      TRIGGER_TOKEN="$OPTARG"
      ;;
    u)
      GITHUB_USER="$OPTARG"
      ;;
    p)
      GITHUB_TOKEN="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$TRIGGER_TOKEN" ]; then
  echo "Error: TRIGGER_TOKEN is required. Use -t option to provide it."
  exit 1
fi

if [ -z "$GITHUB_USER" ]; then
  echo "Error: GITHUB_USER is required. Use -u option to provide it."
  exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN is required. Use -p option to provide it."
  exit 1
fi

PAYLOAD_JSON="{\"pull_request_number\": \"$PR_NUMBER\", \"repository\": \"$REPOSITORY\", \"baseline_cluster_config\": \"$BASELINE_CLUSTER_CONFIG\", \"DISTRIBUTION_URL\": \"$DISTRIBUTION_URL\", \"DISTRIBUTION_VERSION\": \"$OPENSEARCH_VERSION\", \"SECURITY_ENABLED\": \"$SECURITY_ENABLED\", \"SINGLE_NODE_CLUSTER\": \"$SINGLE_NODE_CLUSTER\", \"MIN_DISTRIBUTION\": \"$MIN_DISTRIBUTION\", \"TEST_WORKLOAD\": \"$TEST_WORKLOAD\", \"MANAGER_NODE_COUNT\": \"$MANAGER_NODE_COUNT\", \"DATA_NODE_COUNT\": \"$DATA_NODE_COUNT\", \"DATA_INSTANCE_TYPE\": \"$DATA_INSTANCE_TYPE\", \"DATA_NODE_STORAGE\": \"$DATA_NODE_STORAGE\", \"JVM_SYS_PROPS\": \"$JVM_SYS_PROPS\", \"ADDITIONAL_CONFIG\": \"$ADDITIONAL_CONFIG\", \"USER_TAGS\": \"$USER_TAGS\", \"WORKLOAD_PARAMS\": $WORKLOAD_PARAMS, \"TEST_PROCEDURE\": \"$TEST_PROCEDURE\", \"EXCLUDE_TASKS\": \"$EXCLUDE_TASKS\", \"INCLUDE_TASKS\": \"$INCLUDE_TASKS\", \"CAPTURE_NODE_STAT\": \"$CAPTURE_NODE_STAT\"}"
echo "Triggering Jenkins workflow"
JENKINS_REQ=`curl -s -XPOST \
     -H "Authorization: Bearer $TRIGGER_TOKEN" \
     -H "Content-Type: application/json" \
     "$JENKINS_URL/generic-webhook-trigger/invoke" \
     --data "$(echo $PAYLOAD_JSON)"`

echo $PAYLOAD_JSON
echo $JENKINS_REQ

QUEUE_URL=$(echo $JENKINS_REQ | jq --raw-output '.jobs."benchmark-pull-request".url')
echo QUEUE_URL $QUEUE_URL

MAX_RETRIES=10
RETRY_INTERVAL=5

for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i: Checking if queue exists in Jenkins"
    if [ -n "$QUEUE_URL" ] && [ "$QUEUE_URL" != "null" ]; then
        WORKFLOW_URL=$(curl -s -XGET ${JENKINS_URL}/${QUEUE_URL}api/json --user ${GITHUB_USER}:${GITHUB_TOKEN}| jq --raw-output .executable.url)
        echo WORKFLOW_URL $WORKFLOW_URL

        if [ -n "$WORKFLOW_URL" ] && [ "$WORKFLOW_URL" != "null" ]; then
            echo "Job is submitted and running"
            echo "Final WORKFLOW_URL: $WORKFLOW_URL"
            echo "WORKFLOW_URL=$WORKFLOW_URL" >> $GITHUB_ENV
            break
        fi
    fi

    if [ $i -eq $MAX_RETRIES ]; then
        echo "Max retries reached. Job may not have started."
        exit 1
    fi

    echo "Job not started yet. Waiting for $RETRY_INTERVAL seconds before next attempt."
    sleep $RETRY_INTERVAL
done
