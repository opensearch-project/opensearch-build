# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging
import shutil
from abc import ABC, abstractmethod
from typing import Any

from system.execute import execute
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation_args import ValidationArgs


class Validation(ABC):
    """
        Abstract class for all types of artifact validation
    """

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__()
        self.args = args

    def check_url(self, url: str) -> bool:
        if DownloadUtils().download(url, self.tmp_dir) and DownloadUtils().is_url_valid(url):  # type: ignore
            logging.info(f"Valid URL - {url} and Download Successful !")
            return True
        else:
            raise Exception(f"Invalid url - {url}")

    def copy_artifact(self, filepath: str, tempdir_path: str) -> bool:
        if filepath:
            shutil.copy2(filepath, tempdir_path)
            return True
        else:
            raise Exception("Provided path for local artifacts does not exist")

    def test_security_plugin(self, work_dir: str) -> bool:
        (_, stdout_1, _) = execute(f'find {work_dir} -type f -iname \'opensearch-plugin\'', ".", True, False)
        if (stdout_1):
            (_, stdout_2, _) = execute("./opensearch-plugin list", stdout_1.replace("opensearch-plugin", "").rstrip("\n"), True, False)
            return "opensearch-security" in stdout_2
        else:
            raise Exception("Couldn't fetch the path to plugin folder")

    def run(self) -> Any:
        try:
            return self.download_artifacts() and self.installation() and self.start_cluster() and self.validation() and self.cleanup()
        except Exception as e:
            raise Exception(f'An error occurred while running the validation tests: {str(e)}')

    @abstractmethod
    def download_artifacts(self) -> bool:
        pass

    @abstractmethod
    def installation(self) -> bool:
        pass

    @abstractmethod
    def start_cluster(self) -> bool:
        pass

    @abstractmethod
    def validation(self) -> bool:
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        pass
