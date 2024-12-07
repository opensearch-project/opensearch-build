# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from manifests.test_manifest import TestManifest
from test_workflow.smoke_test.smoke_test_runner import SmokeTestRunner
from test_workflow.smoke_test.smoke_test_runner_opensearch import SmokeTestRunnerOpenSearch
from test_workflow.test_args import TestArgs


class SmokeTestRunners:
    RUNNERS = {
        "OpenSearch": SmokeTestRunnerOpenSearch
    }

    @classmethod
    def from_test_manifest(cls, args: TestArgs, test_manifest: TestManifest) -> SmokeTestRunner:
        return cls.RUNNERS[test_manifest.name](args, test_manifest)
