# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for setting up systemd env base for services with root user
# It is initially designed to test yum installation, but can be used for anything that requires systemd
# It used the method posted by Daniel Walsh: https://developers.redhat.com/blog/2014/05/05/running-systemd-within-docker-container

# In order to run images with systemd, you need to run in privileged mode: `docker run --privileged -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro <image_tag>`
# If you use this image in jenkins pipeline you need to add these arguments: `args '--entrypoint=/usr/sbin/init -u root --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro'`

FROM rockylinux:8

ENV container docker

RUN dnf -y update && yum clean all

# Possible retain of multi-user.target.wants later due to PA
# As of now we do not need this
RUN dnf -y install systemd procps util-linux-ng openssl openssl-devel which curl git gnupg2 tar net-tools jq && dnf clean all && \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

CMD ["/usr/sbin/init"]
