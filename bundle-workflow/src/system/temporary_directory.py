# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

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
