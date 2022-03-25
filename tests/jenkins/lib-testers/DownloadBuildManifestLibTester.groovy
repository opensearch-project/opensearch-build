import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat
import org.yaml.snakeyaml.Yaml


class DownloadBuildManifestLibTester extends LibFunctionTester {

    private String url
    private String path

    public DownloadBuildManifestLibTester(url, path){
        this.url = url
        this.path = path
    }

    void configure(helper, binding) {
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((path as File).text)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.url.first(), notNullValue())
        assertThat(call.args.path.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.url.first().toString().equals(this.url)
                && call.args.path.first().toString().equals(this.path)
    }

    String libFunctionName() {
        return 'downloadBuildManifest'
    }
}
