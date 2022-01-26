import jenkins.tests.BuildPipelineTest

abstract class LibFunctionTester extends BuildPipelineTest {

    // Used for testing the library function
    abstract String libFunctionName()
    abstract void parameterInvariantsAssertions(call)
    abstract boolean expectedParametersMatcher(call)

    // used to setup the variable values for the library
    abstract void configure(helper, binding)

    void verifyParams(helper){

        def callList = helper.callStack.findAll { call ->
            call.methodName == libFunctionName()
        }

        assert callList.size() > 0

        callList.each ( this.&parameterInvariantsAssertions )

        assert callList.any( this.&expectedParametersMatcher )
    }

}
