# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys
import os
import logging
from typing import Any


from manifests.test_manifest import TestManifest
from system import console
from report_workflow.report_args import ReportArgs
from manifests.test_run_manifest import TestRunManifest, TestComponent

class TestRunComponent:
    name: str




    def __init__(self, args: ReportArgs, component:TestComponent) -> None:
        self.name = component.name


