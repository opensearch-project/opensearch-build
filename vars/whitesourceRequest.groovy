/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

void call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    withCredentials([
        string(credentialsId: 'whitesource-scan-bot-userkey', variable: 'wss_bot_userkey'),
        string(credentialsId: 'whitesource-scan-opensearch-opensearch-projectkey', variable: 'wss_os_os_projectkey')
    ]) {

        def payloadMap = readJSON file: "$WORKSPACE/jenkins/vulnerability-scan/whitesource-report-opensearch-opensearch.json"

        payloadMap['userKey'] = wss_bot_userkey
        payloadMap['projectToken'] = wss_os_os_projectkey
        requestList = ['getProjectVulnerabilityReport', 'getProjectInventoryReport']

        for (request in requestList) {
            payloadMap['requestType'] = request
            println("Sending request: " + payloadMap['requestType'])

            def response = sendHttpRequest(
                 payloadMap,
                 'https://saas.whitesourcesoftware.com/api/v1.3',
                 'POST'
            )
            
            //println(response.status)
            //println(response.content)
        }
    }
}


