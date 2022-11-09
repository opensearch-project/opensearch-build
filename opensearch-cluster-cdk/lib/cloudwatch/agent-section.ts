/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

/* eslint-disable max-len */
interface EditableCloudwatchAgentSection {
    // eslint-disable-next-line camelcase
    metrics_collection_interval: number;
    logfile: string;
    // eslint-disable-next-line camelcase
    omit_hostname: boolean;
    debug: boolean;
}

/**
 * Cloudwatch configuration - Agent Section
 *
 * See definition at https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html#CloudWatch-Agent-Configuration-File-Agentsection
 *
 * Example configuration:
 * ```
 * agent: {
 *   metrics_collection_interval: 60, // seconds between collections
 *   logfile: '/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log',
 *   omit_hostname: true,
 *   debug: true,
 * }
 * ```
 */
export type CloudwatchAgentSection = Readonly<EditableCloudwatchAgentSection>;
