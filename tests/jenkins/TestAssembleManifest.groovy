/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
package jenkins.tests

import org.junit.*

class TestAssembleManifest extends BuildPipelineTest {

    @Test
    void testAssembleManifest_rpm() {
        this.registerLibTester(new AssembleManifestLibTester('tests/data/opensearch-build-1.3.0-rpm.yml'))

        this.registerLibTester(new SignArtifactsLibTester('.rpm', 'linux', "rpm/dist/opensearch", null, null))

        this.registerLibTester(new BuildYumRepoTester(
            'tests/data/opensearch-build-1.3.0-rpm.yml',
            'https://ci.opensearch.org/dbc/vars-build/1.3.0/123/linux/x64'
        ))

        super.setUp()

        super.testPipeline('tests/jenkins/jobs/AssembleManifest_rpm_Jenkinsfile')
    }

    @Test
    void testAssembleManifest_tar() {
        this.registerLibTester(new AssembleManifestLibTester('tests/data/opensearch-build-1.3.0.yml'))
        super.setUp()

        super.testPipeline('tests/jenkins/jobs/AssembleManifest_tar_Jenkinsfile')
    }
}
