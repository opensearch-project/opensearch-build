# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.manifest import Manifest


class Component:
    def __init__(self, name, repo, snapshot=False, checks=[]):
        self.name = name
        self.git_repo = repo
        self.snapshot = snapshot
        self.checks = checks

    @classmethod
    def gradle_cmd(self, target, props={}):
        cmd = [f"./gradlew {target}"]
        cmd.extend([f"-D{k}={v}" for k, v in props.items()])
        return " ".join(cmd)

    def to_dict(self):
        return Manifest.compact(
            {
                "name": self.name,
                "repository": self.git_repo.url,
                "ref": self.git_repo.ref,
                "checks": self.checks,
            }
        )
