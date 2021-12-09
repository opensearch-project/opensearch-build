void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    buildManifest(args)

    echo "Archiving into zip: builds/**, ${args.manifest}"

    zip(
        zipFile: "archived-builds.zip",
        archive: true,
        glob: 'builds/**'
    )

    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}.")
}
