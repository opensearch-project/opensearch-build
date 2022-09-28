# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from paths.output_dir import OutputDir


class AssembleOutputDir(OutputDir):
    def __init__(cls, filename: str, distribution: str, cwd: str = None, makedirs: bool = True) -> None:
        super().__init__("dist", filename, distribution, cwd, makedirs)
