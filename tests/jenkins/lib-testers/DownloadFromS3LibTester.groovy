import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.CoreMatchers.anyOf


class DownloadFromS3LibTester extends LibFunctionTester {

    private String sourcePath
    private String bucket
    private String path
    private boolean force

    public DownloadFromS3LibTester(sourcePath, bucket, path, force){
        this.sourcePath = sourcePath
        this.bucket = bucket
        this.path = path
        this.force = force
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.sourcePath.first(), notNullValue())
        assertThat(call.args.bucket.first(), notNullValue())
        assertThat(call.args.path.first(), notNullValue())
        assertThat(call.args.force.first(), notNullValue())
        assertThat(call.args.force.first(), anyOf(is("true"), is("false")))
    }

    boolean expectedParametersMatcher(call) {
        return call.args.sourcePath.first().toString().equals(this.sourcePath)
                && call.args.bucket.first().toString().equals(this.bucket)
                && call.args.path.first().toString().equals(this.path)
                && call.args.force.first() == (this.force)
    }

    String libFunctionName(){
        return 'downloadFromS3'
    }

    void configure(helper, binding){
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }
}
