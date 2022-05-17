import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerBuildWithDockerhubOnlyJob extends BuildPipelineTest {

    @Before
    void setUp() {

        super.setUp()
        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', 'dummy_command')
        binding.setVariable('DOCKER_HUB', true)
        binding.setVariable('ECR', false)
        binding.setVariable('TAG_LATEST', true)

    }

    @Test
    public void testDockerWithDockerhubOnlyJobStaging(){

        binding.setVariable('DOCKER_USERNAME ', 'docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'docker_password')
        helper.registerAllowedMethod("parameters", [ArrayList])

        helper.registerAllowedMethod("git", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-with-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-with-dockerhub-only.jenkinsfile")
    
    }

}
