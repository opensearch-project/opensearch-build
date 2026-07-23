# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0


# This dockerfile generates a Red Hat UBI-based image containing an OpenSearch-Dashboards installation.
# Dockerfile for building an OpenSearch-Dashboards image based on Red Hat UBI 10 minimal for Red Hat certification.
# This image is designed to work with arbitrary UIDs in OpenShift without requiring SCC modifications.
# It assumes that the working directory contains four files: an OpenSearch-Dashboards tarball (opensearch-dashboards.tgz), opensearch_dashboards.yml, opensearch-dashboards-docker-entrypoint.sh, and example certs.
# Build arguments:
#   VERSION: Required. Used to label the image.
#   BUILD_DATE: Required. Used to label the image. Should be in the form 'yyyy-mm-ddThh:mm:ssZ', i.e. a date-time from https://tools.ietf.org/html/rfc3339. The timestamp must be in UTC.
#   OPENSEARCH_DASHBOARDS_HOME: Optional. Specify the opensearch-dashboards root directory. Defaults to /usr/share/opensearch-dashboards.

########################### Stage 0 ########################
FROM registry.access.redhat.com/ubi10-minimal:10.1 AS linux_stage_0

ARG VERSION
ARG TEMP_DIR=/tmp/opensearch-dashboards
ARG OPENSEARCH_DASHBOARDS_HOME=/usr/share/opensearch-dashboards

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball.
# Install which to allow running of securityadmin.sh
RUN microdnf update -y && \
    microdnf install -y tar gzip which dnf && \
    microdnf clean all

RUN mkdir -p $TEMP_DIR && \
    mkdir -p $OPENSEARCH_DASHBOARDS_HOME && \
    chmod 777 $TEMP_DIR

# Prepare working directory
COPY * $TEMP_DIR/
RUN tar -xzpf $TEMP_DIR/opensearch-dashboards-`uname -m`.tgz -C $OPENSEARCH_DASHBOARDS_HOME --strip-components=1 && \
    MAJOR_VERSION_ENTRYPOINT=`echo $VERSION | cut -d. -f1` && \
    MAJOR_VERSION_YML=`echo $VERSION | cut -d. -f1` && \
    echo $MAJOR_VERSION_ENTRYPOINT && echo $MAJOR_VERSION_YML && \
    if ! (ls $TEMP_DIR | grep -E "opensearch-dashboards-docker-entrypoint-.*.x.sh" | grep $MAJOR_VERSION_ENTRYPOINT); then MAJOR_VERSION_ENTRYPOINT="default"; fi && \
    if ! (ls $TEMP_DIR | grep -E "opensearch_dashboards-.*.x.yml" | grep $MAJOR_VERSION_YML); then MAJOR_VERSION_YML="default"; fi && \
    cp -v $TEMP_DIR/opensearch-dashboards-docker-entrypoint-$MAJOR_VERSION_ENTRYPOINT.x.sh $OPENSEARCH_DASHBOARDS_HOME/opensearch-dashboards-docker-entrypoint.sh && \
    cp -v $TEMP_DIR/opensearch_dashboards-$MAJOR_VERSION_YML.x.yml $OPENSEARCH_DASHBOARDS_HOME/config/opensearch_dashboards.yml && \
    cp -v $TEMP_DIR/opensearch.example.org.* $OPENSEARCH_DASHBOARDS_HOME/config/ && \
    echo "server.host: '0.0.0.0'" >> $OPENSEARCH_DASHBOARDS_HOME/config/opensearch_dashboards.yml && \
    chgrp -R 0 $OPENSEARCH_DASHBOARDS_HOME && \
    chmod -R g+rwX $OPENSEARCH_DASHBOARDS_HOME && \
    chmod g+x $OPENSEARCH_DASHBOARDS_HOME/opensearch-dashboards-docker-entrypoint.sh && \
    ls -l $OPENSEARCH_DASHBOARDS_HOME && \
    rm -rf $TEMP_DIR

########################### Stage 1 ########################
# Copy working directory to the actual release docker images
FROM registry.access.redhat.com/ubi10-minimal:10.1

ARG OPENSEARCH_DASHBOARDS_HOME=/usr/share/opensearch-dashboards

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball.
# Install which to allow running of securityadmin.sh
RUN microdnf update -y && \
    microdnf install -y tar gzip which dnf && \
    microdnf clean all

# Install Reporting dependencies
RUN dnf install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && dnf clean all

# Copy from Stage0 with root group ownership (GID 0) for OpenShift arbitrary UID support
COPY --from=linux_stage_0 --chown=root:0 $OPENSEARCH_DASHBOARDS_HOME $OPENSEARCH_DASHBOARDS_HOME

# Setup OpenSearch-dashboards
WORKDIR $OPENSEARCH_DASHBOARDS_HOME

RUN chgrp -R 0 $OPENSEARCH_DASHBOARDS_HOME && \
    chmod -R g+rwX $OPENSEARCH_DASHBOARDS_HOME

# Set PATH
ENV PATH=$PATH:$OPENSEARCH_DASHBOARDS_HOME/bin

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
  "DOCKERFILE"="https://github.com/opensearch-project/opensearch-build/blob/main/docker/release/dockerfiles/opensearch-dashboards.ubi10.dockerfile"

# CMD to run
ENTRYPOINT ["./opensearch-dashboards-docker-entrypoint.sh"]
CMD ["opensearch-dashboards"]
