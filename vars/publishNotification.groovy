void call(Map args = [:]) {
    text = ([
        "${args.icon} ${JOB_NAME} [${BUILD_NUMBER}] ${args.message}",
        "Build: ${BUILD_URL}",
        args.manifest,
        args.extra
    ] - null).join("\n")

    withCredentials([string(credentialsId: args.credentialsId, variable: 'WEBHOOK_URL')]) {
        sh ([
            'curl',
            '-XPOST',
            '--header "Content-Type: application/json"',
            "--data '{\"result_text\":\"${text}\"}'",
            "\"${WEBHOOK_URL}\""
        ].join(' '))
    }
}
