def call(Map args = [:]) {

    try {
        unstash "job_yml"
    } catch(Exception ex) {
        echo("No job.yml exists in stashed. Please make sure inputManifest parameter is passed.")
    }

    def inputManifest = args.inputManifest ?: "job.yml"
    def sourceyml = readYaml(file: inputManifest)
    def outputyml = args.outputyml ?: "job.yml"
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

    if (args.stage == "START") {
        echo("Initiate the job info yaml file.")
        sourceyml.build.status = "IN_PROGRESS"
        sourceyml.build.number = "${BUILD_NUMBER}"
        sourceyml.results = [:]
    } else if (args.stage == "COMPLETE") {
        sourceyml.components.each { component ->
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
        sourceyml.build.status = status
    } else {
        stageField = args.stage
        echo("stage is $stageField")
        echo("status is $status")
        sourceyml.results.("$stageField".toString()) = status
        sourceyml.results.duration = currentBuild.duration
        sourceyml.results.startTimestamp = currentBuild.startTimeInMillis
    }
    writeYaml(file: outputyml, data: sourceyml, overwrite: true)
    sh ("cat $outputyml")
    stash includes: "job.yml", name: "job_yml"
}
