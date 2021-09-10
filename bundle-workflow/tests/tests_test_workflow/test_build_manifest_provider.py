import unittest

from test_workflow.utils.build_manifest_provider import BuildManifestProvider


class TestBuildManifestProvider(unittest.TestCase):
    def test_get_manifest_relative_location(self):
        actual = BuildManifestProvider.get_build_manifest_relative_location(
            '25', '1.1.0', 'x64'
        )
        expected = 'builds/1.1.0/25/x64/manifest.yml'
        self.assertEqual(actual, expected, "the manifest relative location is not as expected")
