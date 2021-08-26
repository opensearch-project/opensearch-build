import argparse
import os

import yaml

from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_cluster import PerformanceTestCluster
from test_workflow.perf_test_suite import PerformanceTestSuite

parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
parser.add_argument('manifest', type=argparse.FileType('r'), help="Manifest file.")
parser.add_argument('--stack', dest='stack', help='Stack name for performance test')
parser.add_argument('config', type=argparse.FileType('r'), help="Config file.")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)

config = yaml.load(args.config, Loader=yaml.FullLoader)


def get_repo_url():
    if "GITHUB_TOKEN" in os.environ:
        return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-infra.git"
    return "https://github.com/opensearch-project/opensearch-infra.git"


os.chdir(os.getcwd())
current_workspace = os.path.join(os.getcwd(), 'infra')
cloned_repo = GitRepository(get_repo_url(), 'main', current_workspace)
security = False
for component in manifest.components:
    if component.name == 'security':
        security = True
os.chdir(current_workspace)
perf_cluster = PerformanceTestCluster(manifest, config, args.stack, security)
try:
    perf_cluster.create()

    # IP of the cluster
    endpoint = perf_cluster.endpoint()
    os.chdir(current_workspace)
    perf_test_suite = PerformanceTestSuite(manifest, endpoint, security)
    perf_test_suite.execute()
except:
    os.chdir(current_workspace)
    perf_cluster.destroy()
