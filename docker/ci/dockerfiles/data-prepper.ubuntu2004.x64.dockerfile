# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for releasing data-prepper artifacts

FROM ubuntu:20.04

ARG MAVEN_DIR=/usr/local/apache-maven

# Import necessary repository for installing qemu 5.0
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y wget docker.io curl python3-pip python3.7 && apt clean -y && pip3 install pipenv awscli==1.22.12

# Install JDK
RUN curl -SL https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.9.1%2B1/OpenJDK11U-jdk_x64_linux_hotspot_11.0.9.1_1.tar.gz -o /opt/jdk11.tar.gz && \
    mkdir -p /opt/java/openjdk-11 && \
    tar -xzf /opt/jdk11.tar.gz --strip-components 1 -C /opt/java/openjdk-11/ && \
    rm /opt/jdk11.tar.gz

# ENV JDK
ENV JAVA_HOME=/opt/java/openjdk-11
ENV PATH=$PATH:$JAVA_HOME/bin

# Install higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"'`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn
