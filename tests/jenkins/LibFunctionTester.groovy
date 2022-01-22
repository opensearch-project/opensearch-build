import jenkins.tests.BuildPipelineTest

abstract class LibFunctionTester extends BuildPipelineTest {

    abstract String libFunctionName()
    abstract void parameterInvariantsAssertions(call)
    abstract boolean expectedParametersMatcher(call)

    abstract void configure(helper, binding)

    void verifyParams(helper){

        def callList = helper.callStack.findAll { call ->
            call.methodName == this.libFunctionName()
        }

        assert callList.size() > 0

        callList.each ( this.&parameterInvariantsAssertions )

        assert callList.any( this.&expectedParametersMatcher )
    }

}
