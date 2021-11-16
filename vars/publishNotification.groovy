void call(Map args = [:]) {
    text = ([
        "${args.icon} ${env.JOB_NAME} [${env.BUILD_NUMBER}] ${args.message}",
        "Build: ${env.BUILD_URL}",
        "Manifest: ${env.INPUT_MANIFEST}",
        args.extra
    ] - null).join("\n")

    withCredentials([string(credentialsId: 'BUILD_NOTICE_WEBHOOK', variable: 'TOKEN')]) {
        sh ([
            args.script ?: 'curl',
            '-XPOST',
            '--header "Content-Type: application/json"',
            "--data '{\"result_text\":\"${text}\"}'"
        ].join(' '))
    }
}