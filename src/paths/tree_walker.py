# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import Iterator, Tuple


def walk(root: str) -> Iterator[Tuple[str, str]]:
    logging.info(f"Walking tree from {root}")
    for dir, dirs, files in os.walk(root):
        for file_name in files:
            absolute_path = os.path.join(dir, file_name)
            relative_path = os.path.relpath(absolute_path, root)
            yield os.path.realpath(absolute_path), relative_path
