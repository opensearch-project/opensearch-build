# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import urllib.request
from abc import ABC, abstractmethod
from typing import IO, Any, Dict, Generic, Optional, Type, TypeVar

import validators
import yaml
import yamlfix
from cerberus import Validator

T = TypeVar('T', bound='Manifest')


class Manifest(ABC, Generic[T]):
    SCHEMA = {
        "schema-version": {
            "required": True, "type": "string", "empty": False
        }
    }

    VERSIONS: Optional[Dict[str, object]] = None

    @classmethod
    def from_file(cls, file: IO[Any]) -> T:
        yml = yaml.safe_load(file)
        version = yml["schema-version"]
        loader = cls.from_version(version)
        return loader(yml)

    @classmethod
    def from_url(cls, url: str) -> T:
        logging.info(f"Loading {url}")
        with urllib.request.urlopen(url) as f:
            yml = yaml.safe_load(f.read().decode("utf-8"))
            version = yml["schema-version"]
            loader = cls.from_version(version)
            return loader(yml)

    @classmethod
    def from_version(cls, version: str) -> Type[T]:
        if cls.VERSIONS is None:
            return cls  # type: ignore[return-value]
        if version in [None, ""]:
            raise ValueError(f"Missing manifest version, must be one of {', '.join(cls.VERSIONS.keys())}")

        try:
            return cls.VERSIONS[version]  # type: ignore[return-value]
        except KeyError:
            raise ValueError(f"Invalid manifest version: {version}, must be one of {', '.join(cls.VERSIONS.keys())}")

    @classmethod
    def from_path(cls, path: str) -> T:
        logging.info(f"Loading {path}")
        with open(path, "r") as f:
            return cls.from_file(f)

    @classmethod
    def from_urlpath(cls, file_or_url: str) -> T:
        if validators.url(file_or_url):
            return cls.from_url(file_or_url)
        elif os.path.exists(file_or_url):
            return cls.from_path(file_or_url)
        else:
            raise ValueError(f"Invalid manifest: {file_or_url}")

    @classmethod
    def compact(cls, d: Any) -> Any:
        if isinstance(d, list):
            return list(map(lambda i: cls.compact(i), d))  # type: ignore[return-value, no-any-return]
        elif isinstance(d, dict):
            result = {}
            for k, v in d.items():
                v = cls.compact(v)
                if v or isinstance(v, bool):
                    result[k] = v
            return result
        else:
            return d

    def __to_dict(self) -> dict:
        return {}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.to_dict() == other.to_dict()  # type: ignore[no-any-return]
        return False

    def to_dict(self) -> Any:
        return Manifest.compact(self.__to_dict__())  # type: ignore[attr-defined]

    def to_file(self, path: str) -> None:
        with open(path, "w") as file:
            file.write(
                yamlfix.fix_code(
                    yaml.safe_dump(
                        self.to_dict(),
                        sort_keys=False
                    )
                )
            )

    @abstractmethod
    def __init__(self, data: Any) -> None:
        self.validate(data)
        self.version = str(data["schema-version"])

    @property
    def schema(self) -> Any:
        return self.SCHEMA

    def validate(self, data: Any) -> None:
        v = Validator(self.schema)
        if not v.validate(data):
            raise ValueError(f"Invalid manifest schema: {v.errors}")
