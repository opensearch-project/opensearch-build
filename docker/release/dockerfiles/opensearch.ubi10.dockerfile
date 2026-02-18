# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0


# This dockerfile generates a Red Hat UBI-based image containing an OpenSearch installation.
# Dockerfile for building an OpenSearch image based on Red Hat UBI 10 minimal for Red Hat certification.
# This image is designed to work with arbitrary UIDs in OpenShift without requiring SCC modifications.
# It assumes that the working directory contains these files: an OpenSearch tarball (opensearch.tgz), log4j2.properties, opensearch.yml, opensearch-docker-entrypoint.sh, opensearch-onetime-setup.sh.
# Build arguments:
#   VERSION: Required. Used to label the image.
#   BUILD_DATE: Required. Used to label the image. Should be in the form 'yyyy-mm-ddThh:mm:ssZ', i.e. a date-time from https://tools.ietf.org/html/rfc3339. The timestamp must be in UTC.
#   OPENSEARCH_HOME: Optional. Specify the opensearch root directory. Defaults to /usr/share/opensearch.


########################### Stage 0 ########################
FROM registry.access.redhat.com/ubi10-minimal:10.1 AS linux_stage_0

ARG VERSION
ARG TEMP_DIR=/tmp/opensearch
ARG OPENSEARCH_HOME=/usr/share/opensearch
ARG OPENSEARCH_PATH_CONF=$OPENSEARCH_HOME/config
ARG SECURITY_PLUGIN_DIR=$OPENSEARCH_HOME/plugins/opensearch-security
ARG PERFORMANCE_ANALYZER_PLUGIN_CONFIG_DIR=$OPENSEARCH_PATH_CONF/opensearch-performance-analyzer

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball.
# Install which to allow running of securityadmin.sh
RUN microdnf update -y && \
    microdnf install -y tar gzip which && \
    microdnf clean all

RUN mkdir -p $TEMP_DIR && \
    mkdir -p $OPENSEARCH_HOME && \
    chmod 777 $TEMP_DIR

# Prepare working directory
# Copy artifacts and configurations to corresponding directories
COPY * $TEMP_DIR/
RUN ls -l $TEMP_DIR && \
    tar -xzpf /tmp/opensearch/opensearch-`uname -m`.tgz -C $OPENSEARCH_HOME --strip-components=1 && \
    MAJOR_VERSION_ENTRYPOINT=`echo $VERSION | cut -d. -f1` && \
    echo $MAJOR_VERSION_ENTRYPOINT && \
    if ! (ls $TEMP_DIR | grep -E "opensearch-docker-entrypoint-.*.x.sh" | grep $MAJOR_VERSION_ENTRYPOINT); then MAJOR_VERSION_ENTRYPOINT="default"; fi && \
    mkdir -p $OPENSEARCH_HOME/data && chown -Rv root:0 $OPENSEARCH_HOME/data && chmod -Rv g+rwX $OPENSEARCH_HOME/data && \
    if [[ -d $SECURITY_PLUGIN_DIR ]] ; then chmod -v 750 $SECURITY_PLUGIN_DIR/tools/* && chgrp -R 0 $SECURITY_PLUGIN_DIR/tools/* && chmod -R g+rwX $SECURITY_PLUGIN_DIR/tools/* ; fi && \
    if [[ -d $PERFORMANCE_ANALYZER_PLUGIN_CONFIG_DIR ]] ; then cp -v $TEMP_DIR/performance-analyzer.properties $PERFORMANCE_ANALYZER_PLUGIN_CONFIG_DIR; fi && \
    cp -v $TEMP_DIR/opensearch-docker-entrypoint-$MAJOR_VERSION_ENTRYPOINT.x.sh $OPENSEARCH_HOME/opensearch-docker-entrypoint.sh && \
    cp -v $TEMP_DIR/opensearch-onetime-setup.sh $OPENSEARCH_HOME/ && \
    cp -v $TEMP_DIR/log4j2.properties $TEMP_DIR/opensearch.yml $OPENSEARCH_PATH_CONF/ && \
    chgrp -R 0 $OPENSEARCH_HOME && \
    chmod -R g+rwX $OPENSEARCH_HOME && \
    chmod g+x $OPENSEARCH_HOME/opensearch-docker-entrypoint.sh $OPENSEARCH_HOME/opensearch-onetime-setup.sh && \
    ls -l $OPENSEARCH_HOME && \
    rm -rf $TEMP_DIR

########################### Stage 1 ########################
# Copy working directory to the actual release docker images
FROM registry.access.redhat.com/ubi10-minimal:10.1

ARG OPENSEARCH_HOME=/usr/share/opensearch

# Update packages
# Install the tools we need: tar and gzip to unpack the OpenSearch tarball.
# Install which to allow running of securityadmin.sh
RUN microdnf update -y && \
    microdnf install -y tar gzip which && \
    microdnf clean all

# Copy from Stage0 with root group ownership (GID 0) for OpenShift arbitrary UID support
COPY --from=linux_stage_0 --chown=root:0 $OPENSEARCH_HOME $OPENSEARCH_HOME
WORKDIR $OPENSEARCH_HOME

RUN chgrp -R 0 $OPENSEARCH_HOME && \
    chmod -R g+rwX $OPENSEARCH_HOME && \
    find $OPENSEARCH_HOME -type d -exec chmod g+x {} + && \
    find $OPENSEARCH_HOME -type f -exec chmod g+r {} +

# Set $JAVA_HOME
RUN echo "export JAVA_HOME=$OPENSEARCH_HOME/jdk" >> /etc/profile.d/java_home.sh && \
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile.d/java_home.sh && \
    ls -l $OPENSEARCH_HOME

ENV JAVA_HOME=$OPENSEARCH_HOME/jdk
ENV PATH=$PATH:$JAVA_HOME/bin:$OPENSEARCH_HOME/bin

# Add k-NN lib directory to library loading path variable
ENV LD_LIBRARY_PATH="$OPENSEARCH_HOME/plugins/opensearch-knn/lib"

# Setup OpenSearch
# Disable security demo installation during image build, and allow user to disable during startup of the container
# Enable security plugin during image build, and allow user to disable during startup of the container
ARG DISABLE_INSTALL_DEMO_CONFIG=true
ARG DISABLE_SECURITY_PLUGIN=false
RUN ./opensearch-onetime-setup.sh && \
    chgrp -R 0 $OPENSEARCH_HOME && \
    chmod -R g+rwX $OPENSEARCH_HOME

# Expose ports for the opensearch service (9200 for HTTP and 9300 for internal transport) and performance analyzer (9600 for the agent and 9650 for the root cause analysis component)
EXPOSE 9200 9300 9600 9650

ARG VERSION
ARG BUILD_DATE
ARG NOTES

# Label
LABEL org.label-schema.schema-version="1.0" \
  org.label-schema.name="opensearch" \
  org.label-schema.version="$VERSION" \
  org.label-schema.url="https://opensearch.org" \
  org.label-schema.vcs-url="https://github.com/opensearch-project/OpenSearch" \
  org.label-schema.license="Apache-2.0" \
  org.label-schema.vendor="OpenSearch" \
  org.label-schema.description="$NOTES" \
  org.label-schema.build-date="$BUILD_DATE" \
  "DOCKERFILE"="https://github.com/opensearch-project/opensearch-build/blob/main/docker/release/dockerfiles/opensearch.ubi8.dockerfile"

RUN chmod g+x $OPENSEARCH_HOME/opensearch-docker-entrypoint.sh

# CMD to run
ENTRYPOINT ["./opensearch-docker-entrypoint.sh"]
CMD ["opensearch"]
