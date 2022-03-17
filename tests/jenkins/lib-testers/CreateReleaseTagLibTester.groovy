import jenkins.BuildManifest
import org.yaml.snakeyaml.Yaml

import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class CreateReleaseTagLibTester extends LibFunctionTester {

    private String distManifest
    private String tagVersion
    private ArrayList buildManifestComponentsList

    public CreateReleaseTagLibTester(distManifest, tagVersion){
        this.distManifest = distManifest
        this.tagVersion = tagVersion
        this.buildManifestComponentsList = []
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.distManifest.first(), notNullValue())
        assertThat(call.args.tagVersion.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.distManifest.first().toString().equals(this.distManifest)
                && call.args.tagVersion.first().toString().equals(this.tagVersion)
                && this.buildManifestComponentsList.size() > 1
    }

    String libFunctionName(){
        return 'createReleaseTag'
    }

    void configure(helper, binding){
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'dummy_token_name')
        binding.setVariable('GITHUB_USER', 'dummy_user')
        binding.setVariable('GITHUB_TOKEN', 'dummy_token')

        helper.registerAllowedMethod("checkout", [Map], {})
        helper.registerAllowedMethod("dir", [Map], {})
        InputStream inputStream = new FileInputStream(new File(this.distManifest));
        Yaml yaml = new Yaml()
        Map ymlMap = yaml.load(inputStream)
        BuildManifest buildManifestObj = new BuildManifest(ymlMap)
        this.buildManifestComponentsList = buildManifestObj.getNames()
        boolean checkFirst = true
        for (component in this.buildManifestComponentsList) {
            def repo = buildManifestObj.getRepo(component)
            def version = "$tagVersion.0"
            if (component == "OpenSearch" || component == "OpenSearch-Dashboards" || component == "functionalTestDashboards") {
                version = tagVersion
            }
            def out = ""
            if (checkFirst) {
                out = buildManifestObj.getCommitId(component)
                checkFirst = false
            }
            helper.addShMock("git ls-remote --tags $repo $version | awk 'NR==1{print \$1}'") { script ->
                return [stdout: out, exitValue: 0]
            }
        }
    }
}
