# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import threading


class ThreadSafeCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.__call_count__ = 0

    def thread_safe_count(self, *args, **kwargs):
        with self.lock:
            self.__call_count__ += 1

    @property
    def call_count(self):
        return self.__call_count__
