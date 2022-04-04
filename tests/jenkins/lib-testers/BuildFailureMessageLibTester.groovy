import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class BuildFailureMessageLibTester extends LibFunctionTester {


    public BuildFailureMessageLibTester() {}


     void parameterInvariantsAssertions(call) {
          //N/A
     }

     boolean expectedParametersMatcher(call) {
        return true
     }


    String libFunctionName() {
        return 'buildFailureMessage'
    }

    void configure(helper, binding){
    }
}