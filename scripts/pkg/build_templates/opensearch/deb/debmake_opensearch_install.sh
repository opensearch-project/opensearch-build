#!/bin/sh

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# debmake install script

set -ex

if [ -z "$1" ]; then
    echo "Missing curdir path"
    exit 1
fi

curdir=$1
name=opensearch
product_dir=/usr/share/${name}
config_dir=/etc/${name}
data_dir=/var/lib/${name}
log_dir=/var/log/${name}
pid_dir=/var/run/${name}
buildroot=${curdir}/debian/${name}

# Create necessary directories
mkdir -p ${buildroot}
mkdir -p ${buildroot}${pid_dir}
mkdir -p ${buildroot}${product_dir}/plugins

# Install directories/files
cp -a ${curdir}/etc ${curdir}/usr ${curdir}/var ${buildroot}/
chmod -c 0755 ${buildroot}${product_dir}/bin/*
if [ -d ${buildroot}${product_dir}/plugins/opensearch-security ]; then
    chmod -c 0755 ${buildroot}${product_dir}/plugins/opensearch-security/tools/*
fi

# Symlinks (do not symlink config dir as security demo installer has dependency, if no presense it will switch to rpm/deb mode)
ln -s ${data_dir} ${buildroot}${product_dir}/data
ln -s ${log_dir}  ${buildroot}${product_dir}/logs

# Performance Analyzer Settings
echo 'true' > ${buildroot}${data_dir}/rca_enabled.conf
echo 'true' > ${buildroot}${config_dir}/performance_analyzer_enabled.conf
echo 'true' > ${buildroot}${config_dir}/rca_enabled.conf
# Change Permissions
chmod -Rf a+rX,u+w,g-w,o-w ${buildroot}/*

exit 0
