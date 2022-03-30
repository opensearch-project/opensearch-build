# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import subprocess

from manifests.build_manifest import BuildManifest
from system.os import rpm_architecture


class BundleRpm:

    def __init__(self, filename: str, package_path: str, min_path: str) -> None:
        self.filename = filename
        self.package_path = package_path
        self.min_path = min_path

    def extract(self, dest: str) -> None:
        cpio_basename = os.path.splitext(os.path.basename(self.package_path))[0]
        cpio_path = os.path.join(dest, f"{cpio_basename}.cpio")
        min_source_path = os.path.join(dest, 'usr', 'share', self.filename)
        min_dest_path = os.path.join(dest, self.min_path)
        min_config_path = os.path.join(dest, 'etc', self.filename)
        min_bin_env_path = os.path.join(min_dest_path, 'bin', f"{self.filename}-env")

        # Convert rpm to cpio so we can extract the content
        logging.info(f"Convert rpm to cpio for extraction: {self.package_path} to {cpio_path}")
        with open(cpio_path, 'wb') as fp:
            subprocess.check_call(
                [
                    'rpm2cpio',
                    self.package_path,
                ],
                stdout=fp,
                cwd=dest,
            )

        # Extract cpio archive based on the rpm package
        logging.info(f"Extract cpio {cpio_path} content to {dest}")
        with open(cpio_path, 'rb') as fp:
            subprocess.check_call(
                [
                    'cpio',
                    '-imdv',
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

        if os.path.exists(min_bin_env_path):
            # Backup original file
            shutil.copy2(min_bin_env_path, f"{min_bin_env_path}.backup")
            # Prevent sourcing as file is only in place after rpm installation
            # So that min can install plugin zips
            # Have to decode then encode back to ascii due to mypy complains TextIO not equals to BinaryIO
            with open(min_bin_env_path, 'rb') as fp:
                min_bin_env_lines = fp.read().decode('ascii')

            with open(min_bin_env_path, 'wb') as fp:
                fp.write(min_bin_env_lines.replace('source', '#source').encode('ascii'))

    def build(self, name: str, dest: str, archive_path: str, build_cls: BuildManifest.Build) -> None:
        # extract dest and build dest are not the same, this is restoring the extract dest
        # mainly due to rpm requires several different setups compares to tarball and zip
        ext_dest = os.path.dirname(archive_path)
        min_source_path = os.path.join(ext_dest, 'usr', 'share', self.filename)
        min_dest_path = os.path.join(ext_dest, self.min_path)
        min_bin_env_path = os.path.join(min_dest_path, 'bin', f"{self.filename}-env")
        bundle_artifact_path: str = None

        # Remove env var
        logging.info('Organize folder structure before generating rpm')
        os.environ.pop('OPENSEARCH_PATH_CONF', None)

        # Restore config file and core folder to original location
        if os.path.exists(f"{min_bin_env_path}.backup"):
            logging.info(f"Restore {min_bin_env_path}.backup to {min_bin_env_path}")
            shutil.move(f"{min_bin_env_path}.backup", min_bin_env_path)

        shutil.move(min_dest_path, min_source_path)

        # Run bundle rpmbuild
        bundle_cmd = " ".join(
            [
                'rpmbuild',
                '-bb',
                f"--define '_topdir {ext_dest}'",
                f"--define '_version {build_cls.version}'",
                f"--define '_architecture {rpm_architecture(build_cls.architecture)}'",
                f"{self.filename}.rpm.spec",
            ]
        )

        logging.info(f"Execute {bundle_cmd} in {ext_dest}")
        subprocess.check_call(bundle_cmd, cwd=ext_dest, shell=True)

        # Move artifact to repo root before being published to {dest}
        for dirpath, dirnames, filenames in os.walk(os.path.join(ext_dest, 'RPMS')):
            for filename in [file for file in filenames if file.endswith('.rpm')]:
                bundle_artifact_path = os.path.join(dirpath, filename)
                break

        shutil.move(bundle_artifact_path, name)
