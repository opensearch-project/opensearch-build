# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0


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
ARG TEMP_DIR=/tmp/opensearch-dashboards
ARG OPENSEARCH_DASHBOARDS_HOME=/usr/share/opensearch-dashboards

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball, and shadow-utils to give us `groupadd` and `useradd`.
# Install which to allow running of securityadmin.sh
RUN yum update -y && yum install -y tar gzip shadow-utils which && yum clean all

# Create an opensearch-dashboards user, group, and directory
RUN groupadd -g $GID opensearch-dashboards && \
    adduser -u $UID -g $GID -d $OPENSEARCH_DASHBOARDS_HOME opensearch-dashboards && \
    mkdir $TEMP_DIR

# Prepare working directory
COPY * $TEMP_DIR
RUN tar -xzpf $TEMP_DIR/opensearch-dashboards-`uname -p`.tgz -C $OPENSEARCH_DASHBOARDS_HOME --strip-components=1 && \
    cp -v $TEMP_DIR/opensearch-dashboards-docker-entrypoint.sh $OPENSEARCH_DASHBOARDS_HOME/ && \
    cp -v $TEMP_DIR/opensearch_dashboards.yml $TEMP_DIR/opensearch.example.org.* $OPENSEARCH_DASHBOARDS_HOME/config/ && \
    ls -l $OPENSEARCH_DASHBOARDS_HOME && \
    rm -rf $TEMP_DIR

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

# Install Reporting dependencies
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
