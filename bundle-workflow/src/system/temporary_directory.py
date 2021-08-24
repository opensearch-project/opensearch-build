# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def TemporaryDirectory(keep=False):
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        if keep:
            print(f"Keeping {name}")
        else:
            shutil.rmtree(name)
