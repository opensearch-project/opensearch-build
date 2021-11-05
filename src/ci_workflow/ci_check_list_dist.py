# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.ci_check_list import CiCheckList


class CiCheckListDist(CiCheckList):
    def check(self):
        pass

    def checkout(self, path):
        pass
