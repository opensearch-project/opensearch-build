/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*
import java.nio.file.*

class TestArchiveAssembleUpload extends BuildPipelineTest {
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('JOB_NAME', 'vars-build')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'artifact-bucket')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')
        binding.setVariable('STAGE_NAME', 'stage')
        binding.setVariable('BUILD_URL', 'http://jenkins.us-east-1.elb.amazonaws.com/job/vars/42')
        binding.setVariable('BUILD_NUMBER', '33')

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("git", [Map])

        Path source = Path.of("tests/data/opensearch-build-1.1.0.yml");
        Path target = Path.of("builds/opensearch/manifest.yml");
        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);    
    }

    @Test
    public void testSHAExists() {
        binding.env."BUILD_SHA_linux_x64_SHA" = 'sha1'
        binding.env."BUILD_SHA_linux_x64_LOCK" = 'tests/jenkins/data/opensearch-1.3.0.yml.lock'
        binding.env."BUILD_SHA_linux_x64_PATH" = 'assemble-upload-build/1.1.0/shas/linux/x64/sha1.yml'

        super.testPipeline(
            "tests/jenkins/jobs/ArchiveAssembleUpload_Jenkinsfile",
            "tests/jenkins/jobs/ArchiveAssembleUpload_Jenkinsfile_sha"
        )
    }

    @Test
    public void testSHADoesNotExist() {
        super.testPipeline(
            "tests/jenkins/jobs/ArchiveAssembleUpload_Jenkinsfile",
            "tests/jenkins/jobs/ArchiveAssembleUpload_Jenkinsfile_no_sha"
        )
    }
}
