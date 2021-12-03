# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import itertools
import logging
from typing import Any, Callable, Dict, Generic, Iterator, List, Tuple, TypeVar

from manifests.manifest import Manifest

ManifestType = TypeVar('ManifestType', bound='ComponentManifest')
ComponentsType = TypeVar('ComponentsType', bound='Components')
ComponentType = TypeVar('ComponentType', bound='Component')


class ComponentManifest(Manifest[ManifestType], Generic[ManifestType, ComponentsType]):
    components: ComponentsType
    SCHEMA = {
        "schema-version": {
            "required": True, "type": "string", "allowed": ["1.0"]
        },
        "components": {
            "type": "list"
        }
    }

    def __init__(self, data: Any) -> None:
        super().__init__(data)

        self.components = Components(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "schema-version": "1.0",
            "components": self.components.__to_dict__()
        }


class Components(Dict[str, ComponentType], Generic[ComponentType]):
    def __init__(self, data: Dict[Any, Any]) -> None:
        create_component: Callable[[Any], Tuple[str, ComponentType]] = lambda component: (component["name"], self.__create__(component))
        super().__init__(map(create_component, data))

    @classmethod
    def __create__(self, data: Any) -> ComponentType:
        return Component(data)  # type: ignore[return-value]

    def __to_dict__(self) -> List[Dict[Any, Any]]:
        as_dict: Callable[[ComponentType], dict] = lambda component: component.__to_dict__()
        return list(map(as_dict, self.values()))

    def select(self, focus: str = None) -> Iterator[ComponentType]:
        """
        Select components.

        :param str focus: Choose one component.
        :return: Collection of components.
        :raises ValueError: Invalid platform or component name specified.
        """
        is_focused: Callable[[ComponentType], bool] = lambda component: component.__matches__(focus)
        selected, it = itertools.tee(filter(is_focused, self.values()))

        if not any(it):
            raise ValueError(f"No components matched focus={focus}.")

        return selected


class Component:
    platforms: List[str]

    def __init__(self, data: dict) -> None:
        self.name = data["name"]

    def __to_dict__(self) -> dict:
        return {
            "name": self.name
        }

    def __matches__(self, focus: str = None, platform: str = None) -> bool:
        matches = ((not focus) or (self.name == focus)) and ((not platform) or (not self.platforms) or (platform in self.platforms))

        if not matches:
            logging.info(f"Skipping {self.name}")

        return matches
