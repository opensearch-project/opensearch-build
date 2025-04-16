#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# debmake opensearch-dashboards install script

set -ex

if [ -z "$1" ]; then
    echo "Missing curdir path"
    exit 1
fi

curdir=$1
product_dir=/usr/share/opensearch-dashboards
config_dir=/etc/opensearch-dashboards
data_dir=/var/lib/opensearch-dashboards
log_dir=/var/log/opensearch-dashboards
pid_dir=/var/run/opensearch-dashboards
buildroot=${curdir}/debian/opensearch-dashboards

# Create necessary directories
mkdir -p ${buildroot}
mkdir -p ${buildroot}${pid_dir}
mkdir -p ${buildroot}${product_dir}/assets
mkdir -p ${buildroot}${product_dir}/plugins
mkdir -p ${buildroot}${log_dir}

# Install directories/files
# Service files stored in /usr/lib/systemd for pkg installation, /etc/systemd is meant for manual changes by sysadmin
rm -rvf ${curdir}/etc/systemd
cp -a ${curdir}/etc ${curdir}/usr ${curdir}/var ${buildroot}/
chmod -c 0755 ${buildroot}${product_dir}/bin/*

# Symlinks (do not symlink config dir as security demo installer has dependency, if no presense it will switch to rpm/deb mode)
ln -s ${data_dir} ${buildroot}${product_dir}/data
ln -s ${log_dir}  ${buildroot}${product_dir}/logs

# Change Permissions
chmod -Rf g-s ${buildroot}/*
chmod -Rf u=rwX,g=rX,o=rX ${buildroot}/*

exit 0
