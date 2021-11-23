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
    def __init__(self, name, path, distribution):
        self.name = name
        self.path = path
        self.distribution = distribution

    @abstractmethod
    def __extract__(self, dest):
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
        if distribution == "rpm":
            return DistRpm(name, path, distribution)
        elif distribution == "tar":
            return DistTar(name, path, distribution)
        elif distribution == "zip":
            return DistZip(name, path, distribution)
        else:
            raise ValueError("Distribution not specified or invalid distribution")


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


class DistTar(Dist):
    def __extract__(self, dest):
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    def __build__(self, bundle_recorder, dest):
        with tarfile.open(bundle_recorder.package_name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))


class DistRpm(Dist):
    def __extract__(self, dest):
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    def __build__(self, bundle_recorder, dest):
        logging.info("build for rpm distribution.")
        manifest_data = bundle_recorder.bundle_manifest.data["build"]
        product_name = manifest_data["name"].lower()
        if product_name == "opensearch dashboards":
            product_name = "-".join(product_name.split())
            product_name_alt = "_".join(product_name.split())
        output_dir = os.getcwd()
        output_package_name = output_dir + "/" + bundle_recorder.package_name
        description = " ".join([product_name , self.distribution, manifest_data["version"]])
        scripts_path = output_dir + "/scripts/pkg"
        pre_install_path = scripts_path + "/scripts/pre_install.sh"
        pre_remove_path = scripts_path + "/scripts/pre_remove.sh"
        post_install_path = scripts_path + "/scripts/post_install.sh"
        post_remove_path = scripts_path + "/scripts/post_remove.sh"
        config_file_path = "/etc/" + product_name + "/" + product_name + ".yml"
        architecture_alt = "x86_64" if manifest_data["architecture"] == "x64" else "aarch64"
        real_archive_path = os.path.realpath(self.archive_path)
        data_foler_path = real_archive_path + '/data/'
        systemed_entrypoint_path = real_archive_path + '/bin/systemd-entrypoint'
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
                output_package_name,
                "--output-type",
                self.distribution,
                "--name",
                product_name,
                "--description",
                description,
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
                pre_install_path,
                "--before-remove",
                pre_remove_path,
                "--after-instal",
                post_install_path,
                "--after-remove",
                post_remove_path,
                "--config-file",
                config_file_path,
                "--template-value",
                "product=" + product_name,
                "--template-value",
                "user=" + product_name,
                "--template-value",
                "group=" + product_name,
                "--template-value",
                "homeDir=/usr/share/" + product_name,
                "--template-value",
                "configDir=/etc" + product_name,
                "--template-value",
                "pluginsDir=/usr/share" + product_name + "/plugins",
                "--template-value",
                "dataDir=/var/lib/" + product_name,
                "--exclude",
                "usr/share/" + product_name + "/data",
                "--exclude",
                "usr/share/" + product_name + "/config",
                "--architecture",
                architecture_alt,
                real_archive_path + "/=/usr/share/" + product_name + "/",
                real_archive_path + "/config/=/etc/" + product_name + "/",
                real_archive_path + "/data/=/var/lib" + product_name + "/",
                scripts_path + "service_templates/" + product_name + "/systemd/etc/=/etc",
            ]
        )
