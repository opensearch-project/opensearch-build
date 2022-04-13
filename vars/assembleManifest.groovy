void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    def baseUrl = buildManifest.getArtifactRootUrlWithoutDistribution("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    sh([
        './assemble.sh',
        "\"${args.buildManifest}\"",
        "--base-url ${baseUrl}"
    ].join(' '))

    if (args.distribution == 'rpm') {
        echo "Creating repo file and data for ${args.buildManifest}"

        def filename = buildManifest.build.getFilename()
        def name = buildManifest.build.name
        def version = buildManifest.build.version
        def repoFilePath = "${args.distribution}/dist/${filename}"

        sh([
            'createrepo',
            "\"${repoFilePath}\"",
        ].join(' '))

        def repoFileContent = [
            "[${filename}-staging-${version}-${BUILD_NUMBER}]",
            "name=${name} ${version} ${BUILD_NUMBER} Staging",
            "baseurl=${baseUrl}/${args.distribution}/dist/${filename}/",
            "enabled=1",
            "autorefresh=1",
            "type=rpm-md"
        ].join('\n')

        writeFile file: "${repoFilePath}/${filename}-artifacts.repo", text: repoFileContent
    }
}
