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
    def name = BundleManifestObj.build.getFilename()   //opensearch
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
    // The context the meta data should be for OpenSearch
    refMap['Summary'] = "An open source distributed and RESTful search engine"
    refMap['Description'] = "OpenSearch makes it easy to ingest, search, visualize, and analyze your data\n" +
            "For more information, see: https://opensearch.org/"

    rpmMetaValidation(
            rpmDistribution: distFile,
            refMap: refMap
    )

    //Validation for the installation
    //Install OpenSearch with designated version via yum
    println("Start installation with yum.")
    rpmCommands(
            command: "install",
            product: "$name-$rpmVersion"
    )
    println("RPM distribution for $name is installed with yum.")

    //Check certs in /etc/opensearch/
    //The location of these certs are up to change based on the progress from Security.
    println("Check if the certs are existed.")
    sh ('[[ -d /etc/opensearch ]] && echo "/etc/opensearch directory exists"' +
            '|| (echo "/etc/opensearch does not exist" && exit 1)')
    def certs = sh (
            script: "ls /etc/opensearch",
            returnStdout: true
    ).trim()
    def requiredCerts = ["esnode-key.pem", "kirk.pem", "esnode.pem", "kirk-key.pem", "root-ca.pem"]
    requiredCerts.each {
        if (certs.contains(it)){
            println("$it is found existed")
        } else {
            error("Error fail to find $it certificate.")
        }
    }

    //Check the install_demo_configuration.log
    println("Start validating the install_demo_configuration.log.")
    sh ('[[ -f /var/log/opensearch/install_demo_configuration.log ]] && echo "install_demo_configuration.log exists" ' +
            '|| (echo "install_demo_configuration.log does not exist" && exit 1)')
    def install_demo_configuration_log = sh (
            script: "cat /var/log/opensearch/install_demo_configuration.log",
            returnStdout: true
    ).trim()
    if (install_demo_configuration_log.contains("Success")) {
        println("install_demo_configuration.log validation succeed.")
    } else {
        println("install_demo_configuration.log failed.")
    }

    //Start the installed OpenSearch distribution
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
        error("Something went wrong! Installed $name is not actively running.")
    }

    //Check the starting cluster
    def cluster_info_json = sh (
            script:  "curl -s \"https://localhost:9200\" -u admin:admin --insecure",
            returnStdout: true
    ).trim()
    println("Cluster info is: \n" + cluster_info_json)
    def cluster_info = readJSON(text: cluster_info_json)
    assert cluster_info["cluster_name"] == name
    println("Cluster name is validated.")
    assert cluster_info["version"]["number"] == version
    println("Cluster version is validated.")
    assert cluster_info["version"]["build_type"] == 'rpm'
    println("Cluster type is validated as rpm.")
    println("Cluster information is validated.")

    //Cluster status validation
    def cluster_status_json = sh (
            script:  "curl -s \"https://localhost:9200/_cluster/health?pretty\" -u admin:admin --insecure",
            returnStdout: true
    ).trim()
    println("Cluster status is: \n" + cluster_status_json)
    def cluster_status = readJSON(text: cluster_status_json)
    assert cluster_status["cluster_name"] == name
    println("Cluster name is validated.")
    assert cluster_status["status"] == "green"
    println("Cluster status is green!")

    //Check the cluster plugins
    def cluster_plugins = sh (
            script: "curl -s \"https://localhost:9200/_cat/plugins\" -u admin:admin --insecure",
            returnStdout: true
    ).trim().replaceAll("\"", "").replaceAll(",", "")
    println("Cluster plugins are: \n" + cluster_plugins)
    def components_list = []
    for (component in plugin_names) {
        if (component == "OpenSearch" || component == "common-utils") {
            continue
        }
        def location = BundleManifestObj.getLocation(component)
        def component_name_with_version = location.split('/').last().minus('.zip') //e.g. opensearch-job-scheduler-2.0.0.0-rc1
        components_list.add(component_name_with_version)
    }
    for (line in cluster_plugins.split("\n")) {
        def component_name = line.split("\\s+")[1].trim()
        def component_version = line.split("\\s+")[2].trim()
        assert components_list.contains([component_name,component_version].join('-'))
        println("Component $component_name is present with correct version $component_version." )
    }

    //Check the status of Performance analyzer
    //Check systemctl status
    systemdCommands(
            command: "start",
            product: "opensearch-performance-analyzer"
    )
    def running_status_PA = systemdCommands(
            command: "status",
            product: "opensearch-performance-analyzer"
    )
    if (running_status_PA.contains(active_status_message)) {
        println("After checking the status, the Performance-analyzer plugin is actively running!")
    } else {
        error("Something went wrong! Performance-analyzer is not actively running.")
    }
    //Check logs exist in the /tmp/
    sh ('[[ -f /tmp/PerformanceAnalyzer.log ]] && echo "PerformanceAnalyzer.log exists" ' +
            '|| (echo "PerformanceAnalyzer.log does not exist" && exit 1)')
    sh ('[[ -f /tmp/performance_analyzer_agent_stats.log ]] && echo "performance_analyzer_agent_stats.log exists" ' +
            '|| (echo "performance_analyzer_agent_stats.log does not exist" && exit 1)')
    //Validate the metrics name is CPU_Utilization
    def pa_metrics = sh (
            script:  "curl -s localhost:9600/_plugins/_performanceanalyzer/metrics?metrics=CPU_Utilization\\&agg=avg",
            returnStdout: true
    ).trim()
    println("PA metrics is: \n" + pa_metrics)
    assert pa_metrics.contains("\"timestamp\"")
    assert pa_metrics.contains("\"data\"")
    println("Performance Analyzer is validated.")

    println("Installation and running for opensearch has been validated.")

    systemdCommands(
            command: "stop",
            product: name
    )
    rpmCommands(
            command: "remove",
            product: "opensearch"
    )

}
