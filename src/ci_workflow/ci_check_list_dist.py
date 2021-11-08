# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.ci_check_list import CiCheckList
from ci_workflow.ci_check_manifest_component import CiCheckManifestComponent


class CiCheckListDist(CiCheckList):
    def checkout(self, work_dir):
        pass

    CHECKS = {"manifest:component": CiCheckManifestComponent}

    class InvalidCheckError(Exception):
        def __init__(self, check):
            self.check = check
            super().__init__(f"Invalid check: {check.name}, must be one of {CiCheckListDist.CHECKS.keys()}.")

    def check(self):
        for check in self.component.checks:
            klass = CiCheckListDist.CHECKS.get(check.name, None)
            if klass is None:
                raise CiCheckListDist.InvalidCheckError(check)
            instance = klass(self.component, self.target, check.args)
            instance.check()
