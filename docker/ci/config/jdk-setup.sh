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
       JDKS+="999fbd90b070f9896142f0eb28354abbeb367cbe49fd86885c626e2999189e0a@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.15_10.tar.gz "
       JDKS+="2e3c19c1707205c6b90cc04b416e8d83078ed98417d5a69dce3cf7dc0d7cfbca@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.3_7.tar.gz "
       JDKS+="e184dc29a6712c1f78754ab36fb48866583665fa345324f1a79e569c064f95e9@https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_aarch64_linux_hotspot_21.0.1_12.tar.gz "
       JDKS+="a598260e340028d9b2383c23df16aa286769a661bd3bf28a52e8c1a5774b1110@https://github.com/adoptium/temurin24-binaries/releases/download/jdk-24.0.1%2B9/OpenJDK24U-jdk_aarch64_linux_hotspot_24.0.1_9.tar.gz "
       JDKS+="95716d04bdfc8b10c94f4448ea8d57a3ba872d98b53c752e4c6b48f1c95bc582@https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25%2B36/OpenJDK25U-jdk_aarch64_linux_hotspot_25_36.tar.gz "
       ;;
   amd64|x86_64)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="5fdb4d5a1662f0cca73fec30f99e67662350b1fa61460fa72e91eb9f66b54d0b@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz "
       JDKS+="81f5bed21077f9fbb04909b50391620c78b9a3c376593c0992934719c0de6b73@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.3_7.tar.gz "
       JDKS+="1a6fa8abda4c5caed915cfbeeb176e7fbd12eb6b222f26e290ee45808b529aa1@https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_x64_linux_hotspot_21.0.1_12.tar.gz "
       JDKS+="78832cb5ea4074f2215cde0d01d6192d09c87636fc24b36647aea61fb23b8272@https://github.com/adoptium/temurin24-binaries/releases/download/jdk-24.0.1%2B9/OpenJDK24U-jdk_x64_linux_hotspot_24.0.1_9.tar.gz "
       JDKS+="ee04de95ab9da7287d40bd2173076ecc2a6dd662f007bedfc6eb0380c0ef90e8@https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25%2B36/OpenJDK25U-jdk_x64_linux_hotspot_25_36.tar.gz "
       ;;
   ppc64le)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="262ff98d6d88a7c7cc522cb4ec4129491a0eb04f5b17dcca0da57cfcdcf3830d@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%2B9/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.21_9.tar.gz "
       JDKS+="3ae4b254d5b720f94f986481e787fbd67f0667571140ba2e2ae5020ceddbc826@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_ppc64le_linux_hotspot_17.0.9_9.tar.gz "
       JDKS+="9574828ef3d735a25404ced82e09bf20e1614f7d6403956002de9cfbfcb8638f@https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_ppc64le_linux_hotspot_21.0.1_12.tar.gz "
       JDKS+="770e7e506d5ea3baf6c4c9004a82648e29508a1c731d8425acded34906e91b09@https://github.com/adoptium/temurin24-binaries/releases/download/jdk-24.0.1%2B9/OpenJDK24U-jdk_ppc64le_linux_hotspot_24.0.1_9.tar.gz "
       JDKS+="b060bb12b3a192a0599f03ebb9495492f78c48cb61e291e336a8b00e7798ffb0@https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25%2B36/OpenJDK25U-jdk_ppc64le_linux_hotspot_25_36.tar.gz "
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
    regex2="openjdk([0-9]+)[-]"
    if [[ $jdk =~ $regex || $jdk =~ $regex2 ]]; then
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
