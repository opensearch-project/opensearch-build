# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any, Dict

from build_workflow.build_target import BuildTarget
from build_workflow.opensearch.build_artifact_check_maven import BuildArtifactOpenSearchCheckMaven
from build_workflow.opensearch.build_artifact_check_plugin import BuildArtifactOpenSearchCheckPlugin
from build_workflow.opensearch_dashboards.build_artifact_check_plugin import BuildArtifactOpenSearchDashboardsCheckPlugin


class BuildArtifactChecks:
    TYPES: Dict[str, Dict[str, Any]] = {
        "OpenSearch": {
            "plugins": BuildArtifactOpenSearchCheckPlugin,
            "maven": BuildArtifactOpenSearchCheckMaven,
        },
        "OpenSearch Dashboards": {"plugins": BuildArtifactOpenSearchDashboardsCheckPlugin},
    }

    @classmethod
    def from_name_and_type(cls, name: str, type: str) -> Any:
        checks = cls.TYPES.get(name, None)
        if not checks:
            raise ValueError(f"Unsupported bundle: {name}")
        return checks.get(type, None)

    @classmethod
    def create(cls, target: BuildTarget, artifact_type: str) -> Any:
        klass = cls.from_name_and_type(target.name, artifact_type)
        if not klass:
            return None
        return klass(target)

    @classmethod
    def check(cls, target: BuildTarget, artifact_type: str, path: str) -> None:
        instance = cls.create(target, artifact_type)
        if instance:
            instance.check(path)
