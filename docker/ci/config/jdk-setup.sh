#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Downloads JDK distributions using Eclipse Adoptium project.
# The distributions are extracted to /opt/java/ folder
# with environment variables JAVA${MAJOR_VERSION}_HOME exported and pointing at respective ones.
# JAVA_HOME as well as PATH=$PATH:JAVA_HOME is default to the one with the highest version.

set -eux

ARCH="$(uname -m)"
JDKS=""

case "${ARCH}" in
   aarch64|arm64)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="f287cdc2a688c2df247ea0d8bfe2863645b73848e4e5c35b02a8a3d2d6b69551@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u302-b08/OpenJDK8U-jdk_aarch64_linux_hotspot_8u302b08.tar.gz "
       JDKS+="0ba188a2a739733163cd0049344429d2284867e04ca452879be24f3b54320c9a@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14%2B9/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.14_9.tar.gz "
       JDKS+="302caf29f73481b2b914ba2b89705036010c65eb9bc8d7712b27d6e9bedf6200@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.2_8.tar.gz "
       ;;
   amd64|x86_64)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="cc13f274becf9dd5517b6be583632819dfd4dd81e524b5c1b4f406bdaf0e063a@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u302-b08/OpenJDK8U-jdk_x64_linux_hotspot_8u302b08.tar.gz "
       JDKS+="1189bee178d11402a690edf3fbba0c9f2ada1d3a36ff78929d81935842ef24a9@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz "
       JDKS+="288f34e3ba8a4838605636485d0365ce23e57d5f2f68997ac4c2e4c01967cd48@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_x64_linux_hotspot_17.0.2_8.tar.gz "
       ;;
   *)
       echo "Unsupported arch: ${ARCH}"
       exit 1
       ;;
esac

for jdk in ${JDKS}; do
    ESUM=$(echo ${jdk} | cut -d '@' -f1)
    BINARY_URL=$(echo ${jdk} | cut -d '@' -f2)
    regex="temurin([0-9]+)[-]"
    if [[ $jdk =~ $regex ]]; then
        MAJOR=${BASH_REMATCH[1]}
        curl -LfsSo /tmp/openjdk-${MAJOR}.tar.gz ${BINARY_URL}
        echo "${ESUM} */tmp/openjdk-${MAJOR}.tar.gz" | sha256sum -c -
        mkdir -p /opt/java/openjdk-${MAJOR}
        cd /opt/java/openjdk-${MAJOR}
        tar -xf /tmp/openjdk-${MAJOR}.tar.gz --strip-components=1
        rm -rf /tmp/openjdk-${MAJOR}.tar.gz
        echo "export JAVA${MAJOR}_HOME=/opt/java/openjdk-${MAJOR}" >> /etc/profile.d/java_home.sh
    fi
done;

echo "export JAVA_HOME=\$JAVA${MAJOR}_HOME" >> /etc/profile.d/java_home.sh
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile.d/java_home.sh
