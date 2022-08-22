# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import stat
import tempfile
from pathlib import Path
from types import FunctionType
from typing import Any


def g__handleRemoveReadonly(func: FunctionType, path: str, exc: Any) -> Any:
    excvalue = exc[1]
    logging.debug(f"excvalue {excvalue}")
    logging.debug(f"func {func.__name__}")
    if func in (os.rmdir, os.remove, os.unlink):
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO | stat.S_IWRITE | stat.S_IREAD)  # 0777 nix* / +wr windows
        retry_total = 3
        for retry_count in range(retry_total):  # Re-run func to force deletion especially on windows
            try:
                logging.debug(f'Try count: {retry_count + 1}/{retry_total}')
                func_result = func(path)
                if func_result is None:
                    break
            except Exception as ex:
                logging.warn(func_result)
                logging.warn(ex)
    else:
        raise


class TemporaryDirectory:
    def __init__(self, keep: bool = False, chdir: bool = False) -> None:
        self.keep = keep
        self.name = tempfile.mkdtemp()
        if chdir:
            self.curdir = os.getcwd()
            os.chdir(self.name)
        else:
            self.curdir = None

    @property
    def path(self) -> Path:
        return Path(self.name)

    def __enter__(self) -> 'TemporaryDirectory':
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        if self.curdir:
            os.chdir(self.curdir)

        if self.keep:
            logging.info(f"Keeping {self.name}")
        else:
            logging.debug(f"Removing {self.name}")
            shutil.rmtree(self.name, ignore_errors=False, onerror=g__handleRemoveReadonly)
