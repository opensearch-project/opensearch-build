# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""
This class is responsible for sanity checking the OpenSearch bundle.
"""


class Ci:
    def __init__(self, component_name, git_repo):
        """
        Construct a new instance of Ci.
        :param component_name: The name of the component to sanity-check.
        :param git_repo: A GitRepository instance containing the checked-out code.
        """

        self.component_name = component_name
        self.git_repo = git_repo

    def check(self, version, arch, snapshot):
        pass
