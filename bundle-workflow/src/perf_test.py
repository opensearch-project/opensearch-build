import argparse
import os

import yaml

from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.perf_test_cluster import PerformanceTestCluster
from test_workflow.perf_test_suite import PerformanceTestSuite

parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
parser.add_argument('manifest', type=argparse.FileType('r'), help="Manifest file.")
parser.add_argument('--keep', dest='keep', action='store_true', help="Do not delete the working temporary directory.")
parser.add_argument('--stack', dest='stack', help='Stack name for performance test')
parser.add_argument('config', type=argparse.FileType('r'), help="Config file.")
parser.add_argument("-t", '--token', help="Github Token")

args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)

config = yaml.load(args.config, Loader=yaml.FullLoader)

workspace = os.getcwd()


with TemporaryDirectory(keep=args.keep) as work_dir:
    os.chdir(work_dir)
    current_workspace = os.path.join(workspace, 'infra56')
    cloned_repo = GitRepository(f'https://{args.token}:x-oauth-basic@github.com/opensearch-project/opensearch-infra', 'main', current_workspace)
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
        perf_cluster.destroy()
