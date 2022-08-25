def call(Map args = [:]) {

    try {
        unstash "buildInfo_yml"
    } catch(Exception ex) {
        echo("No buildInfo.yml exists in stashed. Starting initialize the buildInfo yaml file.")
    }

    def inputManifest = args.inputManifest ?: "buildInfo.yml"
    def sourceyml = readYaml(file: inputManifest)
    def outputyml = args.outputyml ?: "buildInfo.yml"
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
        sourceyml.components.each { component ->
            componentsList.add(component.name)
        }
    }
    echo (componentsList.toString())

    if (args.stage == "INITIALIZE_STAGE") {
        echo("Initiate the build info yaml file.")
        sourceyml.build.status = "IN_PROGRESS"
        sourceyml.build.number = "${BUILD_NUMBER}"
        sourceyml.results = [:]
        sourceyml.results.startTimestamp = currentBuild.startTimeInMillis
    } else if (args.stage == "FINALIZE_STAGE") {
        sourceyml.components.each { component ->
            if (componentsList.contains(component.name)) {
                // Convert ref from branch to commit
                dir(component.name) {
                    checkout([$class: 'GitSCM', branches: [[name: component.ref]],
                              userRemoteConfigs: [[url: component.repository]]])
                    def commitID = sh(
                            script: "git rev-parse HEAD",
                            returnStdout: true
                    ).trim()
                    component.ref = commitID
                }
            }
        }
        sourceyml.build.status = status
        sourceyml.results.duration = currentBuild.duration
    } else {
        stageField = args.stage
        echo("stage is $stageField")
        echo("status is $status")
        sourceyml.results.("$stageField".toString()) = status
    }
    writeYaml(file: outputyml, data: sourceyml, overwrite: true)
    sh ("cat $outputyml")
    stash includes: "buildInfo.yml", name: "buildInfo_yml"
}
