# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from assemble_workflow.bundle_opensearch import BundleOpenSearch
from assemble_workflow.bundle_opensearch_dashboards import BundleOpenSearchDashboards


class Bundles:
    TYPES = {
        "OpenSearch": BundleOpenSearch,
        "OpenSearch Dashboards": BundleOpenSearchDashboards,
    }

    @classmethod
    def from_name(cls, name):
        klass = cls.TYPES.get(name, None)
        if not klass:
            raise ValueError(f"Unsupported bundle: {name}")
        return klass

    @classmethod
    def create(cls, build_manifest, artifacts_dir, bundle_recorder):
        klass = cls.from_name(build_manifest.build.name)
        return klass(build_manifest, artifacts_dir, bundle_recorder)
