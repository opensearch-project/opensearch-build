#!/bin/bash

###### Information ############################################################################
#  SPDX-License-Identifier: Apache-2.0
#
#  The OpenSearch Contributors require contributions made to
#  this file be licensed under the Apache-2.0 license or a
#  compatible open source license.
#
# Name:          publish-snapshot.sh
# Language:      Shell
#
# About:         Deploy opensearch artifacts to a sonatype snapshot repository.
#                This script will search POM files under the passed in directory.
#                If found, pom, jar, and signature files will be deployed to the org/opensearch namespace.
#
# Prerequisites: The given directory must be the parent directory of org/opensearch artifacts.
#                Environment variables must be set:
#                SONATYPE_ID/SONATYPE_PASSWORD - repository credentials
#                SNAPSHOT_HOST - repository host
#
#
# Usage:         ./publish-snapshot.sh <directory>
#
###############################################################################################
set -e

[ -z "${1:-}" ] && {
  usage
}

usage() {
    echo "usage: $0 [-h] [dir]"
    echo "  dir     parent directory of artifacts to be published to org/opensearch namespace."
    echo "          example: dir = ~/.m2/repository/org/opensearch where dir contains artifacts of a path:"
    echo "                   /plugin/reindex-client/1.0.0-SNAPSHOT/reindex-client-1.0.0-SNAPSHOT.jar"
    echo "  -h      display help"
    echo "Required environment variables:"
    echo "SONATYPE_ID - username with publish rights to a sonatype repository"
    echo "SONATYPE_ID - password for sonatype"
    echo "REPO_URL    - repository URL without path, ex. https://aws.oss.sonatype.org/"
    exit 1
}

while getopts ":h" option; do
  case $option in
    h)
       usage
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
       usage
    ;;
  esac
done

[ -z "${SONATYPE_ID}" ] && {
  echo "SONATYPE_ID is required"
  exit 1
}

[ -z "${SONATYPE_PASSWORD}" ] && {
  echo "SONATYPE_PASSWORD is required"
  exit 1
}

[ -z "${REPO_URL}" ] && {
  echo "REPO_URL is required"
  exit 1
}

if [ ! -d "$1" ]; then
  echo "Invalid directory $1 does not exist"
  usage
fi

snapshot_url="${REPO_URL%/}/nexus/content/repositories/snapshots/org/opensearch"

cd "$1"

# Import Opensearch PUBLIC GPG key
curl -S https://artifacts.opensearch.org/publickeys/opensearch.pgp | gpg --import

echo "searching for poms under $PWD"

pomFiles="$(find "." -name '*.pom')"
if [ -z "${pomFiles}" ]; then
  echo "No artifacts found under $PWD"
  exit 1
fi

artifacts=()
for pom in ${pomFiles}; do
  jar=${pom/.pom/.jar}

  pomsig=${pom/.pom/.pom.asc}
  jarsig=${pom/.pom/.jar.asc}

  if [ -z "${pomsig}" ]; then
    echo "No signature file found for pom, skipping ${jar}..."
    continue
  fi

  if [ -z "${jarsig}" ]; then
    echo "No signature file found for jar, skipping ${jar}..."
    continue
  fi

  echo "Validating signatures for - ${pomsig} and ${jarsig}"

  gpg --verify-files "${pomsig}" "${jarsig}"

  if [ $? -ne 0 ]; then
    echo "Invalid signature on artifact, ${pom}"
    exit 1
  fi
  artifacts+=("${pom}" "${pomsig}" "${jar}" "${jarsig}")
done

echo "==========================================="
echo "Found ${#artifacts[@]} artifacts to upload"
echo "==========================================="

success_count=0
for artifact in "${artifacts[@]}"; do
    response=$(curl -s -w "%{http_code}" -v -u "${SONATYPE_ID}":"${SONATYPE_PASSWORD}" --upload-file "${artifact}" "$snapshot_url${artifact}")
    http_code=$(tail -n1 <<< "$response")
    if [[ "${http_code}" != 2* ]]; then
     echo "Failed to upload ${artifact}"
     continue;
    fi
    ((success_count++))
done

echo "==========================================="
echo "Finished deploying ${success_count} artifacts to $snapshot_url"
echo "==========================================="
