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
    switch (command) {
        case ("setup"):
            sh ("cd /etc/yum.repos.d/ && curl -sSLO $repoFileURL && cd -")
            break
        case ("clean"):
            sh ("yum clean all")
            break
        case ("download"):
            sh ("yum install -y yum-plugin-downloadonly && yum install -y --downloadonly --downloaddir=./yum-download/ $product")
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
