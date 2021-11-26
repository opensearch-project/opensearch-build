# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import itertools
import logging

from manifests.manifest import Manifest


class ComponentManifest(Manifest):
    SCHEMA = {
        "schema-version": {
            "required": True, "type": "string", "allowed": ["1.0"]
        },
        "components": {
            "type": "list"
        }
    }

    def __init__(self, data):
        super().__init__(data)

        self.components = self.Components(data.get("components", []))

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "components": self.components.__to_dict__()
        }

    class Components(dict):
        def __init__(self, data):
            super().__init__(map(lambda component: (component["name"], self.__create__(component)), data))

        @classmethod
        def __create__(data):
            ComponentManifest.Component(data)

        def __to_dict__(self):
            return list(map(lambda component: component.__to_dict__(), self.values()))

        def select(self, focus=None):
            """
            Select components.

            :param str focus: Choose one component.
            :return: Collection of components.
            :raises ValueError: Invalid platform or component name specified.
            """
            selected, it = itertools.tee(filter(lambda component: component.__matches__(focus), self.values()))

            if not any(it):
                raise ValueError(f"No components matched focus={focus}.")

            return selected

    class Component:
        def __init__(self, data):
            self.name = data["name"]

        def __to_dict__(self):
            return {
                "name": self.name
            }

        def __matches__(self, focus=None, platform=None):
            matches = ((not focus) or (self.name == focus)) and ((not platform) or (not self.platforms) or (platform in self.platforms))

            if not matches:
                logging.info(f"Skipping {self.name}")

            return matches
