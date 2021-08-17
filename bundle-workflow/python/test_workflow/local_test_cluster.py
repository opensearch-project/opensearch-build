import os
import tempfile
import urllib.request
import shutil
import subprocess
from test_workflow.test_cluster import TestCluster

class LocalTestCluster(TestCluster):
    def __init__(self, bundle_manifest):
        self.manifest = bundle_manifest
        self.work_dir = tempfile.TemporaryDirectory()

    def create(self):
        print(f'Creating local test cluster in {self.work_dir.name}')
        os.chdir(self.work_dir.name)
        print(f'Downloading bundle from {self.manifest.build.location}')
        urllib.request.urlretrieve(self.manifest.build.location, 'bundle.tgz')
        print(f'Downloaded bundle to {os.path.realpath("bundle.tgz")}')
        print('Unpacking')
        subprocess.check_call('tar -xzf bundle.tgz', shell = True)
        print('Unpacked')
        self.stdout = open('stdout.txt', 'w')
        self.stderr = open('stderr.txt', 'w')
        dir = f'opensearch-{self.manifest.build.version}'
        self.process = subprocess.Popen('./opensearch-tar-install.sh', cwd = dir, shell = True, stdout = self.stdout, stderr = self.stderr)
        print(f'Started OpenSearch with PID {self.process.pid}')

    def endpoint(self):
        return 'localhost'

    def port(self):
        return 9200

    def destroy(self):
        print(f'Sending SIGTERM to PID {self.process.pid}')
        self.process.terminate()
        try:
            print('Waiting for process to terminate')
            self.process.wait(10)
        except TimeoutExpired:
            print('Process did not terminate after 10 seconds. Sending SIGKILL')
            self.process.kill()
            try:
                print('Waiting for process to terminate')
                self.process.wait(10)
            except TimeoutExpired:
                print('Process failed to terminate even after SIGKILL')
                raise
        finally:
            print(f'Process terminated with exit code {self.process.returncode}')
            self.stdout.close()
            self.stderr.close()
            self.process = None
