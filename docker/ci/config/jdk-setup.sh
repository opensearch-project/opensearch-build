#!/bin/bash

# Copyright OpenSearch Contributors
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
       JDKS+="d10efb2afad3ed3d7bac9d3249cea77928aca6acb973cac0f90a2dd3606a3533@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u332-b09/OpenJDK8U-jdk_aarch64_linux_hotspot_8u332b09.tar.gz "
       JDKS+="999fbd90b070f9896142f0eb28354abbeb367cbe49fd86885c626e2999189e0a@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.15_10.tar.gz "
       JDKS+="2e3c19c1707205c6b90cc04b416e8d83078ed98417d5a69dce3cf7dc0d7cfbca@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.3_7.tar.gz "
       ;;
   amd64|x86_64)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="adc13a0a0540d77f0a3481b48f10d61eb203e5ad4914507d489c2de3bd3d83da@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u332-b09/OpenJDK8U-jdk_x64_linux_hotspot_8u332b09.tar.gz "
       JDKS+="5fdb4d5a1662f0cca73fec30f99e67662350b1fa61460fa72e91eb9f66b54d0b@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz "
       JDKS+="81f5bed21077f9fbb04909b50391620c78b9a3c376593c0992934719c0de6b73@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.3_7.tar.gz "
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
