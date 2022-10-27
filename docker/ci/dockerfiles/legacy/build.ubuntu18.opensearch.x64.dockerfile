# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for running gradle check of OpenSearch repository

FROM ubuntu:18.04

# Install necessary packages

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y docker.io curl && apt clean -y 


# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch


# Downloads JDK-8, JDK-11 and JDK-17 distributions using Eclipse Adoptium project.
# The distributions are extracted to /opt/java/ folder with environment variables JAVA8_HOME,
# JAVA11_HOME and JAVA17_HOME exported and pointing at respective ones.

# JDK 8
RUN curl -SL https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u302-b08/OpenJDK8U-jdk_x64_linux_hotspot_8u302b08.tar.gz -o /opt/jdk8.tar.gz && \
    mkdir -p /opt/java/openjdk-8 && \
    tar -xzf /opt/jdk8.tar.gz --strip-components 1 -C /opt/java/openjdk-8/ && \
    rm /opt/jdk8.tar.gz
# JDK 11
RUN curl -SL https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.12_7.tar.gz -o /opt/jdk11.tar.gz && \
    mkdir -p /opt/java/openjdk-11 && \
    tar -xzf /opt/jdk11.tar.gz --strip-components 1 -C /opt/java/openjdk-11/ && \
    rm /opt/jdk11.tar.gz
# JDK 14
RUN curl -SL https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U-jdk_x64_linux_hotspot_14.0.2_12.tar.gz -o /opt/jdk14.tar.gz && \
    mkdir -p /opt/java/openjdk-14 && \
    tar -xzf /opt/jdk14.tar.gz --strip-components 1 -C /opt/java/openjdk-14/ && \
    rm /opt/jdk14.tar.gz
# JDK 17
RUN curl -SL https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_linux_hotspot_17_35.tar.gz -o /opt/jdk17.tar.gz && \
    mkdir -p /opt/java/openjdk-17 && \
    tar -xzf /opt/jdk17.tar.gz --strip-components 1 -C /opt/java/openjdk-17/ && \
    rm /opt/jdk17.tar.gz

# ENV JDK
ENV JAVA_HOME=/opt/java/openjdk-14 \
    PATH=$PATH:$JAVA_HOME/bin \
    JAVA14_HOME=/opt/java/openjdk-14 \
    JAVA8_HOME=/opt/java/openjdk-8 \
    JAVA11_HOME=/opt/java/openjdk-11 \
    JAVA17_HOME=/opt/java/openjdk-17

# Sets user to opensearch as gradle check requires non-root user
USER opensearch

# Sets working directory with write permission to clone OpenSearch
WORKDIR /usr/share/opensearch
