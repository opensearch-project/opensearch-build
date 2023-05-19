#!/bin/bash

# Copyright OpenSearch Contributors
###### Information ############################################################################
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Name:          publish-snapshot.sh
# Language:      Shell
#
# About:         Deploy opensearch artifacts to a sonatype snapshot repository.
#                This script will search POM files under the passed in directory and publish artifacts to
#                a snapshot repository using the mvn deploy plugin.
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
  echo "                   /maven/reindex-client/1.0.0-SNAPSHOT/reindex-client-1.0.0-SNAPSHOT.jar"
  echo "  -h      display help"
  echo "Required environment variables:"
  echo "SONATYPE_USERNAME - username with publish rights to a sonatype repository"
  echo "SONATYPE_PASSWORD - password for sonatype"
  echo "SNAPSHOT_REPO_URL - repository URL ex. http://localhost:8081/nexus/content/repositories/snapshots/"
  exit 1
}

while getopts ":h" option; do
  case $option in
  h)
    usage
    ;;
  \?)
    echo "Invalid option -$OPTARG" >&2
    usage
    ;;
  esac
done

[ -z "${SONATYPE_USERNAME}" ] && {
  echo "SONATYPE_USERNAME is required"
  exit 1
}

[ -z "${SONATYPE_PASSWORD}" ] && {
  echo "SONATYPE_PASSWORD is required"
  exit 1
}

[ -z "${SNAPSHOT_REPO_URL}" ] && {
  echo "REPO_URL is required"
  exit 1
}

if [ ! -d "$1" ]; then
  echo "Invalid directory $1 does not exist"
  usage
fi

create_maven_settings() {
  # Create a settings.xml file with the user+password for maven
  mvn_settings="${workdir}/mvn-settings.xml"
  cat >${mvn_settings} <<-EOF
<?xml version="1.0" encoding="UTF-8" ?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                            http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <servers>
    <server>
      <id>nexus</id>
      <username>${SONATYPE_USERNAME}</username>
      <password>${SONATYPE_PASSWORD}</password>
    </server>
  </servers>
</settings>
EOF
}

url="${SNAPSHOT_REPO_URL}"
workdir=$(mktemp -d)

function cleanup() {
  rm -rf "${workdir}"
}

trap cleanup TERM INT EXIT

create_maven_settings

cd "$1"

echo "searching for poms under $PWD"

pomFiles="$(find "." -name '*.pom')"
if [ -z "${pomFiles}" ]; then
  echo "No artifacts found under $PWD"
  exit 1
fi

for pom in ${pomFiles}; do
  pom_dir="$(dirname "${pom}")"
  for FILE in "${pom_dir}"/*; do
    # The POM is deployed with the artifact in a single deploy-file command, we can skip over it
    if [[ $FILE != $pom ]] &&
       [[ $FILE != *"test-fixtures"* ]] && # This is a hack to ensure the OpenSearch build-tools test fixture jar is not uploaded instead of the actual build-tools jar.
       [[ $FILE != *"javadoc"* ]] &&
       [[ $FILE != *"sources"* ]]; then
      extension="${FILE##*.}"
      case $extension in jar | war | zip)
          echo "Uploading: ${FILE} with ${pom} to ${url}"
          mvn --settings="${mvn_settings}" deploy:deploy-file \
            -DgeneratePom=false \
            -DrepositoryId=nexus \
            -Durl="${SNAPSHOT_REPO_URL}" \
            -DpomFile="${pom}" \
            -Dfile="${FILE}" || echo "Failed to upload ${FILE}"
        ;;
      *) echo "Skipping upload for ${FILE}" ;;
      esac
    fi
  done

  echo "Finished uploading ${pom_dir}"
done

echo "==========================================="
echo "Done."
echo "==========================================="
