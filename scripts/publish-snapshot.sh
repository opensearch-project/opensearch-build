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
#                The given directory is intended to be the root directory of a maven repository containing ./org/opensearch artifacts.
#                This script will search POM files under ./org/opensearch.
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
  echo "Usage: ($basename $0) dir"
  exit 1
}

[ -z "${SONATYPE_ID}" ] && {
  echo "SONATYPE_ID is required"
  exit 1
}

[ -z "${SONATYPE_PASSWORD}" ] && {
  echo "SONATYPE_PASSWORD is required"
  exit 1
}

[ -z "${SNAPSHOT_HOST}" ] && {
  echo "SNAPSHOT_HOST is required"
  exit 1
}

snapshot_url="${SNAPSHOT_HOST}/nexus/content/repositories/snapshots/"

# Import Opensearch GPG key
curl -S https://artifacts.opensearch.org/publickeys/opensearch.pgp | gpg --import

cd "$1"
i=0

echo "searching for poms under $PWD"

pomFiles="$(find "./org/opensearch" -name '*.pom')"
if [ -z "${pomFiles}" ]; then
  echo "No artifacts found under $PWD"
  exit 1
fi

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
    echo "Invalid signature on artifacts, skipping ${pom}"
  else
    echo "Uploading artifacts for ${pom}"
  fi

  curl -v -u "${SONATYPE_ID}":"${SONATYPE_PASSWORD}" --upload-file "${pom}" "$snapshot_url${pom}"
  curl -v -u "${SONATYPE_ID}":"${SONATYPE_PASSWORD}" --upload-file "${jar}" "$snapshot_url${jar}"
  curl -v -u "${SONATYPE_ID}":"${SONATYPE_PASSWORD}" --upload-file "${pomsig}" "$snapshot_url${pomsig}"
  curl -v -u "${SONATYPE_ID}":"${SONATYPE_PASSWORD}" --upload-file "${jarsig}" "$snapshot_url${jarsig}"
  ((i++))
done

echo "==========================================="
echo "Finished deploying ${i} projects to $snapshot_url"
echo "==========================================="
