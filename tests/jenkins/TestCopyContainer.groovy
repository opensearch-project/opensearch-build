import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestCopyContainer extends BuildPipelineTest {

    String sourceImage = 'samplerepo/alpine:3.15.4'
    String destinationImage = 'alpine:3.15.4'

    @Before
    void setUp() {
        /*this.registerLibTester(new CopyContainerLibTester(sourceImage,
                "public.ecr.aws/opensearchstaging/${destinationImage}",
                'ecr',
                false))*/
        helper.registerAllowedMethod('withAWS', [Map, Closure], null)
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'ecr')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', false)
        super.setUp()

    }


    /*@Test
    public void testCopyContainerDockerStaging() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', 'DockerHub')
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', false)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-DockerHubStaging.jenkinsfile")
    }*/

    /*@Test
    public void testCopyContainerDockerProd() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', "DockerHub")
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', true)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-DockerHubProd.jenkinsfile")
    }*/

    @Test
    public void testCopyContainerECRStaging() {

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-ECRStaging.jenkinsfile")
    }

    /*@Test
    public void testCopyContainerECRProd() {

        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', "ECR")
        binding.setVariable('DESTINATION_IMAGE', destinationImage)
        binding.setVariable('prod', true)

        super.testPipeline("jenkins/docker/docker-copy.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-copy-ECRProd.jenkinsfile")
    }*/

}
