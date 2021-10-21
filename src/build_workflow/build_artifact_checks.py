# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from build_workflow.opensearch.build_artifact_check_maven import BuildArtifactOpenSearchCheckMaven
from build_workflow.opensearch.build_artifact_check_plugin import BuildArtifactOpenSearchCheckPlugin
from build_workflow.opensearch_dashboards.build_artifact_check_plugin import BuildArtifactOpenSearchDashboardsCheckPlugin


class BuildArtifactChecks:
    TYPES = {
        "OpenSearch": {
            "plugins": BuildArtifactOpenSearchCheckPlugin,
            "maven": BuildArtifactOpenSearchCheckMaven,
        },
        "OpenSearch Dashboards": {"plugins": BuildArtifactOpenSearchDashboardsCheckPlugin},
    }

    @classmethod
    def from_name_and_type(cls, name, type):
        checks = cls.TYPES.get(name, None)
        if not checks:
            raise ValueError(f"Unsupported bundle: {name}")
        return checks.get(type, None)

    @classmethod
    def create(cls, target, artifact_type):
        klass = cls.from_name_and_type(target.name, artifact_type)
        if not klass:
            return None
        return klass(target)

    @classmethod
    def check(cls, target, artifact_type, path):
        instance = cls.create(target, artifact_type)
        if instance:
            instance.check(path)
