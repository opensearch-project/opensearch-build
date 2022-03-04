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
                def tag_version
                if (component == "OpenSearch") {
                    tag_version = version
                } else {
                    tag_version = "$version.0"
                }
                def tag_id = sh (
                        script: "git ls-remote --tags $repo $version | awk 'NR==1{print \$1}'",
                        returnStdout: true
                ).trim()
                if (tag_id == "") {
                    echo "Creating $tag_version tag for $component"
                    sh "git tag $tag_version"
                    sh "git push $push_url $tag_version"
                } else if (tag_id == commitID) {
                    echo "Tag $tag_version has been created with identical commit ID. Skipping creating new tag for $component."
                } else {
                    error "Tag $tag_version already existed in $component with a different commit ID. Please check this."
                }
            }
        }
    }
}
