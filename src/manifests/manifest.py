# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod

import yaml
from cerberus import Validator  # type:ignore


class Manifest(ABC):
    SCHEMA = {"schema-version": {"required": True, "type": "string", "empty": False}}

    @classmethod
    def from_file(cls, file):
        return cls(yaml.safe_load(file))

    @classmethod
    def from_path(cls, path):
        with open(path, "r") as f:
            return cls.from_file(f)

    @classmethod
    def compact(cls, d):
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = cls.compact(v)
                if nested:
                    result[k] = nested
            elif v and v != []:
                result[k] = v
        return result

    def __to_dict(self):
        return {}

    def to_dict(self):
        return Manifest.compact(self.__to_dict__())

    def to_file(self, path):
        with open(path, "w") as file:
            yaml.safe_dump(self.to_dict(), file)

    @abstractmethod
    def __init__(self, data):
        self.validate(data)
        self.version = str(data["schema-version"])

    @property
    def schema(self):
        return self.SCHEMA

    def validate(self, data):
        v = Validator(self.schema)
        if not v.validate(data):
            raise ValueError(f"Invalid manifest schema: {v.errors}")
