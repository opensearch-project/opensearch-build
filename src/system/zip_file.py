# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries

import os
import zipfile


class ZipFile(zipfile.ZipFile):
    def _extract_member(self, member: zipfile.ZipInfo, targetpath: str, pwd: str) -> str:
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)  # type: ignore[misc]

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)

        return targetpath
