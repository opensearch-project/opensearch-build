/**
 * This is a helper method for package manager yum call.
 * @param Map args = [:]
 * args.call: The command that we want to run with SystemD.
 * args.product: The name of the product we are testing for running status.
 */
def call(Map args = [:]) {

    def command = args.call
    def product = args.product
    switch (command) {
        case ("install"):
            sh ("sudo yum install -y $product")
            break
        case ("remove"):
            sh ("sudo yum remove -y $product")
    }

}
