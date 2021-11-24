# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import errno
import logging
import os
import shutil
import subprocess
import tarfile
import zipfile
from abc import ABC, abstractmethod

from system.zip_file import ZipFile


class Dist(ABC):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @abstractmethod
    def __extract__(self, dest):
        pass

    @abstractmethod
    def get_distribution(self):
        pass

    def extract(self, dest):
        self.__extract__(dest)

        # OpenSearch & Dashboard tars will include only a single folder at the top level of the tar.

        for file in os.scandir(dest):
            if file.is_dir():
                self.archive_path = file.path
                return self.archive_path

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(dest, "*"))

    def build(self, bundle_recorder, dest):
        name = bundle_recorder.package_name
        self.__build__(bundle_recorder, dest)
        path = os.path.join(dest, name)
        shutil.copyfile(name, path)
        logging.info(f"Published {path}.")

    @classmethod
    def create_dist(cls, name, path, distribution):
        DISTRIBUTIONS = {
            "rpm": DistRpm(name, path),
            "tar": DistTar(name, path),
            "zip": DistZip(name, path),
        }
        if distribution not in DISTRIBUTIONS:
            raise ValueError("Distribution not specified or invalid distribution")
        else:
            return DISTRIBUTIONS[distribution]


class DistZip(Dist):
    def __extract__(self, dest):
        with ZipFile(self.path, "r") as zip:
            zip.extractall(dest)

    def __build__(self, bundle_recorder, dest):
        with ZipFile(bundle_recorder.package_name, "w", zipfile.ZIP_DEFLATED) as zip:
            rootlen = len(self.archive_path) + 1
            for base, dirs, files in os.walk(self.archive_path):
                for file in files:
                    fn = os.path.join(base, file)
                    zip.write(fn, fn[rootlen:])

    @property
    def get_distribution(self):
        return "zip"


class DistTar(Dist):
    def __extract__(self, dest):
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    def __build__(self, bundle_recorder, dest):
        with tarfile.open(bundle_recorder.package_name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))

    @property
    def get_distribution(self):
        return "tar"


class DistRpm(Dist):
    def __extract__(self, dest):
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    @property
    def get_distribution(self):
        return "rpm"

    def __build__(self, bundle_recorder, dest):
        logging.info("build for rpm distribution.")
        manifest_data = bundle_recorder.bundle_manifest.data["build"]
        product_name = product_name_alt = manifest_data["name"].lower()
        if product_name == "opensearch dashboards":
            product_name = "-".join(product_name.split())
            product_name_alt = "_".join(product_name.split())
        root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
        scripts_path = os.path.join(root, "scripts", "pkg")
        architecture_alt = "x86_64" if manifest_data["architecture"] == "x64" else "aarch64"
        real_archive_path = os.path.realpath(self.archive_path)
        data_foler_path = os.path.join(real_archive_path, "data", "")
        systemed_entrypoint_path = os.path.join(real_archive_path, "bin", "systemd-entrypoint")
        os.makedirs(data_foler_path, exist_ok=True)
        shutil.copyfile("scripts/pkg/scripts/systemd-entrypoint", systemed_entrypoint_path)

        subprocess.run(
            [
                "fpm",
                "--force",
                "--verbose",
                "--input-type",
                "dir",
                "--package",
                os.path.join(root, bundle_recorder.package_name),
                "--output-type",
                self.get_distribution,
                "--name",
                product_name,
                "--description",
                " ".join([product_name , self.get_distribution, manifest_data["version"]]),
                "--version",
                manifest_data["version"],
                "--url",
                "https://opensearch.org/",
                "--vendor",
                "OpenSearch",
                "--maintainer",
                "OpenSearch",
                "--license",
                "ASL 2.0",
                "--before-install",
                os.path.join(scripts_path, "scripts", "pre_install.sh"),
                "--before-remove",
                os.path.join(scripts_path, "scripts", "pre_remove.sh"),
                "--after-install",
                os.path.join(scripts_path, "scripts", "post_install.sh"),
                "--after-remove",
                os.path.join(scripts_path, "scripts", "post_remove.sh"),
                "--config-files",
                os.path.join(os.sep, "etc", product_name, product_name_alt + ".yml"),
                "--template-value",
                "product=" + product_name,
                "--template-value",
                "user=" + product_name,
                "--template-value",
                "group=" + product_name,
                "--template-value",
                "homeDir=" + os.path.join(os.sep, "usr", "share", product_name),
                "--template-value",
                "configDir=" + os.path.join(os.sep, "etc", product_name),
                "--template-value",
                "pluginsDir=" + os.path.join(os.sep, "usr", "share", product_name, "plugins"),
                "--template-value",
                "dataDir=" + os.path.join(os.sep, "var", "lib", product_name),
                "--exclude",
                os.path.join("usr", "share", product_name, "data"),
                "--exclude",
                os.path.join("usr", "share", product_name, "config"),
                "--architecture",
                architecture_alt,
                os.path.join(real_archive_path, "") + "=" + os.path.join(os.sep, "usr", "share", product_name, ""),
                os.path.join(real_archive_path, "config", "") + "=" + os.path.join(os.sep, "etc", product_name, ""),
                os.path.join(real_archive_path, "data", "") + "=" + os.path.join(os.sep, "var", "lib", product_name, ""),
                os.path.join(scripts_path, "service_templates", product_name, "systemd", "etc", "") + "=" + os.path.join(os.sep, "etc", ""),
            ]
        )
