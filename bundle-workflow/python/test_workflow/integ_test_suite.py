import os

class IntegTestSuite:
    def __init__(self, name, repo, script_finder):
        self.name = name
        self.repo = repo
        self.script_finder = script_finder

    def execute(self, cluster):
        script = self.script_finder.find_integ_test_script(self.name, self.repo.dir)
        if (os.path.exists(script)):
            print(f'sh {script} -b {cluster.endpoint()} -p {cluster.port()}')
            self.repo.execute(f'sh {script} -b {cluster.endpoint()} -p {cluster.port()}')
        else:
            print(f'{script} does not exist. Skipping integ tests for {self.name}')
