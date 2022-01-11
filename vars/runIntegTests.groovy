void call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String testManifest = args.testManifest ?: "manifests/${TEST_MANIFEST}"

    echo "args.architecture: ${args.architecture}"
    String tarball = null
    String buildManifestUrl = null
    if (args.architecture == "x64") {
        tarball = env.BUILD_MANIFEST_URL_linux_x64
        buildManifestUrl = env.BUILD_MANIFEST_URL_linux_x64
    } else if (args.architecture == "arm64") {
        tarball = env.ARTIFACT_URL_linux_arm64
        buildManifestUrl = env.BUILD_MANIFEST_URL_linux_arm64
    } else {
        echo "Architecture ${args.architecture} is invalid"
    }

    echo "testManifest: ${testManifest}"
    echo "buildManifestUrl: ${buildManifestUrl}"

    if (tarball == null) {
        echo "Skipping integ tests for ${args.architecture} architecture because ${args.architecture} artifact was not built."
    } else {
        IntegTests: {
            // TODO: will need to override integ-test in Jenkins with the new workflow in jenkins/opensearch/integ-test.jenkinsfile
            build job: 'Playground/ohltyler-integ-test',
            parameters: [
                string(name: 'TEST_MANIFEST', value: "${testManifest}"),
                string(name: 'BUILD_MANIFEST_URL', value: "${buildManifestUrl}"),
            ]
        }
    }
}