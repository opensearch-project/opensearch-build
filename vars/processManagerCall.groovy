/**
 * This is a helper method for process manager systemD call.
 * @param Map args = [:]
 * args.call: The command that we want to run with SystemD.
 * args.product: The name of the product we are testing for running status.
 */
def call(Map args = [:]) {

    def command = args.call
    def product = args.product
    switch (command) {
        case ("status"):
            //Validate if the running status is succeed
            def running_status = sh (
                    script: "sudo systemctl status $product",
                    returnStdout: true
            ).trim()
            def active_status_message = "Active: active (running)"
            if (running_status.contains(active_status_message)) {
                println("After checking the status, the installed $product is actively running!")
            } else {
                error("Something went run! Installed $product is not actively running.")
            }
            break
        case ("restart"):
            sh ("sudo systemctl restart $product")
            sleep 30
            break
        case ("stop"):
            sh ("sudo systemctl stop $product")
    }
}
