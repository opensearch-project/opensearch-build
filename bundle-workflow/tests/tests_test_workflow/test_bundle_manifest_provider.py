import unittest

from test_workflow.utils.bundle_manifest_provider import BundleManifestProvider


class TestBundleManifestProvider(unittest.TestCase):
    def test_get_manifest_relative_location(self):
        actual = BundleManifestProvider.get_bundle_manifest_relative_location(
            '25', '1.1.0', 'x64'
        )
        expected = 'bundles/1.1.0/25/x64/manifest.yml'
        self.assertEqual(actual, expected, "the manifest relative location is not as expected")

    def test_get_tarball_relative_location(self):
        actual = BundleManifestProvider.get_tarball_relative_location('25', '1.1.0', 'x64')
        expected = 'bundles/1.1.0/25/x64/opensearch-1.1.0-linux-x64.tar.gz'
        self.assertEqual(actual, expected, "the tarball relative location is not as expected")

    def test_get_tarball_name(self):
        actual = BundleManifestProvider.get_tarball_name('1.1.0', 'x64')
        expected = f"opensearch-1.1.0-linux-x64.tar.gz"
        self.assertEqual(actual, expected, "the tarball name is not as expected")