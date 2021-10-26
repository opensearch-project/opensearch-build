# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import errno
import logging
import os
import shutil
import stat
import tempfile


def g__handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


class TemporaryDirectory:
    def __init__(self, keep=False, chdir=False):
        self.keep = keep
        self.name = tempfile.mkdtemp()
        if chdir:
            self.curdir = os.getcwd()
            os.chdir(self.name)
        else:
            self.curdir = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.curdir:
            os.chdir(self.curdir)

        if self.keep:
            logging.info(f"Keeping {self.name}")
        else:
            logging.debug(f"Removing {self.name}")
            shutil.rmtree(self.name, ignore_errors=False, onerror=g__handleRemoveReadonly)
