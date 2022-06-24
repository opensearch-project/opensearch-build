void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def git_repo_url = args.gitRepoUrl ?: 'null'
    def git_reference = args.gitReference ?: 'null'

    println("Git Repo: ${git_repo_url}")
    println("Git Reference: ${git_reference}")

    if (git_repo_url.equals('null') || git_reference.equals('null')) {
        println("No git repo url or git reference to checkout the commit, exit 1")
        System.exit(1)
    }
    else {
        withCredentials([
            usernamePassword(credentialsId: "jenkins-gradle-check-s3-aws-credentials", usernameVariable: 'amazon_s3_access_key', passwordVariable: 'amazon_s3_secret_key'),
            usernamePassword(credentialsId: "jenkins-gradle-check-s3-aws-resources", usernameVariable: 'amazon_s3_base_path', passwordVariable: 'amazon_s3_bucket')]) {

            sh """

                set -e
                set +x

                env | grep JAVA | grep HOME

                echo "Git clone: ${git_repo_url} with ref: ${git_reference}"
                rm -rf search
                git clone ${git_repo_url} search
                cd search/
                git checkout -f ${git_reference}
                git rev-parse HEAD

                echo "Stop existing gradledaemon"
                ./gradlew --stop
                find ~/.gradle -type f -name "*.lock" -delete

                echo "Check existing dockercontainer"
                docker ps -a
                docker stop `docker ps -qa` > /dev/null 2>&1 || echo
                docker rm `docker ps -qa` > /dev/null 2>&1 || echo
                echo "Stop existing dockercontainer"
                docker ps -a

                echo "Check docker-compose version"
                docker-compose version

                echo "Start gradlecheck"
                GRADLE_CHECK_STATUS=0
                ./gradlew check -Dtests.coverage=true --no-daemon --no-scan || GRADLE_CHECK_STATUS=1

                if [ "\$GRADLE_CHECK_STATUS" != 0 ]; then
                    echo Gradle Check Failed!
                    exit 1
                fi

            """
        }

    }


}
