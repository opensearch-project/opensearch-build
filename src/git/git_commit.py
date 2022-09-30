# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


class GitCommit:

    def __init__(self, id: str, date: str) -> None:
        self.id = id
        self.date = date
