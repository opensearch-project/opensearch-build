# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod

import yaml


class Manifest(ABC):
    @classmethod
    def from_file(cls, file):
        return cls(yaml.safe_load(file))

    @classmethod
    def from_path(cls, path):
        with open(path, "r") as f:
            return cls.from_file(f)

    @abstractmethod
    def __init__(self, data):
        self.version = str(data["schema-version"])
        if self.version != "1.0":
            raise ValueError(f"Unsupported schema version: {self.version}")
