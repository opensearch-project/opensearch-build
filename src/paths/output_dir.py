# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from abc import ABC
from typing import Optional


class OutputDir(ABC):
    def __init__(cls, parent_dir: str, filename: str, distribution: str, cwd: Optional[str] = None, makedirs: bool = True) -> None:
        cls.dir = os.path.join(
            cwd or os.getcwd(),
            distribution,
            parent_dir,
            filename
        )

        if makedirs:
            os.makedirs(cls.dir, exist_ok=True)
