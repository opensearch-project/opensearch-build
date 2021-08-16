import os

class IntegTestSuite:
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def execute(self, cluster):
        script = self.repo.dir + "/integtest.sh"
        if (os.path.exists(script)):
            print(f'sh {script} -b {cluster.endpoint()} -p {cluster.port()}')
            self.repo.execute(f'sh {script} -b {cluster.endpoint()} -p {cluster.port()}')
        else:
            print(f'{script} does not exist. Skipping integ tests for {self.name}')
