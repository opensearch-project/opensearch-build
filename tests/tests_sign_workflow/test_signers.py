# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from sign_workflow.signer_pgp import SignerPGP
from sign_workflow.signer_windows import SignerWindows
from sign_workflow.signers import Signers


class TestSigners(unittest.TestCase):

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_PGP(self, mock_repo: Mock) -> None:
        signer = Signers.create("linux")
        self.assertIs(type(signer), SignerPGP)

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_windows(self, mock_repo: Mock) -> None:
        signer = Signers.create("windows")
        self.assertIs(type(signer), SignerWindows)

    def test_signer_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Signers.create("mac")
        self.assertEqual(str(ctx.exception), "Unsupported type of platform for signing: mac")
