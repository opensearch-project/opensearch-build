# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import shutil
from zipfile import ZipFile

import yaml
from jproperties import Properties  # type: ignore

from manifests.build_manifest import BuildManifest


class BuildRecorder:
    class ArtifactInvalidError(Exception):
        def __init__(self, path, message):
            self.path = path
            super().__init__(
                f"Artifact {os.path.basename(path)} is invalid: {message}."
            )

    class PropertiesFile(Properties):
        def __init__(self, filename, data):
            super().__init__(self)
            self.filename = filename
            self.load(data)

        def get_value(self, key, default_value=None):
            try:
                return self[key].data
            except KeyError:
                return default_value

        def check_value(self, key, expected_value):
            try:
                value = self[key].data
                if value != expected_value:
                    raise BuildRecorder.ArtifactInvalidError(
                        self.filename,
                        f"expected to have {key}={expected_value}, but was {value}",
                    )
            except KeyError:
                raise BuildRecorder.ArtifactInvalidError(
                    self.filename,
                    f"expected to have {key}={expected_value}, but none was found",
                )

        def check_value_in(self, key, expected_values):
            try:
                value = self[key].data
                if value not in expected_values:
                    raise BuildRecorder.ArtifactInvalidError(
                        self.filename,
                        f"expected to have {key}=any of {expected_values}, but was {value}",
                    )
            except KeyError:
                if None not in expected_values:
                    raise BuildRecorder.ArtifactInvalidError(
                        self.filename,
                        f"expected to have {key}=any of {expected_values}, but none was found",
                    )

    def __init__(self, build_id, output_dir, name, version, arch, snapshot):
        self.output_dir = output_dir
        self.version = str(version)
        self.opensearch_version = (
            self.version + "-SNAPSHOT" if snapshot else self.version
        )
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        self.component_version = (
            self.version + ".0-SNAPSHOT" if snapshot else f"{self.version}.0"
        )
        self.build_manifest = self.BuildManifestBuilder(
            build_id, name, self.opensearch_version, arch, snapshot
        )

    def record_component(self, component_name, git_repo):
        self.build_manifest.append_component(
            component_name,
            self.component_version,
            git_repo.url,
            git_repo.ref,
            git_repo.sha,
        )

    def record_artifact(
        self, component_name, artifact_type, artifact_path, artifact_file
    ):
        print(
            f"Recording {artifact_type} artifact for {component_name}: {artifact_path} (from {artifact_file})"
        )
        # Ensure the target directory exists
        dest_file = os.path.join(self.output_dir, artifact_path)
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)
        # Check artifact
        self.__check_artifact(artifact_type, artifact_file)
        # Copy the file
        shutil.copyfile(artifact_file, dest_file)
        # Notify the recorder
        self.build_manifest.append_artifact(
            component_name, artifact_type, artifact_path
        )

    def get_manifest(self):
        return self.build_manifest.to_manifest()

    def write_manifest(self, dest_dir):
        output_manifest = self.get_manifest()
        manifest_path = os.path.join(dest_dir, "manifest.yml")
        with open(manifest_path, "w") as file:
            yaml.dump(output_manifest.to_dict(), file)

    def __check_artifact(self, artifact_type, artifact_file):
        if artifact_type == "plugins":
            self.__check_plugin_artifact(artifact_file)
        elif artifact_type == "maven":
            self.__check_maven_artifact(artifact_file)

    def __check_plugin_artifact(self, artifact_file):
        if os.path.splitext(artifact_file)[1] != ".zip":
            raise BuildRecorder.ArtifactInvalidError(artifact_file, "not a zip file")
        if not artifact_file.endswith(f"-{self.component_version}.zip"):
            raise BuildRecorder.ArtifactInvalidError(
                artifact_file, f"expected filename to include {self.component_version}"
            )
        with ZipFile(artifact_file, "r") as zip:
            data = zip.read("plugin-descriptor.properties").decode("UTF-8")
            properties = BuildRecorder.PropertiesFile(artifact_file, data)
            properties.check_value("version", self.component_version)
            properties.check_value("opensearch.version", self.version)
            print(f'Checked {artifact_file} ({properties.get_value("version", "N/A")})')

    def __check_maven_artifact(self, artifact_file):
        ext = os.path.splitext(artifact_file)[1]
        if ext not in [
            ".jar",
            ".asc",
            ".md5",
            ".sha1",
            ".pom",
            ".xml",
            ".sha1",
            ".sha256",
            ".sha512",
            ".module",
            ".zip",
            ".war",
        ]:
            raise BuildRecorder.ArtifactInvalidError(
                artifact_file, f"{ext} is not a valid extension for a maven file"
            )
        if os.path.splitext(artifact_file)[1] == ".jar":
            with ZipFile(artifact_file, "r") as zip:
                data = zip.read("META-INF/MANIFEST.MF").decode("UTF-8")
                properties = BuildRecorder.PropertiesFile(artifact_file, data)
                properties.check_value_in(
                    "Implementation-Version",
                    [self.component_version, self.opensearch_version, None],
                )
                print(
                    f'Checked {artifact_file} ({properties.get_value("Implementation-Version", "N/A")})'
                )

    class BuildManifestBuilder:
        def __init__(self, build_id, name, version, arch, snapshot):
            self.data = {}
            self.data["build"] = {}
            self.data["build"]["id"] = build_id
            self.data["build"]["name"] = name
            self.data["build"]["version"] = version
            self.data["build"]["architecture"] = arch
            self.data["build"]["snapshot"] = str(snapshot).lower()
            self.data["schema-version"] = "1.0"
            # We need to store components as a hash so that we can append artifacts by component name
            # When we convert to a BuildManifest this will get converted back into a list
            self.data["components_hash"] = {}

        def append_component(self, name, version, repository_url, ref, commit_id):
            component = {
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "artifacts": {},
                "version": version,
            }
            self.data["components_hash"][name] = component

        def append_artifact(self, component, type, path):
            artifacts = self.data["components_hash"][component]["artifacts"]
            list = artifacts.get(type, [])
            if len(list) == 0:
                artifacts[type] = list
            list.append(path)

        def to_manifest(self):
            # The build manifest expects `components` to be a list, not a hash, so we need to munge things a bit
            components = self.data["components_hash"].values()
            self.data["components"] = components
            return BuildManifest(self.data)
