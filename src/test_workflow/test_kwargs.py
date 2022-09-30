# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import argparse
from typing import Any, Sequence, Union

from test_workflow.test_args_path_validator import TestArgsPathValidator


class TestKwargs(argparse.Action):
    def __call__(self, parser: Any, namespace: argparse.Namespace, values: Union[str, Sequence[Any], None], option_string: str = None) -> None:
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = TestArgsPathValidator.validate(value)


TestKwargs.__test__ = False  # type:ignore
