# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.ci_check import CiCheckSource


class CiCheckGradlePublishToMavenLocal(CiCheckSource):
    def check(self) -> None:
        cmd = " ".join(
            [
                "./gradlew publishToMavenLocal",
                f"-Dopensearch.version={self.target.opensearch_version}",
                f"-Dbuild.snapshot={str(self.target.snapshot).lower()}",
            ]
        )

        self.git_repo.execute(cmd)
