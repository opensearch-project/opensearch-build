# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from unittest.mock import patch

from checkout_workflow.checkout_args import CheckoutArgs


class TestCheckoutArgs(unittest.TestCase):

    CHECKOUT_PY = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "run_checkout.py"))

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "1.1.0",
            "opensearch-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", [CHECKOUT_PY, OPENSEARCH_MANIFEST])
    def test_manifest(self) -> None:
        self.assertEqual(CheckoutArgs().manifest.name, TestCheckoutArgs.OPENSEARCH_MANIFEST)

    @patch("argparse._sys.argv", [CHECKOUT_PY, OPENSEARCH_MANIFEST, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(CheckoutArgs().logging_level, logging.DEBUG)
