import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerBuildWithDockerhubOnlyJob extends BuildPipelineTest {

    @Before
    void setUp() {

        String imageRepository = 'ci-runner-staging'
        String imageTag = 'latest'
        String accountName = 'aws_account_public'

        super.setUp()
        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', 'dummy_command')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', accountName)
        binding.setVariable('PLATFORM', 'docker-hub')

    }

    @Test
    public void testDockerWithDockerhubOnlyJobStaging(){

        binding.setVariable('DOCKER_USERNAME ', 'docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'docker_password')

        helper.registerAllowedMethod("git", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-with-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-with-dockerhub-only.jenkinsfile")
        }

}
