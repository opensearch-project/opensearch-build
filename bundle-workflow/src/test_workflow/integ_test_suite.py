# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os


class IntegTestSuite:
    def __init__(self, name, repo, script_finder):
        self.name = name
        self.repo = repo
        self.script_finder = script_finder

    def execute(self, cluster, security):
        script = self.script_finder.find_integ_test_script(self.name, self.repo.dir)
        if os.path.exists(script):
            self.repo.execute(
                f"sh {script} -b {cluster.endpoint()} -p {cluster.port()} -s {str(security).lower()}"
            )
        else:
            print(f"{script} does not exist. Skipping integ tests for {self.name}")
