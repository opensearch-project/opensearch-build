# SPDX-License-Identifier: Apache-2.0
# 
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
# 
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
 
 
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.


# This dockerfile generates an AmazonLinux-based image containing an OpenSearch-Dashboards installation.
# It assumes that the working directory contains four files: an OpenSearch-Dashboards tarball (opensearch-dashboards.tgz), opensearch_dashboards.yml, opensearch-dashboards-docker-entrypoint.sh, and example certs.
# Build arguments:
#   VERSION: Required. Used to label the image.
#   BUILD_DATE: Required. Used to label the image. Should be in the form 'yyyy-mm-ddThh:mm:ssZ', i.e. a date-time from https://tools.ietf.org/html/rfc3339. The timestamp must be in UTC.
#   UID: Optional. Specify the opensearch-dashboards userid. Defaults to 1000.
#   GID: Optional. Specify the opensearch-dashboards groupid. Defaults to 1000.
#   OPENSEARCH_DASHBOARDS_HOME: Optional. Specify the opensearch-dashboards root directory. Defaults to /usr/share/opensearch-dashboards.

########################### Stage 0 ########################
FROM amazonlinux:2 AS linux_stage_0

ARG UID=1000
ARG GID=1000
ARG OPENSEARCH_DASHBOARDS_HOME=/usr/share/opensearch-dashboards

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball, and shadow-utils to give us `groupadd` and `useradd`.
# Install which to allow running of securityadmin.sh
RUN yum update -y && yum install -y tar gzip shadow-utils which && yum clean all

# Create an opensearch-dashboards user, group, and directory
RUN groupadd -g $GID opensearch-dashboards && \
    adduser -u $UID -g $GID -d $OPENSEARCH_DASHBOARDS_HOME opensearch-dashboards && \
    mkdir /tmp/opensearch-dashboards

# Prepare working directory
COPY opensearch-dashboards-*.tgz /tmp/opensearch-dashboards/
RUN tar -xzpf /tmp/opensearch-dashboards/opensearch-dashboards-`uname -p`.tgz -C $OPENSEARCH_DASHBOARDS_HOME --strip-components=1 && rm -rf /tmp/opensearch-dashboards
COPY opensearch-dashboards-docker-entrypoint.sh $OPENSEARCH_DASHBOARDS_HOME/
COPY opensearch_dashboards.yml opensearch.example.org.* $OPENSEARCH_DASHBOARDS_HOME/config/

########################### Stage 1 ########################
# Copy working directory to the actual release docker images
FROM amazonlinux:2

ARG UID=1000
ARG GID=1000
ARG OPENSEARCH_DASHBOARDS_HOME=/usr/share/opensearch-dashboards

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball, and shadow-utils to give us `groupadd` and `useradd`.
# Install which to allow running of securityadmin.sh
RUN yum update -y && yum install -y tar gzip shadow-utils which && yum clean all

# Install notebooks dependencies
RUN yum install -y libnss3.so xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Create an opensearch-dashboards user, group
RUN groupadd -g $GID opensearch-dashboards && \
    adduser -u $UID -g $GID -d $OPENSEARCH_DASHBOARDS_HOME opensearch-dashboards

COPY --from=linux_stage_0 --chown=$UID:$GID $OPENSEARCH_DASHBOARDS_HOME $OPENSEARCH_DASHBOARDS_HOME

# Setup OpenSearch-dashboards
WORKDIR $OPENSEARCH_DASHBOARDS_HOME

# Change user
USER $UID

# Expose port
EXPOSE 5601

ARG VERSION
ARG BUILD_DATE
ARG NOTES

# Label
LABEL org.label-schema.schema-version="1.0" \
  org.label-schema.name="opensearch-dashboards" \
  org.label-schema.version="$VERSION" \
  org.label-schema.url="https://opensearch.org" \
  org.label-schema.vcs-url="https://github.com/opensearch-project/OpenSearch-Dashboards" \
  org.label-schema.license="Apache-2.0" \
  org.label-schema.vendor="Amazon" \
  org.label-schema.description="$NOTES" \
  org.label-schema.build-date="$BUILD_DATE"

# CMD to run
CMD ["./opensearch-dashboards-docker-entrypoint.sh"]
