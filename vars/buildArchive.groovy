void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    buildManifest(args)

    echo "Archiving into zip: ${args.distribution}/builds/**, ${args.inputManifest}"

    zip(
        zipFile: "${args.distribution}/archived-builds.zip",
        archive: true,
        glob: "${args.distribution}/builds/**"
    )

    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}.")
}
