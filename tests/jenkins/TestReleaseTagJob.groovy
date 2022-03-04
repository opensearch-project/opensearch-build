/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestReleaseTagJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def buildManifest = 'tests/data/opensearch-build-1.1.0.yml'

        def destPath = "${this.workspace}/${buildManifest}"

        def artifactsPath = 'distribution-build-opensearch/1.1.0/123/linux/x64/builds/opensearch/manifest.yml'

        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new DownloadFromS3LibTester(destPath, bucketName, artifactsPath, true))

        this.registerLibTester(new CreateReleaseTagLibTester(buildManifest, '1.1.0'))

        super.setUp()

        // Variables for Release Tag Job
        binding.setVariable('VERSION', '1.1.0')
        binding.setVariable('BUILD_ID', '123')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('BUILD_MANIFEST', buildManifest)

        helper.registerAllowedMethod("checkout", [Map], {})
        helper.registerAllowedMethod("dir", [Map], {})
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/OpenSearch.git 1.1.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/common-utils.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/job-scheduler.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "4504dabfc67dd5628c1451e91e9a1c3c4ca71525", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/sql.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/alerting.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/notifications.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/security.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/performance-analyzer-rca.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "345a10fd4f4e94d6392c925ad95503ba8addd152", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/performance-analyzer.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/index-management.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/k-NN.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/anomaly-detection.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/asynchronous-search.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/dashboards-reports.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/dashboards-notebooks.git 1.1.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: "", exitValue: 0]
        }

    }

    @Test
    void ReleaseTag_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag.jenkinsfile')
    }
}
