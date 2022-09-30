# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path

from manifests.build_manifest import BuildComponent
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestComponent
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite
from test_workflow.test_recorder.test_recorder import TestRecorder


class BwcTestSuiteOpenSearchDashboards(BwcTestSuite):

    def __init__(
        self,
        work_dir: Path,
        component: BuildComponent,
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

    def get_cmd(self, script: str, security: bool, manifest_build_location: str) -> str:
        return f"{script} -s {str(security).lower()} -d {manifest_build_location}"

    @property
    def test_artifact_files(self) -> dict:
        return {
            "cypress-videos": os.path.join(self.repo_work_dir, "bwc_tmp", "test", "cypress", "videos"),
            "cypress-screenshots": os.path.join(self.repo_work_dir, "bwc_tmp", "test", "cypress", "screenshots"),
            "cypress-report": os.path.join(self.repo_work_dir, "bwc_tmp", "test", "cypress", "results"),
        }
