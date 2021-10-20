# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import shutil
import tempfile


class TemporaryDirectory:
    def __init__(self, keep=False):
        self.keep = keep
        self.name = tempfile.mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.keep:
            logging.info(f"Keeping {self.name}")
        else:
            logging.debug(f"Removing {self.name}")
            shutil.rmtree(self.name)

    @classmethod
    def mkdtemp(cls, keep=False):
        return cls(keep)
