#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to automate the opensearch-build consolidated release notes generation

# On darwin and bsd the given grep/sed is lacking functionalities in gnu grep/gnu sed
# Will exit if no ggrep/gsed found on the host

### Variables ###
shopt -s expand_aliases
ROOT=`dirname "$(realpath $0)"`; echo $ROOT
INPUT_MANIFEST=$1
SKIP_ORIG_URLS=$2
ORIG_URLS_TXT="$ROOT/release-notes-orig-urls.txt"
ORIG_URLS_ARRAY=()
RELEASE_NOTE_MD="$ROOT/release-notes-draft.md"
OLD_IFS=$IFS
RELEASENOTES_CATEGORIES="BREAKING,FEATURE#ADD,ENHANCE,BUG FIX,INFRASTRUCTURE,DOCUMENT,MAINT,REFACTOR"

### Pre-steps ###

if echo $OSTYPE | grep -qi darwin || echo $OSTYPE | grep -qi bsd; then
    echo "System is $OSTYPE"

    if ! command -v ggrep > /dev/null; then
        echo "No ggrep found for darwin/bsd system, exit 1"
        exit 1
    fi

    if ! command -v gsed > /dev/null; then
        echo "No gsed found for darwin/bsd system, exit 1"
        exit 1
    fi

    alias grep='ggrep'
    alias sed='gsed'

    echo "Switch grep to ggrep, sed to gsed on macOS / BSD servers"

fi

if ! command -v yq > /dev/null; then
    echo "No yq found on the system, exit 1"
    exit 1
else
    yq_version=`yq --version | grep -Eo 'v[0-9.]+' | cut -d. -f1`
    if [ "$yq_version" != "v4" ]; then
        echo "You must install v4+ version of yq to run this script, exit 1"
        exit 1
    else
        echo "yq verified: $yq_version"
    fi
fi

if [ -z "$INPUT_MANIFEST" ]; then
    echo "User should provide manifest file as the input, e.g. ../../manifests/2.7.0/opensearch-2.7.0.yml, exit 1"
    exit 1
fi

if ! yq -v "$INPUT_MANIFEST" > /dev/null 2>&1; then
    echo "$INPUT_MANIFEST is either not found, or is not a valid yaml file, exit 1"
    exit 1
fi


### Main Steps: Get Links ###

# Get all release notes links for all repos
REPO_NAMES_ARRAY=( `yq -r '.components.[].repository' $INPUT_MANIFEST` )
REPO_REFS_ARRAY=( `yq -r '.components.[].ref' $INPUT_MANIFEST` )
COMPONENT_NAMES_ARRAY=( `yq -r '.components.[].name' $INPUT_MANIFEST` )
BUILD_VERSION=`yq -r '.build.version' $INPUT_MANIFEST`
NOT_FOUND=0


if [ "$SKIP_ORIG_URLS" != 'true' ]; then

    echo -e "\nRetrieve release notes links for all components\n"
    echo -n > $ORIG_URLS_TXT

    for index in "${!REPO_NAMES_ARRAY[@]}"; do
        repo_name=`echo ${REPO_NAMES_ARRAY[$index]} | rev | cut -d/ -f1 | rev | sed 's/.git//g'`
        repo_ref=`echo ${REPO_REFS_ARRAY[$index]} | sed 's/tags\///g'`
        component_name=`echo ${COMPONENT_NAMES_ARRAY[$index]} | tr '[:upper:]' '[:lower:]'`
        component_name_prefix=""
        build_version="$BUILD_VERSION.0"
    
        # OS / OSD core
        if [ "$component_name" = "opensearch" ] || [ "$component_name" = "opensearch-dashboards" ]; then
            build_version=$BUILD_VERSION
            continue
        fi
    
        # OS defaults
        if (echo $INPUT_MANIFEST | grep -q "opensearch-$BUILD_VERSION") && ( ! echo $component_name | grep -q "opensearch-"); then
            component_name_prefix="opensearch-"
        fi
    
        # OSD defaults
        if (echo $INPUT_MANIFEST | grep -q "opensearch-dashboards-$BUILD_VERSION") && [ "$component_name" != "opensearch-dashboards" ]; then
            component_name="opensearch-${repo_name}"
        fi
    
        # OS plugins
        if [ "$component_name" = "opensearch" ]; then
            component_name_prefix=""
        fi
        if [ "$component_name" = "job-scheduler" ]; then
            component_name_prefix="opensearch."
        fi
        if [ "$component_name" = "k-nn" ]; then
            component_name="knn"
        fi
        if [ "$component_name" = "ml-commons" ]; then
            component_name="ml-common"
        fi
        if [ "$component_name" = "opensearch-reports" ]; then
            component_name="opensearch-reporting"
        fi
        if [ "$repo_name" = "opensearch-dashboards-functional-test" ] || [ "$component_name" = "notifications-core" ]; then
            continue
        fi
    
        # OSD plugins
        if [ "$repo_name" = "dashboards-observability" ]; then
            component_name=$repo_name
            if [ "$BUILD_VERSION" = "2.8.0" ]; then
                component_name=${repo_name//dashboards/opensearch}
            fi
        fi
        if [ "$repo_name" = "dashboards-query-workbench" ] || [ "$repo_name" = "index-management-dashboards-plugin" ]; then
            component_name="${repo_name//dashboards/opensearch}"
        fi
        if [ "$repo_name" = "anomaly-detection-dashboards-plugin" ] || [ "$repo_name" = "security-analytics-dashboards-plugin" ]; then
            component_name="opensearch-${repo_name//-plugin/}"
        fi
        if [ "$repo_name" = "index-management-dashboards-plugin" ]; then
            component_name="opensearch-$repo_name"
        fi
    
        release_note_url="https://raw.githubusercontent.com/opensearch-project/$repo_name/$repo_ref/release-notes/$component_name_prefix$component_name.release-notes-$build_version.md" 
    
        if curl --output /dev/null --silent --fail -r 0-0 "$release_note_url"; then
            echo "Release notes found: $release_note_url"
            ORIG_URLS_ARRAY+=("$release_note_url")
        else
            NOT_FOUND=$(( NOT_FOUND + 1 ))
            echo "Release notes NOT found: $release_note_url"
        fi
    
    
    done


    # Results
    if [ "$NOT_FOUND" -eq 0 ]; then
        echo -e "\nRelease Note found for all components"
        echo "Write all linkes to local file: $ORIG_URLS_TXT"
        echo "${ORIG_URLS_ARRAY[@]}" | tr ' ' '\n' > $ORIG_URLS_TXT
    else
        echo -e "\nRelease Note NOT FOUND for $NOT_FOUND components, exit 1"
        exit 1
    fi

else
    echo -e "\nSkip release notes link retrieval and use the existing links in $ORIG_URLS_TXT\n"

fi

### Main Stage: Analyze and Re-order the Release Notes ###

echo -e "Clean up urls in the file\n"
# Removen empty space and newlines here and sort
sed -e 's/^[ \t]*//' -e '/^$/d' $ORIG_URLS_TXT | sort | uniq > $ORIG_URLS_TXT.tweaks
echo -e "Release Notes $BUILD_VERSION\n\n" > $RELEASE_NOTE_MD 

IFS=","
for category in $RELEASENOTES_CATEGORIES; do
    echo $category
    cat_main=`echo $category | cut -d '#' -f 1`
    echo "## $cat_main" >> $RELEASE_NOTE_MD
    echo "" >> $RELEASE_NOTE_MD

    IFS="#"
    cat_temp_complete=0
    for cat_temp in $category; do
        echo $cat_temp
        if [ "$cat_temp_complete" -eq 1 ]; then
            continue
        fi

        while read -r url; do
            if [ "${url::1}" != "#" ]; then
                echo $url
                curl -sSLo $ORIG_URLS_TXT.plugin_temp $url
                cat_temp_num=`grep -ni "### $cat_temp" $ORIG_URLS_TXT.plugin_temp | cut -d: -f1`
                if [ -n "$cat_temp_num" ]; then
                    # Upper Case every word of the line
                    echo -e "\n### `echo $url | cut -d/ -f5 | sed -e 's/\b\(.\)/\u\1/g;s/-Plugin//g'`" >> $RELEASE_NOTE_MD
                    # Upper Case first letter of each line
                    sed -n "$(( cat_temp_num + 1)),/^$/p" $ORIG_URLS_TXT.plugin_temp | sed 's/\w/\u&/' >> $RELEASE_NOTE_MD
                    echo "" >> $RELEASE_NOTE_MD
                    #cat_temp_complete=1
                fi
            fi
        done < $ORIG_URLS_TXT.tweaks

    done
    IFS=","
done


















