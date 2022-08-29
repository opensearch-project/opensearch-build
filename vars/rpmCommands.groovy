/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
/**
 * This is a helper method for package manager yum call.
 * @param Map args = [:]
 * args.command: The command that we want to run with SystemD.
 * args.product: The name of the product we are testing for running status.
 */
def call(Map args = [:]) {

    def command = args.command
    def product = args.product
    def repoFileURL = args.repoFileURL
    def subPubKeyURL = "https://artifacts.opensearch.org/publickeys/opensearch.pgp"
    switch (command) {
        case ("setup"):
            sh ("cd /etc/yum.repos.d/ && curl -sSLO $repoFileURL && cd -")
            sh ("curl -sSLO $subPubKeyURL && rpm --import opensearch.pgp")
            break
        case ("clean"):
            sh ("yum clean all")
            break
        case ("download"):
            sh ("yum install -y yum-utils && yumdownloader $product --destdir=$WORKSPACE/yum-download/")
            break
        case ("install"):
            sh ("yum install -y $product")
            break
        case ("update"):
            sh ("yum update -y $product")
            break
        case ("remove"):
            sh ("yum remove -y $product")
    }

}
