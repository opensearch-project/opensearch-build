/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*

import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestCopyDockerImage extends BuildPipelineTest {

    static void setUpVariables(binding, helper){
        binding.setVariable('CREDENTIAL_ID', 'dummy_credentials_id')
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')

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

    def sourceImagePath = 'opensearchstaging/ci-runner:latest'
    def destinationImagePath = 'opensearchproject/ci-runner:latest'

    @Test
    public void testForDockerhub() {
        def destinationCredentialIdentifier = 'jenkins-staging-docker-prod-token'
        def destinationType = 'docker'

        binding.setVariable('sourceImagePath', sourceImagePath)
        binding.setVariable('destinationImagePath', destinationImagePath)
        binding.setVariable('destinationType', destinationType)
        binding.setVariable('destinationCredentialIdentifier', destinationCredentialIdentifier)

        super.testPipeline("tests/jenkins/jobs/CopyDockerImage_docker_Jenkinsfile")
        verifyCopyDockerImageParams(helper, sourceImagePath, destinationImagePath,
                destinationType, destinationCredentialIdentifier, null)
    }

    @Test
    public void testForEcr() {
        def destinationCredentialIdentifier = 'jenkins-staging-docker-prod-token'
        def accountName = 'DUMMY_NAME'
        def destinationType = 'ecr'

        binding.setVariable('sourceImagePath', sourceImagePath)
        binding.setVariable('destinationImagePath', destinationImagePath)
        binding.setVariable('destinationType', destinationType)
        binding.setVariable('destinationCredentialIdentifier', destinationCredentialIdentifier)
        binding.setVariable('accountName', accountName)

        super.testPipeline("tests/jenkins/jobs/CopyDockerImage_ecr_Jenkinsfile")

        verifyCopyDockerImageParams(helper, sourceImagePath, destinationImagePath,
                destinationType, destinationCredentialIdentifier, accountName)
    }

    static void verifyCopyDockerImageParams(helper, sourceImagePath, destinationImagePath,
                                            destinationType, destinationCredentialIdentifier, accountName) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'copyDockerImage'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'copyDockerImage'
        }.each { call ->
            assertThat(call.args.sourceImagePath.first(), notNullValue())
            assertThat(call.args.destinationImagePath.first(), notNullValue())
            assertThat(call.args.destinationType.first(), notNullValue())
            assertThat(call.args.destinationType.first(), anyOf(equalTo('ecr'), equalTo('docker')))
            assertThat(call.args.destinationCredentialIdentifier.first(), notNullValue())
            if(call.args.destinationType.first() == "docker") {
                assertThat(call.args.destinationCredentialIdentifier.first(), anyOf(equalTo('jenkins-staging-docker-prod-token'),
                        equalTo('jenkins-staging-docker-staging-credential')))
            }
            if(call.args.destinationType.first() == "ecr"){
                assertThat(call.args.accountName.first(), notNullValue())
                assert call.args.accountName.first() == accountName
            }
            assert call.args.sourceImagePath.first() == sourceImagePath
            assert call.args.destinationImagePath.first() == destinationImagePath
            assert call.args.destinationCredentialIdentifier.first() == destinationCredentialIdentifier
            assert call.args.destinationType.first() == destinationType
        }
    }
}
