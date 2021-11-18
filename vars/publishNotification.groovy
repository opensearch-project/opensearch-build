void call(Map args = [:]) {
    text = ([
        "${args.icon} ${JOB_NAME} [${BUILD_NUMBER}] ${args.message}",
        "Build: ${BUILD_URL}",
        "Manifest: ${INPUT_MANIFEST}",
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