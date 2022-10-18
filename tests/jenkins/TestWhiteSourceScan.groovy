/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.assertj.core.api.Assertions.assertThat

class TestWhileSourceScan extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        super.setUp()
    }

    @Test
    public void testWhileSourceScanRegression() {
        super.testPipeline("jenkins/vulnerability-scan/whitesource-scan.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/vulnerability-scan/whitesource-scan.jenkinsfile")
    }

    @Test
    public void whitesourceScanExecuteWithoutErrors() {
        runScript("jenkins/vulnerability-scan/whitesource-scan.jenkinsfile")

        assertJobStatusSuccess()

        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('wss-scan.sh')
        }).isTrue()
    }
}
