# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from contextlib import contextmanager
from typing import Generator


@contextmanager
def WorkingDirectory(path: str) -> Generator[None, None, None]:
    try:
        saved_path = os.getcwd()
        os.chdir(path)
        yield
    finally:
        os.chdir(saved_path)
