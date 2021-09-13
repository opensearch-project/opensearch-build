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

    @classmethod
    def compact(cls, d):
        clean = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = cls.compact(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None and v != []:
                clean[k] = v
        return clean

    def __to_dict(self):
        return {}

    def to_dict(self):
        return Manifest.compact(self.__to_dict__())

    def to_file(self, path):
        with open(path, "w") as file:
            yaml.dump(self.to_dict(), file)

    @abstractmethod
    def __init__(self, data):
        self.version = str(data["schema-version"])
        if self.version != "1.0":
            raise ValueError(f"Unsupported schema version: {self.version}")
