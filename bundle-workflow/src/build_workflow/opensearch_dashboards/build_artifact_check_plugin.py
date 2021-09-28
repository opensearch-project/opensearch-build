# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import re

from build_workflow.build_artifact_check import BuildArtifactCheck


class BuildArtifactOpenSearchDashboardsCheckPlugin(BuildArtifactCheck):
    def check(self, path):
        if os.path.splitext(path)[1] != ".zip":
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, "Not a zip file.")
        version = re.sub(r'-SNAPSHOT$', '', self.target.opensearch_version)
        if not path.endswith(f"-{version}.zip"):
            raise BuildArtifactCheck.BuildArtifactInvalidError(
                path, f"Expected filename to include {version}."
            )
