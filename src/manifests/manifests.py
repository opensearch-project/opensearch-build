# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import re
from typing import Any, Generic, List, TypeVar

from sortedcontainers import SortedDict

from manifests.manifest import Manifest

T = TypeVar('T', bound='Manifest')


class Manifests(SortedDict, Generic[T]):
    def __init__(self, klass: Any, files: List[str]) -> None:
        super(Manifests, self).__init__()
        self.klass = klass
        self.__append__(files)

    def __append__(self, files: List[str]) -> None:
        for filename in files:
            basename = os.path.basename(filename)
            match = re.search(r"-([0-9.]*).yml$", basename)
            if not match:
                raise ValueError(f"Invalid file: {basename}")

            version = match.group(1)
            manifest = self.klass.from_path(filename)
            self.__setitem__(version, manifest)

    @property
    def manifests_path(self) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))

    @property
    def versions(self) -> List[T]:
        return list(map(lambda manifest: manifest.build.version, self.values()))  # type: ignore[no-any-return]

    @property
    def latest(self) -> T:
        if len(self) == 0:
            raise RuntimeError("No manifests found")

        return self.values()[-1]  # type: ignore[no-any-return]
