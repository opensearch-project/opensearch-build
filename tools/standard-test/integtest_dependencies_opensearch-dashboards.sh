#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a temporary measure before we de-couple OpenSearch-Dashboards repo dependencies
# when building or integration testing Dashboards Plugins
# Assume this script is in the root directory of OpenSearch-Dashboards repository
# https://github.com/opensearch-project/OpenSearch-Dashboards
# And the environment already have the corresponding node and yarn version installed to use

yarn osd bootstrap

