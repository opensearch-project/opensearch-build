/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*
import java.util.*
import java.nio.file.*

class TestCopyDockerImage extends BuildPipelineTest {

    static void setUpVariables(binding, helper){
        binding.setVariable('CREDENTIAL_ID', 'dummy_credentials_id')
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')

        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    @Override
    @Before
    void setUp() {
        super.setUp()
        setUpVariables(binding, helper)
    }

    @Test
    public void testForDockerhub() {
        super.testPipeline("tests/jenkins/jobs/CopyDockerImage_docker_Jenkinsfile")
    }

    @Test
    public void testForEcr() {
        super.testPipeline("tests/jenkins/jobs/CopyDockerImage_ecr_Jenkinsfile")
    }
}
