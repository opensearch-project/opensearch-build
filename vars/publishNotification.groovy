void call(Map args = [:]) {
    def manifest = (args.credentialsId == 'BUILD_NOTICE_WEBHOOK') ? "Manifest: ${INPUT_MANIFEST}" : null
    text = ([
        "${args.icon} ${JOB_NAME} [${BUILD_NUMBER}] ${args.message}",
        "Build: ${BUILD_URL}",
        manifest,
        args.extra
    ] - null).join("\n")

    withCredentials([string(credentialsId: args.credentialsId, variable: 'WEBHOOK_URL')]) {
        sh ([
            args.dryRun ? 'echo curl' : 'curl',
            '-XPOST',
            '--header "Content-Type: application/json"',
            "--data '{\"result_text\":\"${text}\"}'",
            "\"${WEBHOOK_URL}\""
        ].join(' '))
    }
}
