import os

from paths.tree_walker import walk
from system.execute import execute


class IntegTestSuite:
    def __init__(self, name, repo, script_finder, test_recorder):
        self.name = name
        self.repo = repo
        self.script_finder = script_finder
        self.test_recorder = test_recorder

    def execute(self, cluster, security):
        script = self.script_finder.find_integ_test_script(self.name, self.repo.dir)
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
