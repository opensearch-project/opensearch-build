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
    def name = BundleManifestObj.build.getFilename()   //opensearch-dashboards
    def version = BundleManifestObj.build.version        //1.3.0
    def architecture = BundleManifestObj.build.architecture
    def plugin_names = BundleManifestObj.getNames();

    def latestOpenSearchURLRoot = "https://ci.opensearch.org/ci/dbc/Playground/tianleh-test/tianle-opensearch-build-3-22"
    def latestOpenSearchURL = "$latestOpenSearchURLRoot/$version/latest/linux/$architecture/rpm/dist/opensearch/opensearch-$version-linux-${architecture}.rpm"
    def latestOpensearchDist = "$WORKSPACE/opensearch-$version-linux-${architecture}.rpm"
    // Download the latest OpenSearch distribution with same version to be compatible with Dashboards.
    sh("curl -SLO $latestOpenSearchURL")

    // This is a reference meta data which the distribution should be consistent with.
    def refMap = [:]
    refMap['Name'] = name
    refMap['Version'] = version
    refMap['Architecture'] = architecture
    refMap['Group'] = "Application/Internet"
    refMap['License'] = "Apache-2.0"
    refMap['Relocations'] = "(not relocatable)"
    refMap['URL'] = "https://opensearch.org/"
    // The context of meta data should be for OSD
    refMap['Summary'] = "Open source visualization dashboards for OpenSearch"
    refMap['Description'] = "OpenSearch Dashboards is the visualization tool for data in OpenSearch\n" +
            "For more information, see: https://opensearch.org/"

    //Validation for the Meta Data of distribution
    rpmMetaValidation(
            rpmDistribution: distFile,
            refMap: refMap
    )

    //Validation for the installation
    //Install the rpm distribution via yum
    println("Start installations of OpenSearch & OpenSearch-Dashboards with yum.")
    packageManagerCall(
            call: "install",
            product: latestOpensearchDist
    )
    println("Latest RPM distribution for OpenSearch is also installed with yum.")
    packageManagerCall(
            call: "install",
            product: distFile
    )
    println("RPM distribution for $name is installed with yum.")

    //Start the installed OpenSearch-Dashboards distribution
    processManagerCall(
            call: "restart",
            product: "opensearch"
    )
    processManagerCall(
            call: "restart",
            product: name
    )

    //Validate if the running status is succeed
    def running_status = processManagerCall(
                            call: "status",
                            product: name
    )
    def active_status_message = "Active: active (running)"
    if (running_status.contains(active_status_message)) {
        println("After checking the status, the installed $name is actively running!")
    } else {
        error("Something went run! Installed $name is not actively running.")
    }

    //Start validate if this is dashboards distribution.
    println("This is a dashboards validation.")
    def osd_status_json = sh (
            script: "curl -s \"http://localhost:5601/api/status\"",
            returnStdout: true
    ).trim()
    for (int i = 0; i < 10; i++) {
        if (osd_status_json == "") {
            sleep 3
            osd_status_json = sh (
                    script: "curl -s \"http://localhost:5601/api/status\"",
                    returnStdout: true
            ).trim()
        } else {
            break
        }
    }
    println("Dashboards status are here: \n" + osd_status_json)
    def osd_status = readJSON(text: osd_status_json)
    assert osd_status["version"]["number"] == version
    println("Dashboards host version has been validated.")
    assert osd_status["status"]["overall"]["state"] == "green"
    println("OpenSearch Dashboards overall state is running green.")

    //Plugin existence validation;
    def osd_plugins = sh (
            script: "/usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin list",
            returnStdout: true
    ).trim()
    println("osd_plugins are: \n" + osd_plugins)
    def components_list = []
    for (component in plugin_names) {
        if (component == "OpenSearch-Dashboards" || component == "functionalTestDashboards") {
            continue
        }
        def location = BundleManifestObj.getLocation(component)
        def component_name_with_version = location.split('/').last().minus('.zip') //e.g. anomalyDetectionDashboards-1.3.0
        components_list.add(component_name_with_version)
    }
    for (component in components_list) {
        def component_with_version = component.replace("-","@") + ".0"  //e.g. anomalyDetectionDashboards@1.3.0.0
        assert osd_plugins.contains(component_with_version)
        println("Component $component is present with correct version $version." )
    }

    processManagerCall(
            call: "stop",
            product: name
    )
    packageManagerCall(
            call: "remove",
            product: "opensearch-dashboards"
    )
    processManagerCall(
            call: "stop",
            product: "opensearch"
    )
    packageManagerCall(
            call: "remove",
            product: "opensearch"
    )
}
