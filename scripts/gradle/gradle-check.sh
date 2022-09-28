#!/bin/bash

# Copyright OpenSearch Contributors

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is used in OpenSearch Core repo github actions
# To trigger Jenkins Gradle Check from a PR


JENKINS_URL="https://build.ci.opensearch.org"
TIMEPASS=0
TIMEOUT=7200
RESULT="null"
TRIGGER_TOKEN=$1
PR_TITLE_NEW=`echo $pr_title | tr -dc '[:alnum:] ' | tr '[:upper:]' '[:lower:]'`
PAYLOAD_JSON="{\"pr_from_sha\": \"$pr_from_sha\", \"pr_from_clone_url\": \"$pr_from_clone_url\", \"pr_to_clone_url\": \"$pr_to_clone_url\", \"pr_title\": \"$PR_TITLE_NEW\", \"pr_number\": \"$pr_number\"}"

echo "Trigger Jenkins workflows"
JENKINS_REQ=`curl -s -XPOST \
     -H "Authorization: Bearer $TRIGGER_TOKEN" \
     -H "Content-Type: application/json" \
     "$JENKINS_URL/generic-webhook-trigger/invoke" \
     --data "$(echo $PAYLOAD_JSON)"`

echo $PAYLOAD_JSON
echo $JENKINS_REQ

QUEUE_URL=$(echo $JENKINS_REQ | jq --raw-output '.jobs."gradle-check".url')
echo QUEUE_URL $QUEUE_URL
echo "wait for jenkins to start workflow" && sleep 15

echo "Check if queue exist in Jenkins after triggering"
if [ -z "$QUEUE_URL" ] || [ "$QUEUE_URL" != "null" ]; then
    WORKFLOW_URL=$(curl -s -XGET ${JENKINS_URL}/${QUEUE_URL}api/json | jq --raw-output .executable.url)
    echo WORKFLOW_URL $WORKFLOW_URL

    echo "Use queue information to find build number in Jenkins if available"
    if [ -z "$WORKFLOW_URL" ] || [ "$WORKFLOW_URL" != "null" ]; then

        RUNNING="true"

        echo "Waiting for Jenkins to complete the run"
        while [ "$RUNNING" = "true" ] && [ "$TIMEPASS" -le "$TIMEOUT" ]; do
            echo "Still running, wait for another 30 seconds before checking again, max timeout $TIMEOUT"
            echo "Jenkins Workflow Url: $WORKFLOW_URL"
            TIMEPASS=$(( TIMEPASS + 30 )) && echo time pass: $TIMEPASS
            sleep 30
            RUNNING=$(curl -s -XGET ${WORKFLOW_URL}api/json | jq --raw-output .building)
        done

        echo "Complete the run, checking results now......"
        RESULT=$(curl -s -XGET ${WORKFLOW_URL}api/json | jq --raw-output .result)

    fi
fi

echo "Please check jenkins url for logs: $WORKFLOW_URL"

if [ "$RESULT" != "SUCCESS" ]; then
    echo "Result: $RESULT"
    exit 1
else
    echo "Result: $RESULT"
    echo "Get codeCoverage.xml" && curl -SLO ${WORKFLOW_URL}artifact/codeCoverage.xml
    echo 0
fi
