/**
 * This is a general function for RPM distribution validation.
 * @param Map args = [:]
 * args.name: The name of the product we are testing for running status.
 */
def call(Map args = [:]) {

    def name = args.name

    //Validate if the running status is succeed
    def running_status = sh (
            script: "sudo systemctl status $name",
            returnStdout: true
    ).trim()
    def active_status_message = "Active: active (running)"
    if (running_status.contains(active_status_message)) {
        println("After checking the status, the installed $name is actively running!")
    } else {
        error("Something went run! Installed $name is not actively running.")
    }
}
