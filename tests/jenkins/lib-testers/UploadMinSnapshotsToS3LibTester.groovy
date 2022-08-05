import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class UploadMinSnapshotsToS3LibTester extends LibFunctionTester {

    private List<Closure> fileActions
    private String manifest

    public UploadMinSnapshotsToS3LibTester(fileActions, manifest){
        this.fileActions = fileActions
        this.manifest = manifest
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.fileActions.first(), notNullValue())
        assertThat(call.args.manifest.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        boolean actionMatch = call.args.fileActions.size() == 0
        for (actionCall in call.args.fileActions) {
            actionMatch = this.fileActions.any( actionThis -> actionCall.toString().contains(actionThis.toString()) )
        }
        return actionMatch && call.args.manifest.first().toString().equals(this.manifest)
    }

    String libFunctionName(){
        return 'uploadMinSnapshotsToS3'
    }

    void configure(helper, binding){
        binding.setVariable('WORKSPACE', 'tests/data')
        binding.setVariable('productName', 'opensearch')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'dummy_role')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'dummy_bucket')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.addShMock('find tests/data/tar/builds/opensearch/dist -type f') { script ->
            return [stdout: "opensearch-min-1.3.0-linux-x64.tar.gz opensearch-dashboards-min-1.3.0-linux-x64.tar.gz", exitValue: 0]
        }
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }
}
