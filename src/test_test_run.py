from manifests.test_run_manifest import TestRunManifest

data = {
    "schema-version": "1.0",
    "name": "OpenSearch",
    "test-run": {
        "Command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
        "TestType": "integ-test",
        "TestManifest": "manifests/2.7.0/opensearch-2.7.0-test.yml",
        "DistributionManifest": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar/dist/opensearch/manifest.yml",
        "TestID": "2345"
    },
    "components": [{
        "name": "sql",
        "command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --component sql --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
        "configs": [            # configs is a list of dict
            {
                "name": "with-security",
                "status": "pass",
                "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/with-security/sql.yml"
            },
            {
                "name": "without-security",
                "status": "fail",
                "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/without-security/sql.yml"
            }
        ]
    },
        {
            "name": "anomaly-detection",
            "command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --component anomaly-detection --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
            "configs": [            # configs is a list of dict
                {
                    "name": "with-security",
                    "status": "pass",
                    "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/anomaly-detection/with-security/anomaly-detection.yml"
                },
                {
                    "name": "without-security",
                    "status": "fail",
                    "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/anomaly-detection/without-security/anomaly-detection.yml"
                }
            ]
        }
    ]
}

test_run_manifest = TestRunManifest(data)
output_dir = "/Users/zelinhao/workplace/reporting_system/reporting_workflow/opensearch-build/test-run.yml"
test_run_manifest.to_file(output_dir)
# test_run_manifest1 = TestRunManifest.from_path(output_dir)
# print(test_run_manifest1.components.name)
