import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestDockerBuildEcrJob extends BuildPipelineTest {

    def imageRepository = 'ci-runner-staging'
    def imageTag = 'latest'
    def sourceImagePath = "opensearchstaging/${imageRepository}:${imageTag}"

    @Before
    void setUp() {
        super.setUp()
        TestCopyDockerImage.setUpVariables(binding, helper)
    }

    @Test
    public void testDockerForEcrJobStaging(){

        def accountName = 'aws_account_public'

        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', 'dummy_command')
        binding.setVariable('DOCKER_USERNAME ', 'docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'docker_password')
        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_PUBLIC', accountName)

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("cleanWs", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-build-ecr/docker-build-ecr.jenkinsfile")

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "public.ecr.aws/m0o1u6w1/${imageRepository}:${imageTag}",
                'ecr', 'public.ecr.aws/m0o1u6w1', accountName)

        }

}
