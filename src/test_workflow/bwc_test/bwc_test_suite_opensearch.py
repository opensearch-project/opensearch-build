# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path
from typing import Any

from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestComponent
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite
from test_workflow.test_recorder.test_recorder import TestRecorder


class BwcTestSuiteOpenSearch(BwcTestSuite):

    def __init__(
        self,
        work_dir: Path,
        component: Any,
        test_config: TestComponent,
        test_recorder: TestRecorder,
        manifest: BundleManifest
    ) -> None:
        super().__init__(
            work_dir,
            component,
            test_config,
            test_recorder,
            manifest
        )

    # TODO: enable OpenSearch scripts to accept more arguments
    def get_cmd(self, script: str, security: bool, manifest_build_location: str) -> str:
        return script

    @property
    def test_artifact_files(self) -> dict:
        return {
            "opensearch-bwc-test": os.path.join(self.repo_work_dir, "build", "reports", "tests", "bwcTest")
        }
