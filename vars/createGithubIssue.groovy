/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
def call(Map args = [:]){
    def failureMessages = args.message
    List<String> failedComponents = []

    if (failureMessages.size() == 1 && failureMessages[0] == "Build failed") {
        println("No component failed, skip creating github issue.")
    }
    else {
        for(message in failureMessages.unique()){
            java.util.regex.Matcher match = (message =~ /(?<=\bcomponent\s).*/)
            String matched = match[0]
            println(matched.split(" ")[0].trim())
            failedComponents.add(matched.split(" ")[0].trim())
        }

        def yamlFile = readYaml(file: "manifests/${INPUT_MANIFEST}")
        def currentVersion = yamlFile.build.version

        for(component in yamlFile.components){
            if (failedComponents.contains(component.name)) {
                println("Component ${component.name} failed, creating github issue")
                compIndex = failedComponents.indexOf(component.name)
                create_issue(component.name, component.repository, currentVersion, failureMessages[compIndex])
                sleep(time:3,unit:"SECONDS")
            }
        }
    }
}

def create_issue(component, url, currentVersion, failedMessage){
    def versionLabel = "v${currentVersion}"
    def label = "autocut"

    def message = """***Received Error***: **${failedMessage}**.
                      The distribution build for ${component} has failed.
                      Please see build log at ${BUILD_URL}consoleFull""".stripIndent()


    try {
        withCredentials([usernamePassword(credentialsId: 'jenkins-github-bot-token', passwordVariable: 'GITHUB_TOKEN', usernameVariable: 'GITHUB_USER')]) {
            def issues = sh (
                    script: "gh issue list --repo ${url} -S \"[AUTOCUT] OS Distribution Build Failed for ${component}-${currentVersion} in:title\" --label ${label}",
                    returnStdout: true
            )

            def hasLabel = sh (
                    script: "gh label list --repo ${url} -S ${versionLabel}",
                    returnStdout: true
            )

            if (hasLabel){
                label = "\"autocut,${versionLabel}\""
            }

            if (issues){
                println("Issue already exists in the repository, skipping.")
            } else {
                sh (
                        script: "gh issue create --title \"[AUTOCUT] OS Distribution Build Failed for ${component}-${currentVersion}\" --body \"${message}\" --label ${label} --repo ${url}",
                        returnStdout: true
                )
            }
        }
    } catch (Exception ex) {
        println(ex.getMessage())
    }
}
