# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class Distribution(ABC):
    def __enter__(self) -> 'Distribution':
        return self

    def __init__(self, filename: str, distribution: str, version: str, work_dir: str) -> None:
        self.filename = filename
        self.distribution = distribution
        self.version = version
        self.work_dir = work_dir

    @property
    @abstractmethod
    def get_install_dir(self) -> str:
        """
        Return the install directory for the distribution
        """
        pass

    @property
    @abstractmethod
    def get_config_dir(self, bundle_name: str) -> str:
        """
        Return the config directory for the distribution
        """
        pass

    @abstractmethod
    def install_distribution(self) -> None:
        """
        The detailed method to install the distribution before start the service
        """
        pass

    @property
    @abstractmethod
    def get_start_cmd(self) -> str:
        """
        Return the start command for the distribution
        """
        pass

    def cleanup(self) -> None:
        """
        Allow distribution that is not 'tar' to do proper cleanup
        """
        pass
