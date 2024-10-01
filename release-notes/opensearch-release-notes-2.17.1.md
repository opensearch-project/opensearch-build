# OpenSearch and OpenSearch Dashboards 2.17.1 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.17.1](https://opensearch.org/versions/opensearch-2-17-1.html) includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.17/release-notes/opensearch.release-notes-2.17.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.17/release-notes/opensearch-dashboards.release-notes-2.17.1.md).


## BUG FIXES


### Opensearch Anomaly Detection


* Bump BWC Version to 2.18 and Fix Bugs ([#1311](https://github.com/opensearch-project/anomaly-detection/pull/1311))


### Opensearch ML Commons


* Add bedrock batch job post process function; enhance remote job status parsing (#2955)[https://github.com/opensearch-project/ml-commons/pull/2955]
* Fix ML task index mapping (#2949)[https://github.com/opensearch-project/ml-commons/pull/2949]
* Fix full\_response false and no output mapping exceptions (#2944)[https://github.com/opensearch-project/ml-commons/pull/2944]
* Fix get batch task bug (#2937)[https://github.com/opensearch-project/ml-commons/pull/2937]
* Fix field mapping, add more error handling and remove checking jobId filed in batch job response (#2933)[https://github.com/opensearch-project/ml-commons/pull/2933]


### Opensearch Security Analytics


* [Alerts in Correlations] Stash context for system index ([#1297](https://github.com/opensearch-project/security-analytics/pull/1297))
* Threat intel monitor bug fixes ([#1317](https://github.com/opensearch-project/security-analytics/pull/1317))


### Opensearch k-NN


* Adds concurrent segment search support for mode auto [#2111](https://github.com/opensearch-project/k-NN/pull/2111)
* Change min oversample to 1 [#2117](https://github.com/opensearch-project/k-NN/pull/2117)


## DOCUMENTATION


### Opensearch ML Commons


* Fix bedrock claude3 blueprint typo (#2962)[https://github.com/opensearch-project/ml-commons/pull/2962]


## MAINTENANCE


### Dashboards Assistant


* Format the json file to avoid autocut PRs ([#291](https://github.com/opensearch-project/dashboards-assistant/pull/291))


### Opensearch Alerting Dashboards Plugin


* Updated workflows to use latest action of upload-artifacts ([#1089](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1089))


### Opensearch Dashboards Reporting


* [CVE-2024-45801] Bump dompurify from 2.4.7 to 2.5.6 ([#446](https://github.com/opensearch-project/dashboards-reporting/pull/444))


### Opensearch Flow Framework


* Fix flaky integ test reprovisioning before template update ([#880](https://github.com/opensearch-project/flow-framework/pull/880))


### Opensearch Notifications


* Resovle host to all ips and check against the deny list (#[964](https://github.com/opensearch-project/notifications/pull/964))
* Upgrade upload-artifact to v3 and bump version to 2.17.1 (#[963](https://github.com/opensearch-project/notifications/pull/963))


### Opensearch Security Analytics


* Upgrade upload artifacts ([#1305](https://github.com/opensearch-project/security-analytics/pull/1305))


### Opensearch Security Dashboards Plugin


* Bump micromatch to 4.0.8 ([#2117](https://github.com/opensearch-project/security-dashboards-plugin/pull/2117))


