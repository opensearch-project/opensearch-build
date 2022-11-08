/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

/* eslint-disable max-len */
interface FileCollectionDefinition {
    // eslint-disable-next-line camelcase
    file_path: string;
    // eslint-disable-next-line camelcase
    log_group_name: string;
    // eslint-disable-next-line camelcase
    auto_removal: boolean;
    // eslint-disable-next-line camelcase
    log_stream_name: string,
}

interface EditableLogsSection {
    // eslint-disable-next-line camelcase
    logs_collected: {
        files: {
            // eslint-disable-next-line camelcase
            collect_list: FileCollectionDefinition[]
        }
    };
    // eslint-disable-next-line camelcase
    force_flush_interval: number;
}

/**
 * Cloudwatch configuration - Logs Section
 *
 * See definition at https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html#CloudWatch-Agent-Configuration-File-Logssection
 *
 * Example configuration:
 * ```
 logs: {
    logs_collected: {
      files: {
        collect_list: [
          {
            file_path: '/var/log/jenkins/jenkins.log',
            log_group_name: 'JenkinsMainNode/jenkins',
            auto_removal: true,
            log_stream_name: 'jenkins.log',
            timestamp_format: '%Y-%m-%d %H:%M:%S.%f%z',
          },
        ],
      },
    },
    force_flush_interval: 15,
  }
 * ```
 */
export type CloudwatchLogsSection = Readonly<EditableLogsSection>;
