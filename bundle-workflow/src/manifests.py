#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from manifests_workflow.input_manifests import InputManifests
from manifests_workflow.manifests_args import ManifestsArgs
from system import console

args = ManifestsArgs()
console.configure(level=args.logging_level)
manifests = InputManifests()

if args.action == "list":
    for manifest in manifests.values():
        logging.info(f"{manifest.build.name} {manifest.build.version}")
elif args.action == "update":
    manifests.update()

logging.info("Done.")
