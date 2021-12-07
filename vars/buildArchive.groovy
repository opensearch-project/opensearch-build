void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    buildManifest(args)

    echo "Archiving into zip: builds/**, ${args.manifest}"

    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}.") 

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: args.manifest))
}
