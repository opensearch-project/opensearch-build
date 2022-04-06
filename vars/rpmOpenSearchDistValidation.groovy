def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def bundleManifestObj = args.bundleManifestObj
    def distFile = args.rpmDistribution         //Distribution file location
    def name = bundleManifestObj.build.getFilename()   //opensearch
    def version = bundleManifestObj.build.version        //1.3.0
    def architecture = bundleManifestObj.build.architecture
    def plugin_names = bundleManifestObj.getNames();

    // This is a reference meta data which the distribution should be consistent with.
    def refMap = [:]
    refMap['Name'] = name
    refMap['Version'] = version
    refMap['Architecture'] = architecture
    refMap['Group'] = "Application/Internet"
    refMap['License'] = "Apache-2.0"
    refMap['Relocations'] = "(not relocatable)"
    refMap['URL'] = "https://opensearch.org/"
    // The context the meta data should be for OpenSearch
    refMap['Summary'] = "An open source distributed and RESTful search engine"
    refMap['Description'] = "OpenSearch makes it easy to ingest, search, visualize, and analyze your data.\n" +
            "For more information, see: https://opensearch.org/"

    //Validation for the Meta Data of distribution
    println("Meta data validations start:")
    def metadata = sh (
            script: "rpm -qip $distFile",
            returnStdout: true
    ).trim()
    println("Meta data for the RPM distribution is: \n" + metadata)
    // Extract the meta data from the distribution to Map
    def metaMap = [:]
    for (line in metadata.split('\n')) {
        def key = line.split(':')[0].trim()
        if (key != 'Description') {
            metaMap[key] = line.split(':', 2)[1].trim()
        } else {
            metaMap[key] = metadata.split(line)[1].trim()
            break
        }
    }
    // Start validating
    refMap.each{ key, value ->
        if (key == "Architecture") {
            if (value == 'x64') {
                assert metaMap[key] == 'x86_64'
            } else if (value == 'arm64') {
                assert metaMap[key] == 'aarch64'
            }
        } else {
            assert metaMap[key] == value
        }
        println("Meta data for $key is validated")
    }
    println("Validation for meta data of RPM distribution completed.")

    //Validation for the installation
    //Install the rpm distribution via yum
    println("Start installation with yum.")
    sh ("sudo yum install -y $distFile")
    println("RPM distribution for $name is installed with yum.")

    //Check certs in /etc/opensearch/
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
    sh ("sudo systemctl restart $name")
    sleep 30

    //Validate if the running status is succeed
    def running_status = sh (
            script: "sudo systemctl status $name",
            returnStdout: true
    ).trim()
    def active_status_message = "Active: active (running)"
    if (running_status.contains(active_status_message)) {
        println("After checking the status, the installed $name is actively running!")
    } else {
        error("Something went run! Installed $name is not actively running.")
    }

    //Check the starting cluster
    def cluster_info = sh (
            script:  "curl -s \"https://localhost:9200\" -u admin:admin --insecure",
            returnStdout: true
    ).trim().replaceAll("\"", "").replaceAll(",", "")
    println("Cluster info is: \n" + cluster_info)
    for (line in cluster_info.split("\n")) {
        def key = line.split(":")[0].trim()
        if (key == "cluster_name") {
            assert line.split(":")[1].trim() == name
            println("Cluster name is validated.")
        } else if (key == "number") {
            assert line.split(":")[1].trim() == version
            println("Cluster version is validated.")
        } else if (key == "build_type") {
            assert line.split(":")[1].trim() == 'rpm'
            println("Cluster type is validated as rpm.")
        }
    }
    println("Cluster information is validated.")

    //Cluster status validation
    def cluster_status = sh (
            script:  "curl -s \"https://localhost:9200/_cluster/health?pretty\" -u admin:admin --insecure",
            returnStdout: true
    ).trim().replaceAll("\"", "").replaceAll(",", "")
    println("Cluster status is: \n" + cluster_status)
    for (line in cluster_status.split("\n")) {
        def key = line.split(":")[0].trim()
        if (key == "cluster_name") {
            assert line.split(":")[1].trim() == name
            println("Cluster name is validated.")
        } else if (key == "status") {
            assert line.split(":")[1].trim() == "green"
            println("Cluster status is green!")
        }
    }

    //Check the cluster plugins
    def cluster_plugins = sh (
            script: "curl -s \"https://localhost:9200/_cat/plugins?v\" -u admin:admin --insecure",
            returnStdout: true
    ).trim().replaceAll("\"", "").replaceAll(",", "")
    println("Cluster plugins are: \n" + cluster_plugins)
    def components_list = []
    for (component in plugin_names) {
        if (component == "OpenSearch" || component == "common-utils") {
            continue
        }
        def location = bundleManifestObj.getLocation(component)
        def component_name_with_version = location.split('/').last().minus('.zip') //e.g. opensearch-job-scheduler-1.3.0.0
        components_list.add(component_name_with_version)
    }
    for (line in cluster_plugins.split("\n").drop(1)) {
        def component_name = line.split("\\s+")[1].trim()
        def component_version = line.split("\\s+")[2].trim()
        assert components_list.contains([component_name,component_version].join('-'))
        println("Component $component_name is present with correct version $component_version." )
    }

    println("Installation and running for opensearch has been validated.")

    sh ("sudo systemctl stop opensearch")
    sh ("sudo yum remove -y opensearch")

}
