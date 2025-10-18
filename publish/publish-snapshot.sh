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

usage() {
  echo "usage: $0 [-h] [dir]"
  echo "  dir     parent directory of artifacts to be published to org/opensearch namespace."
  echo "          example: dir = ~/.m2/repository/org/opensearch where dir contains artifacts of a path:"
  echo "                   /maven/reindex-client/1.0.0-SNAPSHOT/reindex-client-1.0.0-SNAPSHOT.jar"
  echo "  -h      display help"
  echo "Environment variables:"
  echo "SONATYPE_USERNAME (Required)     - username with publish rights to a sonatype repository"
  echo "SONATYPE_PASSWORD (Required)     - password for sonatype"
  echo "AWS_ACCESS_KEY_ID (Required)     - aws_access_key_id for AWS account with publish rights to a s3 bucket"
  echo "AWS_SECRET_ACCESS_KEY (Required) - aws_secret_access_key for s3"
  echo "AWS_SESSION_TOKEN (Optional)     - aws_session_token for s3 when assume role"
  echo "SNAPSHOT_REPO_URL (Required)     - repository URL nexus : http://localhost:8081/nexus/content/repositories/snapshots/"
  echo "                                                  aws s3: s3://my-bucket-name/maven/snapshots/"
  exit 1
}

[ -z "${1:-}" ] && {
  usage
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

if [ -z "${SNAPSHOT_REPO_URL}" ]; then
  echo "REPO_URL is required"
  exit 1
else
  if echo $SNAPSHOT_REPO_URL | cut -d: -f1 | grep -q s3; then
    SERVER_ID="s3"
  else
    SERVER_ID="nexus"
  fi
fi

if [ "$SERVER_ID" = "s3" ]; then
  if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required for s3"
    exit 1
  fi
else
  if [ -z "$SONATYPE_USERNAME" ] || [ -z "$SONATYPE_PASSWORD" ]; then
    echo "SONATYPE_USERNAME and SONATYPE_PASSWORD are required for nexus"
    exit 1
  fi
fi

if [ ! -d "$1" ]; then
  echo "Invalid directory $1 does not exist"
  usage
else
  PROJ_DIR=$1
  mkdir -p $PROJ_DIR/.mvn
fi

create_maven_settings() {
  # Create a settings.xml file with the user+password for maven
  mvn_settings="${workdir}/mvn-settings.xml"
  echo "Update $mvn_settings"
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
    <server>
      <id>s3</id>
    </server>
  </servers>
</settings>
EOF
}

create_maven_extension_settings() {
  # Create a extensions.xml file with the user+password for maven
  mvn_extension_settings="$PROJ_DIR/.mvn/extensions.xml"
  echo "Update $mvn_extension_settings"
  cat >${mvn_extension_settings} <<-EOF
<?xml version="1.0" encoding="UTF-8"?>
<extensions>
  <extension>
    <groupId>com.github.seahen</groupId>
    <artifactId>maven-s3-wagon</artifactId>
    <version>1.3.3</version>
  </extension>
</extensions>
EOF
}

url="${SNAPSHOT_REPO_URL}"
workdir=$(mktemp -d)

function cleanup() {
  rm -rf "$workdir"
  rm -rf "$PROJ_DIR/.mvn"
}

trap cleanup TERM INT EXIT

create_maven_settings
create_maven_extension_settings

cd "$PROJ_DIR"

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
    if [[ $FILE != "$pom" ]] &&
       [[ $FILE != *"test-fixtures"* ]] && # This is a hack to ensure the OpenSearch build-tools test fixture jar is not uploaded instead of the actual build-tools jar.
       [[ $FILE != *"javadoc"* ]] &&
       [[ $FILE != *"sources"* ]]; then
      extension="${FILE##*.}"
      case $extension in jar | war | zip)
          echo "Uploading: ${FILE} with ${pom} to ${SERVER_ID} repo ${url}"
          mvn --settings="${mvn_settings}" deploy:deploy-file \
            -DgeneratePom=false \
            -DrepositoryId="${SERVER_ID}" \
            -Durl="${url}" \
            -DpomFile="${pom}" \
            -Dfile="${FILE}" || (echo "Failed to upload ${FILE}" && exit 1)
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
