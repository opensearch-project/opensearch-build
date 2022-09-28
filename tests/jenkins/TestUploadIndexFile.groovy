/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
package jenkins.tests

import org.junit.*

class TestUploadIndexFile extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new UploadIndexFileLibTester('test'))
        this.registerLibTester(new UploadToS3LibTester('index.json', 'ARTIFACT_BUCKET_NAME', 'test/index.json'))

        super.setUp()
    }

    @Test
    void testUploadIndexFile() {
        super.testPipeline('tests/jenkins/jobs/UploadIndexFile_Jenkinsfile')
    }

}
