# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from paths.script_finder import ScriptFinder
from paths.tree_walker import walk
from system.execute import execute


class IntegTestSuite:
    def __init__(self, name, repo, test_recorder):
        self.name = name
        self.repo = repo
        self.test_recorder = test_recorder

    def execute(self, cluster, security):
        script = ScriptFinder.find_integ_test_script(self.name, self.repo.dir)
        if (os.path.exists(script)):
            cmd = f'sh {script} -b {cluster.endpoint()} -p {cluster.port()} -s {str(security).lower()}'
            (status, stdout, stderr) = execute(cmd, self.repo.dir, True, False)
            results_dir = os.path.join(self.repo.dir,
                                       'integ-test',
                                       'build',
                                       'reports',
                                       'tests',
                                       'integTest')
            self.test_recorder.record_integ_test_outcome(self.name, status, stdout, stderr, walk(results_dir))
        else:
            print(f"{script} does not exist. Skipping integ tests for {self.name}")
