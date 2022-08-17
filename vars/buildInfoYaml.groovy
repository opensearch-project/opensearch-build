def call(Map args = [:]) {

    def inputManifest = readYaml(file: args.inputManifest)
    def outputFile = args.outputFile
    def components = args.componentName
    def componentsList = []
    def status = args.status
    echo("The status is $status")
    echo("Components is $components")
    if (!components.isEmpty()) {
        echo ("Components parameter is not null")
        for (component in components.split(" ")) {
            componentsList.add(component.trim())
        }
    } else {
        echo ("Components parameter is null")
        inputManifest.components.each { component ->
            componentsList.add(component.name)
        }
    }
    echo (componentsList.toString())
    if (args.stage == "START") {
        echo("Initiate the buildInfo yaml file.")
        inputManifest.build.status = "IN_PROGRESS"
        inputManifest.build.number = "${BUILD_NUMBER}"
        inputManifest.results = [:]
        inputManifest.results.integ_test_x64 = status
        inputManifest.results.bwc_test_x64 = status
        inputManifest.results.integ_test_arm64 = status
        inputManifest.results.bwc_test_arm64 = status
        inputManifest.results.x64_tar = status
        inputManifest.results.arm64_tar = status
        inputManifest.results.x64_rpm = status
        inputManifest.results.arm64_rpm = status
        inputManifest.components.each { component ->
            if (componentsList.contains(component.name)) {
                // Convert ref from branch to commit
                dir (component.name) {
                    checkout([$class: 'GitSCM', branches: [[name: component.ref]],
                              userRemoteConfigs: [[url: component.repository]]])
                    def commitID = sh (
                            script: "git rev-parse HEAD",
                            returnStdout: true
                    ).trim()
                    component.ref = commitID
                }
            }
        }
    }
    else if (args.stage == "x64_tar" || args.stage == "x64_rpm" || args.stage == "arm64_tar" || args.stage == "arm64_rpm") {
        stageField = args.stage
        echo("stage is $stageField")
        echo("status is $status")
        inputManifest.results.("$stageField".toString()) = "$status"
    }
    else if (args.stage == "integ_test_x64" || args.stage == "integ_test_arm64" || args.stage == "bwc_test_x64" || args.stage == "bwc_test_arm64") {
        stageField = args.stage
        echo("stage is $stageField")
        echo("status is $status")
        inputManifest.results.("$stageField".toString()) = "$status"
    }
    else if (args.stage == "COMPLETE") {
        inputManifest.build.status = status
        inputManifest.results.duration = currentBuild.duration
        inputManifest.results.startTimestamp = currentBuild.startTimeInMillis
    }
    writeYaml(file: outputFile, data: inputManifest, overwrite: true)
    sh ("cat $outputFile")
}
