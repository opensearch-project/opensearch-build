#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

# This is a temporary measure before we de-couple OpenSearch-Dashboards repo dependencies
# when building or integration testing Dashboards Plugins
# Assume this script is in the root directory of OpenSearch-Dashboards repository
# https://github.com/opensearch-project/OpenSearch-Dashboards
# And the environment already have the corresponding node and yarn version installed to use

yarn osd bootstrap

