/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import org.junit.*
import jenkins.tests.BuildPipelineTest
import java.util.*
import java.nio.file.*

class TestCreateReleaseTag extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new CreateReleaseTagLibTester('tests/data/opensearch-build-1.1.0.yml', '1.1.0'))
        super.setUp()

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
    void testCreateReleaseTag() {
        super.testPipeline("tests/jenkins/jobs/CreateReleaseTag_Jenkinsfile")
    }
}
