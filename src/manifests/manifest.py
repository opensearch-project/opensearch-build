# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import urllib.request
from abc import ABC, abstractmethod
from typing import Dict, Optional

import validators  # type:ignore
import yaml
from cerberus import Validator  # type:ignore


class Manifest(ABC):
    SCHEMA = {
        "schema-version": {
            "required": True, "type": "string", "empty": False
        }
    }

    VERSIONS: Optional[Dict] = None

    @classmethod
    def from_file(cls, file):
        yml = yaml.safe_load(file)
        version = yml["schema-version"]
        loader = cls.from_version(version)
        return loader(yml)

    @classmethod
    def from_url(cls, url):
        logging.info(f"Loading {url}")
        with urllib.request.urlopen(url) as f:
            yml = yaml.safe_load(f.read().decode("utf-8"))
            version = yml["schema-version"]
            loader = cls.from_version(version)
            return loader(yml)

    @classmethod
    def from_version(cls, version):
        if cls.VERSIONS is None:
            return cls

        if version in [None, ""]:
            raise ValueError(f"Missing manifest version, must be one of {', '.join(cls.VERSIONS.keys())}")

        try:
            return cls.VERSIONS[version]
        except KeyError:
            raise ValueError(f"Invalid manifest version: {version}, must be one of {', '.join(cls.VERSIONS.keys())}")

    @classmethod
    def from_path(cls, path):
        logging.info(f"Loading {path}")
        with open(path, "r") as f:
            return cls.from_file(f)

    @classmethod
    def from_urlpath(cls, file_or_url):
        if validators.url(file_or_url):
            return cls.from_url(file_or_url)
        elif os.path.exists(file_or_url):
            return cls.from_path(file_or_url)
        else:
            raise ValueError(f"Invalid manifest: {file_or_url}")

    @classmethod
    def compact(cls, d):
        if isinstance(d, list):
            return list(map(lambda i: cls.compact(i), d))
        elif isinstance(d, dict):
            result = {}
            for k, v in d.items():
                v = cls.compact(v)
                if v:
                    result[k] = v
            return result
        else:
            return d

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
