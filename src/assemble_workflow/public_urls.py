# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from urllib.parse import urljoin

class PublicURLpath:
    def __init__(self, build): 
        self.public_url = os.getenv("PUBLIC_ARTIFACT_URL", None)
        self.urls_path = {
            "bundles": self.get_url(build, self.public_url, "bundles"), 
            "builds": self.get_url(build, self.public_url, "builds")
            }

    def get_url (self, build, public_url, folder):
        if public_url:
            return "/".join((public_url, build.name.replace(' ', '-').lower(), folder, build.version, build.id, build.architecture))
        return public_url
            