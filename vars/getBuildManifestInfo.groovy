Map call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    String buildManifestFileName = 'manifest.yml'
    echo "Setting BUILD_MANIFEST=${buildManifestFileName}"
    env.BUILD_MANIFEST = buildManifestFileName
    
    sh "wget ${BUILD_MANIFEST_URL} -O ${buildManifestFileName}"
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: "${buildManifestFileName}"))
    String architecture = buildManifest.getArtifactArchitecture()
    String buildId = buildManifest.getArtifactBuildId()
    echo "Setting ARCHITECTURE=${architecture}"
    env.ARCHITECTURE = architecture
    echo "Setting BUILD_ID=${buildId}"
    env.BUILD_ID = buildId
}