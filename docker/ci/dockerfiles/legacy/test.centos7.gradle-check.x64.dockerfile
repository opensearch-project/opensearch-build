# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for running OpenSearch core gradle check
# It should be used on a Jenkins Agent node with only 1 executor, 16xCPU + 16/32GB Memory

# This image can be used with these arguments: 
# '-u root -v /var/run/docker.sock:/var/run/docker.sock -e JAVA_HOME=/opt/java/openjdk-17 -e JAVA11_HOME=/opt/java/openjdk-11 -e JAVA8_HOME=/opt/java/openjdk-8'


FROM centos:7

ARG MAVEN_DIR=/usr/local/apache-maven

# Ensure localedef running correct with root permission
USER 0

# Setup ENV to prevent ASCII data issues with Python3
RUN echo "export LC_ALL=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    echo "export LANG=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    localedef -v -c -i en_US -f UTF-8 en_US.UTF-8 || echo set locale

# Add normal dependencies
RUN yum clean all && \
    yum update -y && \
    yum install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip docker zip unzip jq

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

#JDK setup
COPY --chown=0:0 config/jdk-setup.sh /tmp
RUN /tmp/jdk-setup.sh

# Install higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"'`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn

# Change User
USER 1000
WORKDIR /usr/share/opensearch

