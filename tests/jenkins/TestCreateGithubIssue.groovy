package jenkins.tests

import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestCreateGithubIssue extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        this.registerLibTester(new CreateGithubIssueLibTester(["Error building OpenSearch, retry with: ./build.sh manifests/2.2.0/opensearch-2.2.0.yml --component OpenSearch --snapshot"]))
        super.setUp()
    }

    @Test
    public void testCreateGithubIssue() {
        helper.addShMock("gh issue list --repo https://github.com/opensearch-project/OpenSearch.git -S \"[AUTOCUT] OS Distribution Build Failed for OpenSearch-2.0.0 in:title\" --label autocut",'',0)
        super.testPipeline("tests/jenkins/jobs/CreateGithubIssue_Jenkinsfile")
    }

    @Test
    public void testExistingGithubIssue() {
        super.testPipeline("tests/jenkins/jobs/CreateGithubIssueExisting_Jenkinsfile")
    }

}
