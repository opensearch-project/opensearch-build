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

            sh """
                mkdir $component
                cd $component
                git init
                git remote add origin $repo
                git fetch --depth 1 origin $commitID
                git checkout FETCH_HEAD
                if [ "$component" == "OpenSearch" ]; then
                    if [[ -n \$(git ls-remote --tags $repo $version) ]]; then
                        tag_id=\$(git ls-remote --tags $repo $version | awk 'NR==1{print \$1}')
                        if [[ \${tag_id} != $commitID ]]; then
                            echo "Tag $version already existed with a different commit ID. Please check this." 
                            exit 1
                        else
                            echo "Tag $version has been created with identical commit ID. Skipping creating new tag for $component."
                        fi
                    else
                        git tag $version
                    fi
                else
                    if [[ -n \$(git ls-remote --tags $repo $version.0) ]]; then
                        tag_id=\$(git ls-remote --tags $repo $version.0 | awk 'NR==1{print \$1}')
                        if [[ \${tag_id} != $commitID ]]; then
                            echo "Tag $version.0 already existed with a different commit ID. Please check this." 
                            exit 1
                        else
                            echo "Tag $version.0 has been created with identical commit ID. Skipping creating new tag for $component."
                        fi
                    else
                        git tag $version.0
                    fi
                fi
                git push $push_url --tags
                cd ..
            """
        }
    }
}
