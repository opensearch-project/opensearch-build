# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import subprocess
from typing import List

from manifests.build_manifest import BuildManifest
from system.os import deb_architecture


class BundleLinuxDeb:

    def __init__(self, filename: str, package_path: str, min_path: str) -> None:
        self.filename = filename
        self.package_path = package_path
        self.min_path = min_path

    def changelog_content(self, version: str) -> List[str]:
        # In the changelog content we are dynamically generate this part for now.
        # Instead of 'UNRELEASED' its possible to use 'stable'
        # which will use gpg to sign with the given from 'OpenSearch Team <opensearch@amazon.com>'
        # Debian official documentation suggest using 'unstable' to replace 'UNRELEASED'
        # but it is still asking a key to sign during build, therefore use 'UNRELEASED' here
        # as part of changelog content only
        # https://www.debian.org/doc/manuals/maint-guide/update.en.html

        return [
            f"{self.filename} ({version}) UNRELEASED; urgency=low",
            "",
            "  * Initial release.",
            "",
            " -- OpenSearch Team <opensearch@amazon.com>  Fri, 14 Oct 2022 10:06:23 +0000"
        ]

    def generate_changelog_file(self, dest: str, version: str) -> None:
        changelog_path = os.path.join(dest, 'debian', 'changelog')
        logging.info(f"Write debian changelog to: {changelog_path}")

        with open(changelog_path, 'w') as file:
            for line in self.changelog_content(version):
                file.write(f"{line}\n")

    def extract(self, dest: str) -> None:
        data_path = os.path.join(dest, "data.tar.gz")
        min_source_path = os.path.join(dest, 'usr', 'share', self.filename)
        min_dest_path = os.path.join(dest, self.min_path)
        min_config_path = os.path.join(dest, 'etc', self.filename)

        # Extract data.tar.gz from deb so we can extract the content
        logging.info(f"Extract data.tar.gz from deb for extraction: {self.package_path} to {data_path}")
        with open(data_path, 'wb') as fp:
            subprocess.check_call(
                [
                    'ar',
                    '-xf',
                    self.package_path,
                    'data.tar.gz'
                ],
                stdout=fp,
                cwd=dest,
            )

        # Extract data.tar.gz archive based on the deb package
        logging.info(f"Extract data.tar.gz content to {dest}")
        with open(data_path, 'rb') as fp:
            subprocess.check_call(
                [
                    'tar',
                    '-zvxf',
                    '-'
                ],
                stdin=fp,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                cwd=dest,
            )

        # Move core folder destination so plugin install can proceed
        logging.info(f"Move {min_source_path} to {min_dest_path} for plugin installation")
        shutil.move(min_source_path, min_dest_path)

        # Multiple modifications and env vars setups before install plugins
        # As bin/opensearch-env is different between archive and package
        # https://github.com/opensearch-project/OpenSearch/issues/2092
        os.environ[f"{self.filename.upper()}_PATH_CONF"] = min_config_path

    def build(self, name: str, dest: str, archive_path: str, build_cls: BuildManifest.Build) -> None:
        # extract dest and build dest are not the same, this is restoring the extract dest
        # mainly due to deb requires several different setups compares to tarball and zip
        ext_dest = os.path.dirname(archive_path)
        min_source_path = os.path.join(ext_dest, 'usr', 'share', self.filename)
        min_dest_path = os.path.join(ext_dest, self.min_path)
        bundle_artifact_path: str = None

        # Remove env var
        logging.info('Organize folder structure before generating deb')
        os.environ.pop('OPENSEARCH_PATH_CONF', None)

        logging.info(f"Move {min_dest_path} to {min_source_path} for building the debian package")
        shutil.move(min_dest_path, min_source_path)

        deb_version = build_cls.version.replace('-', '.')
        self.generate_changelog_file(ext_dest, deb_version)

        bundle_cmd = " ".join(
            [
                'debmake',
                '--fullname "OpenSearch Team"',
                '--email "opensearch@amazon.com"',
                '--invoke debuild',
                f'--package {self.filename}',
                '--native',
                '--revision 1',
                f"--upstreamversion {deb_version}"
            ]
        )

        logging.info(f"Execute {bundle_cmd} in {ext_dest}")
        subprocess.check_call(bundle_cmd, cwd=ext_dest, shell=True)

        # Move artifact to repo root before being published to {dest}
        # In debuild, the final package is created in the parent directory of the sources
        # https://github.com/opensearch-project/opensearch-build/issues/4532#issuecomment-2091726868
        bundle_artifact_path = f"/tmp/{self.filename}_{deb_version}_{deb_architecture(build_cls.architecture)}.deb"
        logging.info(f"Found deb file: {bundle_artifact_path}")
        shutil.move(bundle_artifact_path, name)
