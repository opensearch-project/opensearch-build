import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestDockerBuildWithEcrJob extends BuildPipelineTest {

    @Before
    void setUp() {

        String imageRepository = 'ci-runner-staging'
        String imageTag = 'latest'
        String accountName = 'aws_account_public'


        this.registerLibTester(new CopyContainerLibTester("opensearchstaging/${imageRepository}:${imageTag}",
                "public.ecr.aws/m0o1u6w1/${imageRepository}:${imageTag}",
                'ecr',
                'public.ecr.aws/m0o1u6w1',
                accountName))

        super.setUp()
        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', 'dummy_command')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', accountName)

    }

    @Test
    public void testDockerForEcrOnlyJobStaging() {

        binding.setVariable('PLATFORM', 'ECR')

        helper.registerAllowedMethod("git", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-with-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-with-only-ecr.jenkinsfile")
    }

    @Test
    public void testDockerForEcrAndDockerhubJobStaging() {

        binding.setVariable('PLATFORM', 'docker-hub + ECR')
        binding.setVariable('DOCKER_USERNAME ', 'docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'docker_password')

        helper.registerAllowedMethod("git", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-with-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-with-ecr-dockerhub.jenkinsfile")
    }

}
