import os
import sys
import tempfile
from assemble_workflow.bundle import Bundle
from assemble_workflow.bundle_recorder import BundleRecorder
from manifests.build_manifest import BuildManifest

if (len(sys.argv) < 2):
    print("Build an OpenSearch Bundle")
    print("usage: assemble.sh /path/to/build_manifest")
    exit(1)


build_manifest_path = sys.argv[1]
build_manifest = BuildManifest.from_file(build_manifest_path)
build = build_manifest.build
artifacts_dir = os.path.dirname(os.path.realpath(build_manifest_path))
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
