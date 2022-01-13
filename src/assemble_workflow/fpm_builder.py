# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import logging
import shutil
import subprocess
from assemble_workflow.bundle_recorder import BundleRecorder


class FpmBuilder:

    ARCHITECTURE_ALT = {
        "rpm_x64": "x86_64",
        "rpm_arm64": "aarch64"
    }

    def build(self, bundle_recorder: BundleRecorder, archive_path: str, distribution: str) -> None:
        manifest = bundle_recorder.get_manifest()

        product_name = manifest.build.filename
        # OpenSearch Dashboards has its config file name hardcoded to opensearch_dashboards.yml
        product_name_alt = "_".join(product_name.split("-"))
        version = manifest.build.version
        logging.info(f"Product: {product_name}, Config: {product_name_alt}.yml, Version: {version}")

        architecture = manifest.build.architecture
        architecture_alt = self.ARCHITECTURE_ALT['_'.join([distribution, architecture])]
        logging.info(f"Distribution: {distribution}, Architecture: {architecture}({architecture_alt})")

        package_name = bundle_recorder.package_name
        logging.info(f"Creating package: {package_name}")

        root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
        scripts_path = os.path.join(root_path, "scripts", "pkg")
        real_archive_path = os.path.realpath(archive_path)
        data_dir_path = os.path.join(real_archive_path, "data", "")
        log_dir_path = os.path.join(real_archive_path, "logs", "")
        systemed_entrypoint_path = os.path.join(real_archive_path, "bin", "systemd-entrypoint")

        os.makedirs(data_dir_path, exist_ok=True)
        os.makedirs(log_dir_path, exist_ok=True)
        shutil.copyfile("scripts/pkg/scripts/systemd-entrypoint", systemed_entrypoint_path)
        os.chmod(systemed_entrypoint_path, 0o755)
        subprocess.check_call(
            [
                "fpm",
                "--force",
                "--verbose",
                "--input-type",
                "dir",
                "--package",
                os.path.join(root_path, package_name),
                "--output-type",
                distribution,
                "--name",
                product_name,
                "--description",
                " ".join([product_name, distribution, version]),
                "--version",
                version,
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
                "--template-value",
                "logDir=" + os.path.join(os.sep, "var", "log", product_name),               
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
                os.path.join(real_archive_path, "logs", "") + "=" + os.path.join(os.sep, "var", "log", product_name, "")
            ]
        )
