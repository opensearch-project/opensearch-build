/**
 * This is a general function for RPM distribution validation.
 * @param Map args = [:]
 * args.bundleManifest: The location of the distribution manifest.
 * args.rpmDistribution: The location of the RPM distribution file.
 */
def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def BundleManifestObj = lib.jenkins.BundleManifest.new(readYaml(file: args.bundleManifest))
    def distFile = args.rpmDistribution
    def name = BundleManifestObj.build.getFilename()   //opensearch; opensearch-dashboards
    def version = BundleManifestObj.build.version        //1.3.0
    def architecture = BundleManifestObj.build.architecture
    def plugin_names = BundleManifestObj.getNames();

    if (BundleManifestObj.build.distribution != 'rpm') {
        error("Invalid distribution manifest. Please input the correct one.")
    }

    //Validation for the Name convention
    println("Name convention for distribution file starts:")
    def distFileNameWithExtension = distFile.split('/').last()
    println("the File name is : $distFileNameWithExtension")        //e.g. opensearch-1.3.0-linux-x64.rpm
    if (!distFileNameWithExtension.endsWith(".rpm")) {
        error("This isn't a valid rpm distribution.")
    }
    def distFileName = distFileNameWithExtension.replace(".rpm", "")
    def refFileName = [name, version, "linux", architecture].join("-")
    assert distFileName == refFileName
    println("File name for the RPM distribution has been validated.")

    if (name == "opensearch") {
        rpmOpenSearchDistValidation(
                bundleManifestObj: BundleManifestObj,
                rpmDistribution: distFile
        )
    } else {
        rpmDashboardsDistValidation(
                bundleManifestObj: BundleManifestObj,
                rpmDistribution: distFile
        )
    }
}
