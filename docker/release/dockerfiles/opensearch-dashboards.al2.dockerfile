# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0


# This dockerfile generates an AmazonLinux-based image containing an OpenSearch-Dashboards installation (1.x Only).
# Dockerfile for building an OpenSearch-Dashboards image.
# It assumes that the working directory contains four files: an OpenSearch-Dashboards tarball (opensearch-dashboards.tgz), opensearch_dashboards.yml, opensearch-dashboards-docker-entrypoint.sh, and example certs.
# Build arguments:
#   VERSION: Required. Used to label the image.
#   BUILD_DATE: Required. Used to label the image. Should be in the form 'yyyy-mm-ddThh:mm:ssZ', i.e. a date-time from https://tools.ietf.org/html/rfc3339. The timestamp must be in UTC.
#   UID: Optional. Specify the opensearch-dashboards userid. Defaults to 1000.
#   GID: Optional. Specify the opensearch-dashboards groupid. Defaults to 1000.
#   OPENSEARCH_DASHBOARDS_HOME: Optional. Specify the opensearch-dashboards root directory. Defaults to /usr/share/opensearch-dashboards.

########################### Stage 0 ########################
FROM public.ecr.aws/amazonlinux/amazonlinux:2 AS linux_stage_0

ARG UID=1000
ARG GID=1000
ARG VERSION
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
COPY * $TEMP_DIR/
RUN tar -xzpf $TEMP_DIR/opensearch-dashboards-`uname -p`.tgz -C $OPENSEARCH_DASHBOARDS_HOME --strip-components=1 && \
    MAJOR_VERSION_ENTRYPOINT=`echo $VERSION | cut -d. -f1` && \
    MAJOR_VERSION_YML=`echo $VERSION | cut -d. -f1` && \
    echo $MAJOR_VERSION_ENTRYPOINT && echo $MAJOR_VERSION_YML && \
    if ! (ls $TEMP_DIR | grep -E "opensearch-dashboards-docker-entrypoint-.*.x.sh" | grep $MAJOR_VERSION_ENTRYPOINT); then MAJOR_VERSION_ENTRYPOINT="default"; fi && \
    if ! (ls $TEMP_DIR | grep -E "opensearch_dashboards-.*.x.yml" | grep $MAJOR_VERSION_YML); then MAJOR_VERSION_YML="default"; fi && \
    cp -v $TEMP_DIR/opensearch-dashboards-docker-entrypoint-$MAJOR_VERSION_ENTRYPOINT.x.sh $OPENSEARCH_DASHBOARDS_HOME/opensearch-dashboards-docker-entrypoint.sh && \
    cp -v $TEMP_DIR/opensearch_dashboards-$MAJOR_VERSION_YML.x.yml $OPENSEARCH_DASHBOARDS_HOME/config/opensearch_dashboards.yml && \
    cp -v $TEMP_DIR/opensearch.example.org.* $OPENSEARCH_DASHBOARDS_HOME/config/ && \
    echo "server.host: '0.0.0.0'" >> $OPENSEARCH_DASHBOARDS_HOME/config/opensearch_dashboards.yml && \
    ls -l $OPENSEARCH_DASHBOARDS_HOME && \
    rm -rf $TEMP_DIR

########################### Stage 1 ########################
# Copy working directory to the actual release docker images
FROM public.ecr.aws/amazonlinux/amazonlinux:2

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

# Set PATH
ENV PATH=$PATH:$OPENSEARCH_DASHBOARDS_HOME/bin

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
  org.label-schema.vendor="OpenSearch" \
  org.label-schema.description="$NOTES" \
  org.label-schema.build-date="$BUILD_DATE" \
  "DOCKERFILE"="https://github.com/opensearch-project/opensearch-build/blob/main/docker/release/dockerfiles/opensearch-dashboards.al2.dockerfile"

# CMD to run
ENTRYPOINT ["./opensearch-dashboards-docker-entrypoint.sh"]
CMD ["opensearch-dashboards"]
