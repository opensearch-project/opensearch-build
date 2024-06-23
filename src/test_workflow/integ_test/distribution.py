# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import logging
import os.path
from abc import ABC, abstractmethod


class Distribution(ABC):
    def __enter__(self) -> 'Distribution':
        return self

    def __init__(self, filename: str, version: str, work_dir: str) -> None:
        self.filename = filename
        self.version = version
        self.work_dir = work_dir
        self.require_sudo = False

    @property
    @abstractmethod
    def install_dir(self) -> str:
        """
        Return the install directory for the distribution
        """
        pass

    @property
    def config_filename(self) -> str:
        """
        Return the config filename for the distribution
        """
        return f"{self.filename.replace('-', '_')}.yml"

    @property
    @abstractmethod
    def config_path(self) -> str:
        """
        Return the config path for the distribution
        """
        pass

    @property
    @abstractmethod
    def data_dir(self) -> str:
        """
        Return the data directory for the distribution
        """
        pass

    @property
    @abstractmethod
    def log_dir(self) -> str:
        """
        Return the log directory for the distribution
        """
        pass

    @abstractmethod
    def install(self, bundle_name: str) -> None:
        """
        The detailed method to install the distribution before start the service
        """
        pass

    @property
    @abstractmethod
    def start_cmd(self) -> str:
        """
        Return the start command for the distribution
        """
        pass

    @abstractmethod
    def uninstall(self) -> None:
        """
        Allow distribution to do proper cleanup
        """
        pass

    def configure_jvm_options(self, options: list) -> None:
        jvm_config_path = os.path.join(os.path.dirname(self.config_path), 'jvm.options')
        try:
            with open(jvm_config_path, 'r') as file:
                file_content = file.read()

            modified_content = file_content

            for jvm_old, jvm_new in options:
                modified_content = modified_content.replace(jvm_old, jvm_new)

            with open(jvm_config_path, 'w') as file:
                file.write(modified_content)
            logging.info("Configured JVM options")
        except FileNotFoundError:
            logging.error("File not found.")
        except Exception as e:
            logging.error(f"An error occurred:{e}")
