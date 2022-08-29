/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestCopyContainer extends BuildPipelineTest {

    String sourceImage = 'alpine:3.15.4'
    String destinationImage = 'alpine:3.15.4'

    @Before
    void setUp() {
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'sample-agent-AssumeRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234567890')
        binding.setVariable('DATA_PREPPER_STAGING_CONTAINER_REPOSITORY', 'sample_dataprepper_ecr_url')
        helper.registerAllowedMethod('withAWS', [Map, Closure], null)
        super.setUp()

    }

    @Test
    public void testCopyContainerDockerStagingToDockerProd() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'opensearchstaging')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'opensearchproject')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerDockerStagingToDockerProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerDockerStagingToEcrProd() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'opensearchstaging')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'public.ecr.aws/opensearchproject')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerDockerStagingToEcrProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerECRStagingtoDockerProd() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'public.ecr.aws/opensearchstaging')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'opensearchproject')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerECRStagingtoDockerProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerDockerProdtoEcrProd() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'opensearchproject')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'public.ecr.aws/opensearchproject')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerDockerProdtoEcrProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerEcrStagingtoEcrProd() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'public.ecr.aws/opensearchstaging')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'public.ecr.aws/opensearchproject')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerEcrStagingtoEcrProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerDockerStagingtoEcrStaging() {

        binding.setVariable('SOURCE_IMAGE_REGISTRY', 'opensearchstaging')
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'public.ecr.aws/opensearchstaging')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker/docker-copy-testCopyContainerDockerStagingtoEcrStaging.jenkinsfile")
    }

}
