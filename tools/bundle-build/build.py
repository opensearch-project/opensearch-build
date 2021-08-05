import os
import sys
import tempfile
import urllib.request
from lib.manifest import BuildManifest

if (len(sys.argv) < 2):
    print("Build an OpenSearch Bundle")
    print("usage: build.sh /path/to/manifest")
    exit(1)

with tempfile.TemporaryDirectory() as work_dir:
    manifest = BuildManifest.from_file(sys.argv[1])
    build = manifest.build()
    print("Building " + build.name() + " (" + build.arch() + ")")

    os.chdir(work_dir)

    for component in manifest.components():
        print("=== Building " + component.name() + " ...")
        component.checkout()
        component.build(build.version(), build.arch())
