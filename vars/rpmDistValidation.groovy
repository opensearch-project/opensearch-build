/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
/**
 * This is a general function for RPM distribution validation.
 * @param Map args = [:]
 * args.bundleManifestURL: The CI URL of the distribution manifest.
 */
def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def bundleManifestURL = args.bundleManifestURL
    sh ("curl -sL $bundleManifestURL -o $WORKSPACE/manifest.yml")
    def bundleManifest = "$WORKSPACE/manifest.yml"

    def BundleManifestObj = lib.jenkins.BundleManifest.new(readYaml(file: "$bundleManifest"))
    def name = BundleManifestObj.build.getFilename()   //opensearch; opensearch-dashboards
    def version = BundleManifestObj.build.version       //2.0.0-rc1
    def rpmVersion = version.replace("-", ".")        //2.0.0.rc1
    def architecture = BundleManifestObj.build.architecture

    def repoFileURLBackend = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/$version/latest/linux/$architecture/rpm/dist/opensearch/opensearch-${version}.staging.repo"
    def repoFileURLProduct = bundleManifestURL.replace("manifest.yml", "${name}-${version}.staging.repo")

    rpmCommands(
            command: "setup",
            repoFileURL: "$repoFileURLBackend"
    )
    rpmCommands(
            command: "setup",
            repoFileURL: "$repoFileURLProduct"
    )
    rpmCommands(
            command: "clean"
    )
    rpmCommands(
            command: "download",
            product: "$name-$rpmVersion"
    )
    def distFileName = sh(
            script: "ls $WORKSPACE/yum-download/",
            returnStdout: true
    ).trim()
    def distFile = "$WORKSPACE/yum-download/$distFileName"

    if (BundleManifestObj.build.distribution != 'rpm') {
        error("Invalid distribution manifest. Please input the correct one.")
    }

    //Validation for the Name convention
    println("Name convention for distribution file starts:")
    println("The file name is : $distFileName")        //e.g. opensearch-2.0.0.rc1-linux-x64.rpm
    if (!distFileName.endsWith(".rpm")) {
        error("This isn't a valid rpm distribution.")
    }
    def refFileName = BundleManifestObj.build.getBuildLocation().split('/').last()
    println("Name from the manifest is $refFileName")
    assert distFileName == refFileName
    println("File name for the RPM distribution has been validated.")

    if (name == "opensearch") {
        rpmOpenSearchDistValidation(
                bundleManifest: bundleManifest,
                rpmDistribution: distFile
        )
    } else {
        rpmDashboardsDistValidation(
                bundleManifest: bundleManifest,
                rpmDistribution: distFile
        )
    }
}
