void call(Map args = [:]) {

    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    assembleManifest(args)
    uploadArtifacts(args)

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: args.manifest))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.manifest))
    String artifactUrl = inputManifest.getPublicDistUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}", buildManifest.build.platform, buildManifest.build.architecture)
    echo "Setting env.\"ARTIFACT_URL_${buildManifest.build.platform}_${buildManifest.build.architecture}\"=${artifactUrl}"
    env."ARTIFACT_URL_${buildManifest.build.platform}_${buildManifest.build.architecture}" = artifactUrl
}
