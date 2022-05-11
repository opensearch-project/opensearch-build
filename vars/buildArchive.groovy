void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    buildManifest(args)

    String stashName = "build-archive-${args.platform}-${args.architecture}-${args.distribution}-${JOB_NAME}-${BUILD_NUMBER}"
    echo "Stashing builds to assemble later with name: ${stashName}"
    stash includes: "${args.distribution}/builds/**", name: "${stashName}"

    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}.")
}
