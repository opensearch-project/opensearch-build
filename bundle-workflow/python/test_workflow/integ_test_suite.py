import os


class IntegTestSuite:
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def execute(self, cluster):
        script = self.repo.dir.name + "/integtest.sh"
        if (os.path.exists(script)):
            print(f'sh integtest.sh -b {cluster.endpoint()} -p {cluster.port()}')
        #            repo.execute(f'sh integtest.sh -b {cluster.endpoint()} -p {cluster.port()}')
        else:
            print(f'{script} does not exist. Skipping integ tests for {self.name}')
