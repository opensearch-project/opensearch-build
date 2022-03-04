def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))

    def componentsName = buildManifestObj.getNames()
    def componetsNumber = componentsName.size()
    def version = args.tagVersion
    echo "Creating $version release tag for $componetsNumber components in the manifest"

    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        for (component in componentsName) {
            def commitID = buildManifestObj.getCommitId(component)
            def repo = buildManifestObj.getRepo(component)
            def push_url = "https://$GITHUB_TOKEN@" + repo.minus('https://')
            echo "Tagging $component at $commitID ..."

            dir (component) {
                checkout([$class: 'GitSCM', branches: [[name: commitID]],
                          userRemoteConfigs: [[url: repo]]])
                if (component == "OpenSearch") {
                    def tag_id = sh (
                            script: "git ls-remote --tags $repo $version | awk 'NR==1{print \$1}'",
                            returnStdout: true
                    ).trim()
                    if (tag_id == "") {
                        echo "Creating $version tag for $component"
                        sh "git tag $version"
                        sh "git push $push_url $version"
                    } else if (tag_id == commitID) {
                        echo "Tag $version has been created with identical commit ID. Skipping creating new tag for $component."
                    } else {
                        error "Tag $version already existed in $component with a different commit ID. Please check this."
                    }
                } else {
                    def tag_id = sh (
                            script: "git ls-remote --tags $repo $version.0 | awk 'NR==1{print \$1}'",
                            returnStdout: true
                    ).trim()
                    echo "$tag_id"
                    if (tag_id == "") {
                        echo "Creating $version.0 tag for $component"
                        sh "git tag $version.0"
                        sh "git push $push_url $version.0"
                    } else if (tag_id == commitID) {
                        echo "Tag $version.0 has been created with identical commit ID. Skipping creating new tag for $component."
                    } else {
                        error "Tag $version.0 already existed in $component with a different commit ID. Please check this."
                    }
                }
            }
        }
    }
}
