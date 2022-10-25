# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
from typing import Optional

from paths.output_dir import OutputDir


class BuildOutputDir(OutputDir):
    def __init__(self, filename: str, distribution: str, cwd: Optional[str] = None, makedirs: bool = True) -> None:
        super().__init__("builds", filename, distribution, cwd, makedirs)
