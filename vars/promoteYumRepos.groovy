/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))

    String filename = inputManifest.build.getFilename()
    String jobname = args.jobName

    String buildnumber = args.buildNumber ?: 'none'
    if (buildnumber == 'none') {
        println('User did not enter build number in jenkins parameter, exit 1')
        System.exit(1)
    }

    String version = inputManifest.build.version
    String majorVersion = version.tokenize('.')[0]
    String yumRepoVersion = majorVersion + '.x'
    String qualifier = inputManifest.build.qualifier ? '-' + inputManifest.build.qualifier : ''
    String revision = version + qualifier
    println("Product: ${filename}")
    println("Build Number: ${buildnumber}")
    println("Input Manifest: ${manifest}")
    println("Revision: ${revision}")
    println("Major Version: ${majorVersion}")
    println("Yum Repo Version: ${yumRepoVersion}")

    String stagingYumPathX64 = "${PUBLIC_ARTIFACT_URL}/${jobname}/${revision}/${buildnumber}/linux/x64/rpm/dist/${filename}/${filename}-${revision}-linux-x64.rpm"
    String stagingYumPathARM64 = "${PUBLIC_ARTIFACT_URL}/${jobname}/${revision}/${buildnumber}/linux/arm64/rpm/dist/${filename}/${filename}-${revision}-linux-arm64.rpm"

    String localPath = "${WORKSPACE}/artifacts"
    String yumRepoProdPath = "releases/bundle/${filename}/${yumRepoVersion}/yum"
    String artifactPath = "${localPath}/${yumRepoProdPath}"

    withCredentials([string(credentialsId: 'jenkins-artifact-promotion-role', variable: 'ARTIFACT_PROMOTION_ROLE_NAME'),
        string(credentialsId: 'jenkins-aws-production-account', variable: 'AWS_ACCOUNT_ARTIFACT'),
        string(credentialsId: 'jenkins-artifact-production-bucket-name', variable: 'ARTIFACT_PRODUCTION_BUCKET_NAME')]) {
            withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
                println('Pulling Prod Yumrepo')
                sh("aws s3 sync s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${yumRepoProdPath}/ ${artifactPath}/ --no-progress")
            }

        sh """
            set -e
            set +x
            set +x

            echo "Pulling ${revision} rpms"
            cd ${artifactPath}
            curl -SLO ${stagingYumPathX64}
            curl -SLO ${stagingYumPathARM64}

            ls -l

            rm -vf repodata/repomd.xml.asc

            echo "Update repo metadata"
            createrepo --update .

            # Rename .xml to .pom for signing
            # Please do not add .xml to signer filter
            # As maven have many .xml and we do not want to sign them
            # This is an outlier case for yum repo only
            mv -v repodata/repomd.xml repodata/repomd.pom

            echo "Complete metadata update, awaiting signing repomd.xml"

        cd -

    """

        signArtifacts(
            artifactPath: "${artifactPath}/repodata/repomd.pom",
            sigtype: '.sig',
            platform: 'linux'
            )

        sh """
            set -e
            set +x

            cd ${artifactPath}/repodata/

            ls -l

            mv -v repomd.pom repomd.xml
            mv -v repomd.pom.sig repomd.xml.sig

            # This step is required as yum only accept .asc and signing workflow only support .sig
            cat repomd.xml.sig | gpg --enarmor | sed 's@ARMORED FILE@SIGNATURE@g' > repomd.xml.asc

            rm -vf repomd.xml.sig

            ls -l

            cd -
    """

        withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
            println('Pushing Prod Yumrepo')
            sh("aws s3 sync ${artifactPath}/ s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${yumRepoProdPath}/ --no-progress")
        }
        }
}
