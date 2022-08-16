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
                #!/bin/bash

                set -e
                set +x

                echo "Git clone: ${git_repo_url} with ref: ${git_reference}"
                rm -rf search
                git clone ${git_repo_url} search
                cd search/
                git checkout -f ${git_reference}
                git rev-parse HEAD

                echo "Get Major Version"
                OS_VERSION=`cat buildSrc/version.properties | grep opensearch | cut -d= -f2 | grep -oE '[0-9.]+'`
                JDK_MAJOR_VERSION=`cat buildSrc/version.properties | grep "bundled_jdk" | cut -d= -f2 | grep -oE '[0-9]+'  | head -n 1`
                OS_MAJOR_VERSION=`echo \$OS_VERSION | grep -oE '[0-9]+' | head -n 1`
                echo "Version: \$OS_VERSION, Major Version: \$OS_MAJOR_VERSION"

                echo "Using JAVA \$JDK_MAJOR_VERSION"
                eval export JAVA_HOME='\$JAVA'\$JDK_MAJOR_VERSION'_HOME'

                env | grep JAVA | grep HOME

                echo "Gradle clean cache and stop existing gradledaemon"
                ./gradlew --stop
                rm -rf ~/.gradle

                echo "Check existing dockercontainer"
                docker ps -a
                docker stop `docker ps -qa` > /dev/null 2>&1 || echo
                docker rm `docker ps -qa` > /dev/null 2>&1 || echo
                echo "Stop existing dockercontainer"
                docker ps -a

                echo "Check docker-compose version"
                docker-compose version

                echo "Check existing processes"
                ps -ef | grep [o]pensearch | wc -l
                echo "Cleanup existing processes"
                kill -9 `ps -ef | grep [o]pensearch | awk '{print \$2}'` > /dev/null 2>&1 || echo
                ps -ef | grep [o]pensearch | wc -l

                echo "Start gradlecheck"
                GRADLE_CHECK_STATUS=0
                ./gradlew clean && ./gradlew check -Dtests.coverage=true --no-daemon --no-scan || GRADLE_CHECK_STATUS=1

                if [ "\$GRADLE_CHECK_STATUS" != 0 ]; then
                    echo Gradle Check Failed!
                    exit 1
                fi

            """
        }

    }


}
