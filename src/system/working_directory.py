# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def WorkingDirectory(path: str) -> Iterator[str]:
    try:
        saved_path = os.getcwd()
        yield os.chdir(path) # type: ignore
    finally:
        os.chdir(saved_path)
