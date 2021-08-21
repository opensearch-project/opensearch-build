#!/usr/bin/env python

import os
import argparse
import sys
import subprocess

from manifests.bundle_manifest import BundleManifest
from git.git_repository import GitRepository
from test_workflow.local_test_cluster import LocalTestCluster
from test_workflow.integ_test_suite import IntegTestSuite
from paths.script_finder import ScriptFinder
from system.temporary_directory import TemporaryDirectory


def parse_arguments():
    parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
    parser.add_argument('--manifest', type = argparse.FileType('r'), help="Manifest file.")
    parser.add_argument('--keep', dest = 'keep', action='store_true', help = "Do not delete the working temporary directory.")
    args = parser.parse_args()
    return args

#TODO read from configuration file
def is_component_test_supported(component):
    if component.name == 'OpenSearch':
        return True
    else:
        return False

def execute_shell(command, work_dir):
    return subprocess.check_output(command, cwd = work_dir, shell = True)

def pull_component(component, work_dir):
    GitRepository(component.repository, component.commit_id, os.path.join(work_dir, component.name))

def run_tests(work_dir):
    bwc_script = "bwctest.sh"
    change_ownership = f"chmod +x {bwc_script}"
    run_bwctests = f"./{bwc_script}"
    execute_shell(change_ownership, work_dir)
    output = execute_shell(run_bwctests, work_dir)
    return output

def main():
    args = parse_arguments()
    manifest = BundleManifest.from_file(args.manifest)
    # TODO copy all maven dependencies from S3 to local
    with TemporaryDirectory(keep=args.keep) as work_dir:
        os.chdir(work_dir)
        # For each component, check out the git repo and run `bwctest.sh`
        for component in manifest.components:
            # check if component is supported
            if not is_component_test_supported(component):
                #print('Skipping tests for %s, as it is currently not supported' % component.name)
                continue
            pull_component(component, work_dir)
            console_output = run_tests(work_dir + "/" + component.name)
        # TODO: Store test results, send notification via {console_output}


if __name__ == '__main__':
    sys.exit(main())