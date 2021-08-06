import os

class IntegTestSuite:
    def __init__(self, name, repo):
        self._name = name
        self._repo = repo

    def execute(self, cluster):
        script = self._repo.dir() + "/integtest.sh"
        if (os.path.exists(script)):
            repo.execute(f'sh integtest.sh -b {cluster.endpoint()} -p {cluster.port()}')
        else:
            print(f'{script} does not exist. Skipping integ tests for {self._name}')
