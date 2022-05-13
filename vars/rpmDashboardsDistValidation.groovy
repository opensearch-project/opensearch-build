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
    def version = BundleManifestObj.build.version       //2.0.0-rc1
    def rpmVersion = version.replace("-", ".")        //2.0.0.rc1
    def architecture = BundleManifestObj.build.architecture
    def plugin_names = BundleManifestObj.getNames();

    // This is a reference meta data which the distribution should be consistent with.
    def refMap = [:]
    refMap['Name'] = name
    refMap['Version'] = rpmVersion
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
    rpmCommands(
            command: "install",
            product: "opensearch-$rpmVersion"
    )
    println("RPM distribution for OpenSearch $version is also installed with yum.")
    rpmCommands(
            command: "install",
            product: "$name-$rpmVersion"
    )
    println("RPM distribution for $name $version is installed with yum.")

    //Start the installed OpenSearch-Dashboards distribution
    systemdCommands(
            command: "start",
            product: "opensearch"
    )
    systemdCommands(
            command: "start",
            product: name
    )

    //Validate if the running status is succeed
    def running_status = systemdCommands(
                            command: "status",
                            product: name
    )
    def active_status_message = "Active: active (running)"
    if (running_status.contains(active_status_message)) {
        println("After checking the status, the installed $name is actively running!")
    } else {
        error("Something went run! Installed $name is not actively running.")
    }

    // Get the OpenSearch-Dashboards api status after start.
    def osd_status_json = -1
    for (int i = 0; i < 10; i++) {
        if (osd_status_json != 0) {
            sleep 10
            osd_status_json = sh (
                    script: "curl -s \"http://localhost:5601/api/status\" -u admin:admin",
                    returnStatus: true
            )
        } else {
            osd_status_json = sh (
                    script: "curl -s \"http://localhost:5601/api/status\" -u admin:admin",
                    returnStdout: true
            ).trim()
            break
        }
    }
    println("Dashboards status are: \n" + osd_status_json)
    def osd_status = readJSON(text: osd_status_json)
    assert osd_status["version"]["number"] == version
    println("Dashboards host version has been validated.")
    assert osd_status["status"]["overall"]["state"] == "green"
    println("OpenSearch Dashboards overall state is running green.")

    //Plugin existence validation;
    def osd_plugins = sh (
            script: "/usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin list --allow-root",
            returnStdout: true
    ).trim()
    println("osd_plugins are: \n" + osd_plugins)
    def components_list = []
    for (component in plugin_names) {
        if (component == "OpenSearch-Dashboards" || component == "functionalTestDashboards") {
            continue
        }
        def location = BundleManifestObj.getLocation(component)
        def component_name_with_version = location.split('/').last().minus('.zip') //e.g. anomalyDetectionDashboards-2.0.0-rc1
        components_list.add(component_name_with_version)
    }
    for (component in components_list) {
        def component_name = component.split("-").first()
        def component_version = component.minus(component_name + "-")
        if (component_version.contains("-")) {        //It has qualifier
            component_version = component_version.split("-").first() + ".0-" + component_version.split("-").last()
        } else {
            component_version = component_version + ".0"
        }
        def component_with_version = [component_name, component_version].join("@")  //e.g. anomalyDetectionDashboards@2.0.0.0-rc1
        assert osd_plugins.contains(component_with_version)
        println("Component $component is present with correct version $version." )
    }

    systemdCommands(
            command: "stop",
            product: name
    )
    rpmCommands(
            command: "remove",
            product: "opensearch-dashboards"
    )
    systemdCommands(
            command: "stop",
            product: "opensearch"
    )
    rpmCommands(
            command: "remove",
            product: "opensearch"
    )
}
