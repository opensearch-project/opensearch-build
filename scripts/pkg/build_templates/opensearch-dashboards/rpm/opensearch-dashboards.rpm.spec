# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# No build, no debuginfo
%define debug_package %{nil}

# Disable brp-java-repack-jars, so jars will not be decompressed and repackaged
%define __jar_repack 0

# Generate digests, 8 means algorithm of sha256
# This is different from rpm sig algorithm
# Requires rpm version 4.12 + to generate but b/c run on older versions
%define _source_filedigest_algorithm 8
%define _binary_filedigest_algorithm 8

# User Define Variables
%define product_dir %{_datadir}/%{name}
%define config_dir %{_sysconfdir}/%{name}
%define data_dir %{_sharedstatedir}/%{name}
%define log_dir %{_localstatedir}/log/%{name}
%define pid_dir %{_localstatedir}/run/%{name}
%{!?_version: %define _version 0.0.0 }
%{!?_architecture: %define _architecture x86_64 }

Name: opensearch-dashboards
Version: %{_version}
Release: 1
License: Apache-2.0
Summary: Open source visualization dashboards for OpenSearch 
URL: https://opensearch.org/
Group: Application/Internet
ExclusiveArch: %{_architecture}
AutoReqProv: no

%description
OpenSearch Dashboards is the visualization tool for data in OpenSearch
For more information, see: https://opensearch.org/

%prep
# No-op. We are using dir so no need to setup.

%build
# No-op. This is all pre-built Java. Nothing to do here.

%install
set -e
cd %{_topdir} && pwd
# Create necessary directories
mkdir -p %{buildroot}%{pid_dir}
mkdir -p %{buildroot}%{product_dir}/assets
mkdir -p %{buildroot}%{product_dir}/plugins
mkdir -p %{buildroot}%{log_dir}
# Install directories/files
# Service files stored in /usr/lib/systemd for pkg installation, /etc/systemd is meant for manual changes by sysadmin
rm -rvf etc/systemd
cp -a etc usr var %{buildroot}
chmod 0755 %{buildroot}%{product_dir}/bin/*
# Symlinks (do not symlink config dir as security demo installer has dependency, if no presense it will switch to rpm/deb mode)
ln -s %{data_dir} %{buildroot}%{product_dir}/data
ln -s %{log_dir}  %{buildroot}%{product_dir}/logs
# Change Permissions
chmod -Rf a+rX,u+w,g-w,o-w %{buildroot}/*
exit 0

%pre
set -e
# Stop existing service
if command -v systemctl >/dev/null && systemctl is-active %{name}.service >/dev/null; then
    echo "Stop existing %{name}.service"
    systemctl --no-reload stop %{name}.service
fi
# Create user and group if they do not already exist.
getent group %{name} > /dev/null 2>&1 || groupadd -r %{name}
getent passwd %{name} > /dev/null 2>&1 || \
    useradd -r -g %{name} -M -s /sbin/nologin \
        -c "%{name} user/group" %{name}
exit 0

%post
set -e
# Reload systemctl daemon
if command -v systemctl > /dev/null; then
    systemctl daemon-reload
fi
# Reload other configs
if command -v systemd-tmpfiles > /dev/null; then
    systemd-tmpfiles --create %{name}.conf
fi
# Messages
echo "### NOT starting on installation, please execute the following statements to configure opensearch-dashboards service to start automatically using systemd"
echo " sudo systemctl daemon-reload"
echo " sudo systemctl enable opensearch-dashboards.service"
echo "### You can start opensearch-dashboards service by executing"
echo " sudo systemctl start opensearch-dashboards.service"
echo "### Upcoming breaking change in packaging"
echo " In a future release of OpenSearch Dashboards, we plan to change the permissions associated with access to installed files"
echo " If you are configuring tools that require read access to the OpenSearch Dashboards configuration files, we recommend you add the user that runs these tools to the 'opensearch-dashboards' group"
echo " For more information, see https://github.com/opensearch-project/opensearch-build/pull/4043"
exit 0

%preun
set -e
if command -v systemctl >/dev/null && systemctl is-active %{name}.service >/dev/null; then
    echo "Stop existing %{name}.service"
    systemctl --no-reload stop %{name}.service
fi
exit 0

%files
# Permissions
%defattr(-, %{name}, %{name})

# Root dirs/docs/licenses
%dir %{product_dir}
%doc %{product_dir}/NOTICE.txt
%doc %{product_dir}/README.txt
%license %{product_dir}/LICENSE.txt
%{product_dir}/package.json
%{product_dir}/manifest.yml
%{product_dir}/.i18nrc.json

# Config dirs/files
%dir %{config_dir}
%config(noreplace) %{config_dir}/node.options
%config(noreplace) %{config_dir}/opensearch_dashboards.yml

# Service files
%attr(0644, root, root) %{_prefix}/lib/systemd/system/%{name}.service
%attr(0644, root, root) %{_sysconfdir}/init.d/%{name}
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/default/%{name}
%attr(0644, root, root) %config(noreplace) %{_prefix}/lib/tmpfiles.d/%{name}.conf

# Main dirs
%dir %{product_dir}/assets
%{product_dir}/bin
%{product_dir}/node
%{product_dir}/node_modules
%{product_dir}/plugins
%{product_dir}/src
%{log_dir}
%{pid_dir}
%dir %{data_dir}

# Symlinks
%{product_dir}/data
%{product_dir}/logs

%changelog
* Mon Mar 21 2022 OpenSearch Team <opensearch@amazon.com>
- Initial package

