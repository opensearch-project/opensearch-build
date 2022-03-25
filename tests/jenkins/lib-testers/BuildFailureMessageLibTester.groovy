import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class BuildFailureMessageLibTester extends LibFunctionTester {


    public BuildFailureMessageLibTester() {}


    String libFunctionName() {
        return 'buildFailureMessage'
    }

    void configure(helper, binding){
        binding.setVariable("currentBuild", currentBuild)
    }
}