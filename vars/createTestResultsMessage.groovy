def call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    String testType = args.testType
    String status = args.status
    String absoluteUrl = args.absoluteUrl
    String icon = status == 'SUCCESS' ? ':white_check_mark:' : ':warning:'

    lib.jenkins.Messages.new(this).add(
        "${STAGE_NAME}",
        lib.jenkins.Messages.new(this).get(["${STAGE_NAME}"]) + 
        "\n${testType}: ${icon} ${status} ${absoluteUrl}"
    )
}