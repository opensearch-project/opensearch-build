/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

String mapToJson(Map req_body_map) {

    return groovy.json.JsonOutput.toJson(req_body_map)

}

Map call(Map req_body, String req_url, String http_mode = 'GET', String req_type = 'APPLICATION_JSON', String req_codes_valid = '200', Boolean console_log_resp = false) {

    response = httpRequest consoleLogResponseBody: console_log_resp, contentType: req_type, httpMode: http_mode, requestBody: mapToJson(req_body), url: req_url, validResponseCodes: req_codes_valid

    return response
}


