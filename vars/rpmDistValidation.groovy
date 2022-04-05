def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def DistributionManifestObj = lib.jenkins.DistributionManifest.new(readYaml(file: args.distManifest))
    def distFile = args.rpmDistribution         //Distribution file location
    def name = DistributionManifestObj.build.getFilename()   //opensearch; opensearch-dashboards
    def version = DistributionManifestObj.build.version        //1.3.0
    def architecture = DistributionManifestObj.build.architecture
    def plugin_names = DistributionManifestObj.getNames();
    def latestOpenSearchURL = "https://ci.opensearch.org/ci/dbc/Playground/tianleh-test/tianle-opensearch-build-3-22/$version/latest/linux/$architecture/rpm/dist/opensearch/opensearch-$version-linux-${architecture}.rpm"
    def latestOpensearchDist = "$WORKSPACE/opensearch-$version-linux-${architecture}.rpm"

    if (name == "opensearch-dashboards") {
        sh("curl -SLO $latestOpenSearchURL")
    }

    if (DistributionManifestObj.build.distribution != 'rpm') {
        error("Invalid distribution manifest. Please input the correct one.")
    }

    // This is a reference meta data which the distribution should be consistent with.
    def refMap = [:]
    refMap['Name'] = name
    refMap['Version'] = version
    refMap['Architecture'] = architecture
    refMap['Group'] = "Application/Internet"
    refMap['License'] = "Apache-2.0"
    refMap['Relocations'] = "(not relocatable)"
    refMap['URL'] = "https://opensearch.org/"
    switch (name) {
        case "opensearch":
            // The context the meta data should be for OpenSearch
            refMap['Summary'] = "An open source distributed and RESTful search engine"
            refMap['Description'] = "OpenSearch makes it easy to ingest, search, visualize, and analyze your data.\n" +
                    "For more information, see: https://opensearch.org/"
            break
        case "opensearch-dashboards":
            // The context of meta data should be for OSD
            refMap['Summary'] = "Open source visualization dashboards for OpenSearch"
            refMap['Description'] = "OpenSearch Dashboards is the visualization tool for data in OpenSearch\n" +
                    "For more information, see: https://opensearch.org/"
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

    //Validation for the Meta Data of distribution
    println("Meta data validations start:")
    def metadata = sh (
            script: "rpm -qip $distFile",
            returnStdout: true
    ).trim()
    println("Meta data for the RPM distribution is: ")
    println(metadata)
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
            if (value == 'x64') {        //up to change if naming confirmed in the distribution manifest
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
    sh "sudo yum install -y $distFile"
    println("RPM distribution for $name is installed with yum.")
    if (name == "opensearch-dashboards") {
        sh "sudo yum install -y $latestOpensearchDist"
        println("Latest RPM distribution for OpenSearch is also installed with yum.")
    }

    if (name == "opensearch") {
        // The validation for opensearch only.
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
    }

    //Start the installed OpenSearch/OpenSearch-Dashboards distribution
    sh ("sudo systemctl restart $name")
    sleep 30    // We will need to start OpenSearch no matter if we are validating for opensearch or OSD
    sh ("sudo systemctl restart opensearch")
    sleep 30    //wait for 30 secs for opensearch to start
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

    if (name == "opensearch") {
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
            def location = DistributionManifestObj.getLocation(component)
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
    } else {
        //Start validate if this is dashboards distribution.
        println("This is a dashboards validation.")
        def osd_status = sh (
                script: "curl -s \"http://localhost:5601/api/status\"",
                returnStdout: true
        ).trim()
        println("Dashboards status are here: \n" + osd_status)
        def osd_status_json = readJSON(text: osd_status)
        assert osd_status_json["version"]["number"] == version
        println("Dashboards host version has been validated.")
        assert osd_status_json["status"]["overall"]["state"] == "green"
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
            def location = DistributionManifestObj.getLocation(component)
            def component_name_with_version = location.split('/').last().minus('.zip') //e.g. anomalyDetectionDashboards-1.3.0
            components_list.add(component_name_with_version)
        }
        for (component in components_list) {
            def component_with_version = component.replace("-","@") + ".0"  //e.g. anomalyDetectionDashboards@1.3.0.0
            assert osd_plugins.contains(component_with_version)
            println("Component $component is present with correct version $version." )
        }
    }

    // Stop OpenSearch/Dashboards and uninstall them with yum
    if(name == "opensearch-dashboards") {
        sh ("sudo systemctl stop opensearch-dashboards")
        sh ("sudo yum remove -y opensearch-dashboards")
    }
    sh ("sudo systemctl stop opensearch")
    sh ("sudo yum remove -y opensearch")
}
