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

class TestWhileSourceScan extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        super.setUp()

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('latest')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )
    }

    @Test
    public void testWhileSourceScan() {
        super.testPipeline("jenkins/vulnerability-scan/whitesource-scan.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/vulnerability-scan/whitesource-scan.jenkinsfile")
    }
}