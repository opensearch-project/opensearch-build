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

Name: opensearch
Version: %{_version}
Release: 1
License: Apache-2.0
Summary: An open source distributed and RESTful search engine
URL: https://opensearch.org/
Group: Application/Internet
ExclusiveArch: %{_architecture}
#Requires: #java-11-amazon-corretto-devel
AutoReqProv: no

%description
OpenSearch makes it easy to ingest, search, visualize, and analyze your data
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
mkdir -p %{buildroot}%{product_dir}/plugins
# Install directories/files
cp -a etc usr var %{buildroot}
chmod 0755 %{buildroot}%{product_dir}/bin/*
if [ -d %{buildroot}%{product_dir}/plugins/opensearch-security ]; then
    chmod 0755 %{buildroot}%{product_dir}/plugins/opensearch-security/tools/*
fi
# Pre-populate the folders to ensure rpm build success even without all plugins
mkdir -p %{buildroot}%{config_dir}/opensearch-observability
mkdir -p %{buildroot}%{config_dir}/opensearch-reports-scheduler
mkdir -p %{buildroot}%{product_dir}/performance-analyzer-rca
#rm -rf %{buildroot}%{product_dir}/jdk
# Symlinks (do not symlink config dir as security demo installer has dependency, if no presense it will switch to rpm/deb mode)
ln -s %{data_dir} %{buildroot}%{product_dir}/data
ln -s %{log_dir}  %{buildroot}%{product_dir}/logs
# Pre-populate PA configs if not present
if [ ! -f %{buildroot}%{data_dir}/rca_enabled.conf ]; then
    echo 'true' > %{buildroot}%{data_dir}/rca_enabled.conf
fi
if [ ! -f %{buildroot}%{data_dir}/performance_analyzer_enabled.conf ]; then
    echo 'true' > %{buildroot}%{data_dir}/performance_analyzer_enabled.conf
fi
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
if command -v systemctl >/dev/null && systemctl is-active opensearch-performance-analyzer.service >/dev/null; then
    echo "Stop existing opensearch-performance-analyzer.service"
    systemctl --no-reload stop opensearch-performance-analyzer.service
fi
# Create user and group if they do not already exist.
getent group %{name} > /dev/null 2>&1 || groupadd -r %{name}
getent passwd %{name} > /dev/null 2>&1 || \
    useradd -r -g %{name} -M -s /sbin/nologin \
        -c "%{name} user/group" %{name}
exit 0

%post
set -e
# Apply Security Settings
if [ -d %{product_dir}/plugins/opensearch-security ]; then
    sh %{product_dir}/plugins/opensearch-security/tools/install_demo_configuration.sh -y -i -s > %{log_dir}/install_demo_configuration.log 2>&1
fi
chown -R %{name}.%{name} %{config_dir}
chown -R %{name}.%{name} %{log_dir}
# Apply PerformanceAnalyzer Settings
chmod a+rw /tmp
if ! grep -q '## OpenSearch Performance Analyzer' %{config_dir}/jvm.options; then
   # Add Performance Analyzer settings in %{config_dir}/jvm.options
   CLK_TCK=`/usr/bin/getconf CLK_TCK`
   echo >> %{config_dir}/jvm.options
   echo '## OpenSearch Performance Analyzer' >> %{config_dir}/jvm.options
   echo "-Dclk.tck=$CLK_TCK" >> %{config_dir}/jvm.options
   echo "-Djdk.attach.allowAttachSelf=true" >> %{config_dir}/jvm.options
   echo "-Djava.security.policy=file://%{config_dir}/opensearch-performance-analyzer/opensearch_security.policy" >> %{config_dir}/jvm.options
   echo "--add-opens=jdk.attach/sun.tools.attach=ALL-UNNAMED" >> %{config_dir}/jvm.options
fi
# Reload systemctl daemon
if command -v systemctl > /dev/null; then
    systemctl daemon-reload
fi
# Reload other configs
if command -v systemctl > /dev/null; then
    systemctl restart systemd-sysctl.service || true
fi

if command -v systemd-tmpfiles > /dev/null; then
    systemd-tmpfiles --create %{name}.conf
fi

# Messages
echo "### NOT starting on installation, please execute the following statements to configure opensearch service to start automatically using systemd"
echo " sudo systemctl daemon-reload"
echo " sudo systemctl enable opensearch.service"
echo "### You can start opensearch service by executing"
echo " sudo systemctl start opensearch.service"
if [ -d %{product_dir}/plugins/opensearch-security ]; then
    echo "### Create opensearch demo certificates in %{config_dir}/"
    echo " See demo certs creation log in %{log_dir}/install_demo_configuration.log"
fi
exit 0

%preun
set -e
if command -v systemctl >/dev/null && systemctl is-active %{name}.service >/dev/null; then
    echo "Stop existing %{name}.service"
    systemctl --no-reload stop %{name}.service
fi
if command -v systemctl >/dev/null && systemctl is-active opensearch-performance-analyzer.service >/dev/null; then
    echo "Stop existing opensearch-performance-analyzer.service"
    systemctl --no-reload stop opensearch-performance-analyzer.service
fi
exit 0

%files
# Permissions
%defattr(-, %{name}, %{name})

# Root dirs/docs/licenses
%dir %{product_dir}
%doc %{product_dir}/NOTICE.txt
%doc %{product_dir}/README.md
%license %{product_dir}/LICENSE.txt
%{product_dir}/manifest.yml

# Config dirs/files
%dir %{config_dir}
%{config_dir}/jvm.options.d
%{config_dir}/opensearch-*
%config(noreplace) %{config_dir}/%{name}.yml
%config(noreplace) %{config_dir}/jvm.options
%config(noreplace) %{config_dir}/log4j2.properties
%config(noreplace) %{data_dir}/rca_enabled.conf
%config(noreplace) %{data_dir}/performance_analyzer_enabled.conf

# Service files
%attr(0644, root, root) %{_prefix}/lib/systemd/system/%{name}.service
%attr(0644, root, root) %{_prefix}/lib/systemd/system/opensearch-performance-analyzer.service
%attr(0644, root, root) %{_sysconfdir}/init.d/%{name}
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644, root, root) %config(noreplace) %{_prefix}/lib/sysctl.d/%{name}.conf
%attr(0644, root, root) %config(noreplace) %{_prefix}/lib/tmpfiles.d/%{name}.conf

# Main dirs
%{product_dir}/bin
%{product_dir}/jdk
%{product_dir}/lib
%{product_dir}/modules
%{product_dir}/performance-analyzer-rca
%{product_dir}/plugins
%{log_dir}
%{pid_dir}
%dir %{data_dir}

# Symlinks
%{product_dir}/data
%{product_dir}/logs

%changelog
* Mon Mar 21 2022 OpenSearch Team <opensearch@amazon.com>
- Initial package

