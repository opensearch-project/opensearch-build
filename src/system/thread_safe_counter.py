# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import threading
from typing import Any


class ThreadSafeCounter:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.__call_count__ = 0

    def thread_safe_count(self, *args: Any, **kwargs: Any) -> None:
        with self.lock:
            self.__call_count__ += 1

    @property
    def call_count(self) -> int:
        return self.__call_count__
