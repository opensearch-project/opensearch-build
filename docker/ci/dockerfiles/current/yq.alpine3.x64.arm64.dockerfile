# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This docker image is based on yq docker image, but with additional pkgs for specific uses.
# We didnt add yq to other build image because:
# 1. We want to keep the image as slim as possible for specific use case.
# 2. It is not easy to install yq as it is not part of default package manager repositories on RHEL/Ubuntu
# 3. Alpine can install yq with apk from the get go, and does not have the official yq image entrypoint
#    which will cause jenkins to not able to `cat` and hold the container.
# Thanks.

FROM alpine:3

USER 0

# Install pkgs
RUN apk update && apk upgrade && apk add git yq bash

# User opensearch
RUN set -eux; \
  addgroup -g 1000 opensearch; \
  adduser -u 1000 -G opensearch -s /bin/bash -h /home/opensearch -D opensearch

USER 1000
