/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
/**
 * This is a helper method for process manager systemD call.
 * @param Map args = [:]
 * args.command: The command that we want to run with SystemD.
 * args.product: The name of the product we are testing for running status.
 */
def call(Map args = [:]) {

    def command = args.command
    def product = args.product
    switch (command) {
        case ("status"):
            //Validate if the running status is succeed
            def running_status = sh (
                    script: "systemctl status $product",
                    returnStdout: true
            ).trim()
            return running_status
            break
        case ("start"):
            sh ("systemctl start $product")
            break
        case ("restart"):
            sh ("systemctl restart $product")
            break
        case ("stop"):
            sh ("systemctl stop $product")
    }
}
