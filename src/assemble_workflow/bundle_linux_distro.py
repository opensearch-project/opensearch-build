# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from assemble_workflow.bundle_linux_deb import BundleLinuxDeb
from assemble_workflow.bundle_linux_rpm import BundleLinuxRpm
from manifests.build_manifest import BuildManifest


class BundleLinuxDistro:

    def __init__(self, filename: str, package_path: str, min_path: str) -> None:
        self.filename = filename
        self.package_path = package_path
        self.min_path = min_path

    def extract(self, extension: str, dest: str) -> None:
        if extension == "deb":
            BundleLinuxDeb(self.filename, self.package_path, self.min_path).extract(dest)
        elif extension == "rpm":
            BundleLinuxRpm(self.filename, self.package_path, self.min_path).extract(dest)

    def build(self, extension: str, name: str, dest: str, archive_path: str, build_cls: BuildManifest.Build) -> None:
        if extension == "deb":
            BundleLinuxDeb(self.filename, self.package_path, self.min_path).build(name, dest, archive_path, build_cls)
        elif extension == "rpm":
            BundleLinuxRpm(self.filename, self.package_path, self.min_path).build(name, dest, archive_path, build_cls)
