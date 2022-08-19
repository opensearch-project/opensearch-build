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
    } else if (args.stage == "COMPLETE") {
        inputManifest.components.each { component ->
            if (componentsList.contains(component.name)) {
                // Convert ref from branch to commit
                dir(component.name) {
                    checkout([$class           : 'GitSCM', branches: [[name: component.ref]],
                              userRemoteConfigs: [[url: component.repository]]])
                    def commitID = sh(
                            script: "git rev-parse HEAD",
                            returnStdout: true
                    ).trim()
                    component.ref = commitID
                }
            }
        }
        inputManifest.build.status = status
    } else {
        stageField = args.stage
        echo("stage is $stageField")
        echo("status is $status")
        inputManifest.results.("$stageField".toString()) = "$status"
        inputManifest.results.duration = currentBuild.duration
        inputManifest.results.startTimestamp = currentBuild.startTimeInMillis
    }
    writeYaml(file: outputFile, data: inputManifest, overwrite: true)
    sh ("cat $outputFile")
}
