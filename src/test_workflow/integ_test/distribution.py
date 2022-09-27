# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class Distribution(ABC):
    def __enter__(self) -> 'Distribution':
        return self

    def __init__(self, filename: str, version: str, work_dir: str) -> None:
        self.filename = filename
        self.version = version
        self.work_dir = work_dir

    @property
    @abstractmethod
    def install_dir(self) -> str:
        """
        Return the install directory for the distribution
        """
        pass

    @property
    @abstractmethod
    def config_dir(self) -> str:
        """
        Return the config directory for the distribution
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
