/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    def minArtifactPath = buildManifest.getMinArtifact()
    def productFilename = buildManifest.build.getFilename()
    def packageName = buildManifest.build.getPackageName()
    def distribution = buildManifest.build.distribution

    def artifactPath = buildManifest.getArtifactRoot("${JOB_NAME}", "${BUILD_NUMBER}")

    withCredentials([
        string(credentialsId: 'jenkins-artifact-bucket-name', variable: 'ARTIFACT_BUCKET_NAME'),
        string(credentialsId: 'jenkins-artifact-production-bucket-name', variable: 'ARTIFACT_PRODUCTION_BUCKET_NAME'),
        string(credentialsId: 'jenkins-aws-production-account', variable: 'AWS_ACCOUNT_ARTIFACT'),
        string(credentialsId: 'jenkins-artifact-promotion-role', variable: 'ARTIFACT_PROMOTION_ROLE_NAME')]) {
        echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

        uploadToS3(
                sourcePath: "${distribution}/builds",
                bucket: "${ARTIFACT_BUCKET_NAME}",
                path: "${artifactPath}/builds"
        )

        uploadToS3(
                sourcePath: "${distribution}/dist",
                bucket: "${ARTIFACT_BUCKET_NAME}",
                path: "${artifactPath}/dist"
        )

        echo "Uploading to s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${artifactPath}"

        withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
            s3Upload(file: "${distribution}/builds/${productFilename}/${minArtifactPath}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "release-candidates/core/${productFilename}/${buildManifest.build.version}/")
            s3Upload(file: "${distribution}/dist/${productFilename}/${packageName}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "release-candidates/bundle/${productFilename}/${buildManifest.build.version}/")
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/${productFilename}/manifest.yml",
            "${baseUrl}/dist/${productFilename}/manifest.yml"
        ].join('\n')
    )
}
