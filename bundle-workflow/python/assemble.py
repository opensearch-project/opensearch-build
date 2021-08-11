import os
import tempfile
import argparse
from assemble_workflow.bundle import Bundle
from assemble_workflow.bundle_recorder import BundleRecorder
from manifests.build_manifest import BuildManifest

parser = argparse.ArgumentParser(description = "Assembly an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
args = parser.parse_args()

build_manifest = BuildManifest.from_file(args.manifest)
build = build_manifest.build
artifacts_dir = os.path.dirname(os.path.realpath(args.manifest))
output_dir = os.path.join(os.getcwd(), 'bundle')
os.makedirs(output_dir, exist_ok=True)

with tempfile.TemporaryDirectory() as work_dir:
    print(f'Bundling {build.name} ({build.architecture}) into {output_dir} ...')

    os.chdir(work_dir)

    bundle_recorder = BundleRecorder(build, output_dir, artifacts_dir)
    bundle = Bundle(build_manifest, artifacts_dir, bundle_recorder)

    bundle.install_plugins()
    print(f'Installed plugins: {bundle.installed_plugins}')

    #  Save a copy of the manifest inside of the tar
    bundle_recorder.write_manifest(bundle.archive_path)
    bundle.build_tar(output_dir)

    bundle_recorder.write_manifest(output_dir)

print(f'Done.')
