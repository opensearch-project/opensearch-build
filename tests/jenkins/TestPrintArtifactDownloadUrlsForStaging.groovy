/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import jenkins.tests.BuildPipelineTest
import org.junit.*

import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.core.IsNull.notNullValue


class TestPrintArtifactDownloadUrlsForStaging extends BuildPipelineTest implements LibFunctionTester {

    private List artifactFileNames
    private String uploadPath


    @Before
    void setUp() {

        this.artifactFileNames = ['dummy_file.tar.gz', 'dummy_file.tar.gz.sig', 'a_dummy_file.tar.gz']
        this.uploadPath = 'dummy/upload/path'

        this.registerLibTester(new TestPrintArtifactDownloadUrlsForStaging(
                artifactFileNames: artifactFileNames,
                uploadPath: uploadPath
        ))

        super.setUp()
    }

    @Test
    void testPrintArtifactDownloadUrlsForStaging() {

        binding.setVariable('filenamesForUrls', artifactFileNames)
        binding.setVariable('UPLOAD_PATH', uploadPath)

        super.testPipeline("tests/jenkins/jobs/PrintArtifactDownloadUrlsForStaging_Jenkinsfile")

    }

    void configure(helper, bindings){
    }

    void verifyParams(helper) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'printArtifactDownloadUrlsForStaging'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'printArtifactDownloadUrlsForStaging'
        }.each { call ->
            assertThat(call.args.artifactFileNames.first(), notNullValue())
            assertThat(call.args.uploadPath.first(), notNullValue())
            assert call.args.artifactFileNames.size() > 0
        }

        def callFound = false

        def callList = helper.callStack.findAll { call ->
            call.methodName == 'printArtifactDownloadUrlsForStaging'
        }

        for(call in callList){
            if( call.args.uploadPath.first() == this.uploadPath
                    && call.args.artifactFileNames.first().sort() == this.artifactFileNames.sort() ){
                callFound = true
            }
        }

        assert callFound
    }

}
