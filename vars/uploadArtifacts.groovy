void call(Map args = [:]) {
    lib = library(identifier: "jenkins@current", retriever: legacySCM(scm)).jenkins

    def manifestFilename = args.manifest ?: 'builds/manifest.yml'
    def buildManifest = lib.BuildManifest.new(readYaml(file: manifestFilename))

    def artifactPath = buildManifest.getArtifactRoot(env.JOB_NAME, env.BUILD_NUMBER)
    echo "Uploading to s3://${env.ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: 'opensearch-bundle', roleAccount: env.AWS_ACCOUNT_PUBLIC, duration: 900, roleSessionName: 'jenkins-session') {
        if (args.upload) {
            s3Upload(file: 'builds', bucket: env.ARTIFACT_BUCKET_NAME, path: "${artifactPath}/builds")
            s3Upload(file: 'dist', bucket: env.ARTIFACT_BUCKET_NAME, path: "${artifactPath}/dist")
        } else {
            echo "s3Upload(file: 'builds', bucket: ${env.ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/builds)"
            echo "s3Upload(file: 'dist', bucket: ${env.ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/dist)"
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl(env.PUBLIC_ARTIFACT_URL, env.JOB_NAME, env.BUILD_NUMBER)
    lib.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/manifest.yml",
            "${baseUrl}/dist/manifest.yml"
        ].join("\n")
    )
}