# OpenSearch and OpenSearch Dashboards 2.0.1 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.0.1 includes the following bug fixes, documentation, and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.0.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.0.1.md).

## Bug Fixes

### OpenSearch Alerting Dashboards Plugin
* Implemented a fix for issue 258 which was allowing the UX to define more than 1 index for document level monitors ([#259](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/259))
* Fixed a bug that was causing the action execution policy to be configurable for query and cluster metrics monitors ([#261](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/261))
* Fixed an issue preventing doc level monitors from adding execution policy as expected ([#262](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/262))
* Fixed an issue that would sometimes cause the loadDestinations function to not call getChannels ([#264](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/264))

### Opensearch Anomaly Detection
* Use current time as training data end time ([#547](https://github.com/opensearch-project/anomaly-detection/pull/547))
* Bump rcf to 3.0-rc3 ([#568](https://github.com/opensearch-project/anomaly-detection/pull/568))

## Maintenance

### OpenSearch Alerting Dashboards Plugin
* Incremented version to 2.0.1 ([#269](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/269))

## Documentation

### OpenSearch Alerting Dashboards Plugin
* Draft release notes for 2.0.1 patch ([#265](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/265))
