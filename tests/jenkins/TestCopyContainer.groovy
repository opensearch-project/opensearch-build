import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestCopyContainer extends BuildPipelineTest {

    String sourceImage = 'samplerepo/alpine:3.15.4'
    String destinationImage = 'alpine:3.15.4'

    @Before
    void setUp() {
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'sample-agent-AssumeRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234567890')
         helper.registerAllowedMethod('withAWS', [Map, Closure], null)
        super.setUp()

    }


    @Test
    public void testCopyContainerDockerStaging() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'docker')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', false)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-DockerHubStaging.jenkinsfile")
    }

    @Test
    public void testCopyContainerDockerProd() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', "docker")
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', true)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-DockerHubProd.jenkinsfile")
    }

    @Test
    public void testCopyContainerECRStaging() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', "ecr")
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', false)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-ECRStaging.jenkinsfile")
    }

    @Test
    public void testCopyContainerECRProd() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', "ecr")
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', true)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-ECRProd.jenkinsfile")
    }

}
