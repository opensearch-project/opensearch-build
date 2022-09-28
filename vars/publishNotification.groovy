/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    text = ([
        "${args.icon}",
        "JOB_NAME=${JOB_NAME}",
        "BUILD_NUMBER=[${BUILD_NUMBER}]",
        "MESSAGE=${args.message}",
        "BUILD_URL: ${BUILD_URL}",
        "MANIFEST: ${args.manifest}",
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
