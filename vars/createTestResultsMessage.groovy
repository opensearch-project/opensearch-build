/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
def call(Map args = [:]) {
    String testType = args.testType
    String status = args.status
    String absoluteUrl = args.absoluteUrl
    String icon = status == 'SUCCESS' ? ':white_check_mark:' : ':warning:'

    return "\n${testType}: ${icon} ${status} ${absoluteUrl}"
}
