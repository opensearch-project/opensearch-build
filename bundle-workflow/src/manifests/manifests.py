# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os
import re

from sortedcontainers import SortedDict  # type: ignore

from git.git_repository import GitRepository
from manifests.input_manifest import InputManifest
from system.properties_file import PropertiesFile
from system.temporary_directory import TemporaryDirectory


class Manifests(SortedDict):
    def __init__(self):
        super(Manifests, self).__init__()
        self.__discover()

    @property
    def manifests_path(self):
        return os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../../manifests")
        )

    def __discover(self):
        for filename in glob.glob(
            os.path.join(self.manifests_path, "opensearch-*.yml")
        ):
            logging.debug(f"Checking {filename}")
            match = re.search(r"^opensearch-([0-9.]*).yml$", os.path.basename(filename))
            if match:
                version = match.group(1)
                manifest = InputManifest.from_path(filename)
                logging.debug(f"Loaded {version} ({manifest.to_int()}) from {filename}")
                self.__setitem__(version, manifest)

    @property
    def versions(self):
        return list(map(lambda manifest: manifest.build.version, self.values()))

    @property
    def last(self):
        # use the latest manifest
        if len(self) == 0:
            raise RuntimeError("No manifests found")

        return self.values()[-1]

    def update(self):
        known_versions = self.versions
        logging.info(f"Known versions: {known_versions}")
        main_versions = {}
        with TemporaryDirectory() as work_dir:
            logging.info(f"Checking out components into {work_dir}")
            os.chdir(work_dir)
            manifest = self.last
            for component in manifest.components:
                logging.info(f"Checking out {component.name}#main")
                repo = GitRepository(
                    component.repository,
                    "main",
                    os.path.join(work_dir, component.name),
                    component.working_directory,
                )

                try:
                    # if OpenSearch incremented the version first, this is expected to fail
                    # if the component incremented the version first, it depends on an older version and will succeed

                    # HACK: publish to maven local until we have working Maven
                    if component.name in ["OpenSearch", "common-utils"]:
                        cmd = " ".join(
                            [
                                "./gradlew publishToMavenLocal",
                                f"-Dopensearch.version={manifest.build.version}-SNAPSHOT"
                                if component.name != "OpenSearch"
                                else "",
                                "-Dbuild.snapshot=false",
                            ]
                        )
                        # repo.execute_silent(cmd)

                    # collect properties
                    cmd = " ".join(
                        [
                            "./gradlew properties",
                            f"-Dopensearch.version={manifest.build.version}-SNAPSHOT"
                            if component.name != "OpenSearch"
                            else "",
                            "-Dbuild.snapshot=false",
                        ]
                    )

                    properties = PropertiesFile(repo.output(cmd))
                    version = properties.get_value("version")
                    if version:
                        release_version = ".".join(version.split(".")[:3])
                        logging.info(
                            f"Found version {release_version} (from {version}) in {component.name}"
                        )
                        if release_version not in main_versions.keys():
                            main_versions[release_version] = []
                        main_versions[release_version].append(component)
                except Exception:
                    logging.warn(f"Error building {component.name}, ignored.")

        logging.info("Found versions on main:")
        for main_version in main_versions.keys():
            for component in main_versions[main_version]:
                logging.info(f" {component.name}={main_version}")
        for release_version in main_versions.keys() - known_versions:
            logging.info(f"Creating new version: {release_version}")
            data = {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch", "version": release_version},
                "components": [],
            }
            # TODO: was this an increment from a component?
            # if so, copy OpenSearch and common-utils from the previous manifest
            for component in main_versions[release_version]:
                logging.info(f" Adding {component.name}")
                data["components"].append(
                    {
                        "name": component.name,
                        "repository": component.repository,
                        "ref": "main",
                    }
                )
            manifest = InputManifest(data)
            manifest_path = os.path.join(
                self.manifests_path, f"opensearch-{release_version}.yml"
            )
            manifest.to_file(manifest_path)
            logging.info(f"Wrote {manifest_path}")
