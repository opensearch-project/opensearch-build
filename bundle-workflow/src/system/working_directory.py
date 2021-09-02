# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from contextlib import contextmanager

saved_path = os.getcwd()


@contextmanager
def WorkingDirectory(path):
    try:
        yield os.chdir(path)
    finally:
        os.chdir(saved_path)
