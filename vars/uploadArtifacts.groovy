void call(Map args = [:]) {
    lib = library(identifier: "jenkins@20211118", retriever: legacySCM(scm))

    def manifestFilename = args.manifest ?: 'builds/manifest.yml'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))

    def buildNumber = args.build_number ?: "${BUILD_NUMBER}"
    def jobName = args.job_name ?: "${JOB_NAME}"
    def artifactPath = buildManifest.getArtifactRoot(jobName, buildNumber)
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: args.role, roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (args.upload) {
            for (dir in args.dirs) {
                s3Upload(file: dir, bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/${dir}")
            }
        } else {
            for (dir in args.dirs) {
                echo "s3Upload(file: ${dir}, bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/${dir})"
            }
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", jobName, buildNumber)

    def paths = []
    for (path in args.paths) {
        paths.add("${baseUrl}/${path}")
    }
    
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", paths.join("\n"))
}