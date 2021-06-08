#!/bin/bash
# This is necessary for servers that try to run OpenSearch with docker
# The hosts have to have these settings ready
# Or the OpenSearch Process will not run
sudo sysctl -w vm.max_map_count=262144
ulimit -n 65535
# Required for PA and similar processes that require shared memory to work
sudo chmod -R 777 /dev/shm

# As for docker the host must have these as well in /etc/sysconfig/docker and restart service
# OPTIONS="--default-ulimit nofile=65535:65535"
# to replace the default limits of 1024:4096
