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
       JDKS+="ee87e9f03b1fbe6f328429b78fe1a9f44900026d220c90dfd747fe0bcd62d904@https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U-jdk_aarch64_linux_hotspot_14.0.2_12.tar.gz "
       JDKS+="2e3c19c1707205c6b90cc04b416e8d83078ed98417d5a69dce3cf7dc0d7cfbca@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.3_7.tar.gz "
       JDKS+="5e8d7b3189364afd78d936bad140dbe1e7025d4b96d530ed5536d035c21afb7c@https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.1%2B10/OpenJDK19U-jdk_aarch64_linux_hotspot_19.0.1_10.tar.gz "
       JDKS+="b16c0271899de1f0e277dc0398bfff11b54511765f104fa938929ac484dc926d@https://github.com/adoptium/temurin20-binaries/releases/download/jdk-20.0.1%2B9/OpenJDK20U-jdk_aarch64_linux_hotspot_20.0.1_9.tar.gz "
       JDKS+="e184dc29a6712c1f78754ab36fb48866583665fa345324f1a79e569c064f95e9@https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_aarch64_linux_hotspot_21.0.1_12.tar.gz "
       ;;
   amd64|x86_64)
       # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
       JDKS+="adc13a0a0540d77f0a3481b48f10d61eb203e5ad4914507d489c2de3bd3d83da@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u332-b09/OpenJDK8U-jdk_x64_linux_hotspot_8u332b09.tar.gz "
       JDKS+="5fdb4d5a1662f0cca73fec30f99e67662350b1fa61460fa72e91eb9f66b54d0b@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz "
       JDKS+="7d5ee7e06909b8a99c0d029f512f67b092597aa5b0e78c109bd59405bbfa74fe@https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U-jdk_x64_linux_hotspot_14.0.2_12.tar.gz "
       JDKS+="81f5bed21077f9fbb04909b50391620c78b9a3c376593c0992934719c0de6b73@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.3_7.tar.gz "
       JDKS+="163da7ea140210bae97c6a4590c757858ab4520a78af0e3e33129863d4087552@https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.1%2B10/OpenJDK19U-jdk_x64_linux_hotspot_19.0.1_10.tar.gz "
       JDKS+="43ad054f135a7894dc87ad5d10ad45d8e82846186515892acdbc17c2c5cd27e4@https://github.com/adoptium/temurin20-binaries/releases/download/jdk-20.0.1%2B9/OpenJDK20U-jdk_x64_linux_hotspot_20.0.1_9.tar.gz "
       JDKS+="1a6fa8abda4c5caed915cfbeeb176e7fbd12eb6b222f26e290ee45808b529aa1@https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.1%2B12/OpenJDK21U-jdk_x64_linux_hotspot_21.0.1_12.tar.gz "
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
