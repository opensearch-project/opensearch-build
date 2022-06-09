# OpenSearch and OpenSearch Dashboards 1.3.3 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.3 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.3.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.3.md).

## Enhancements

### Opensearch Anomaly Detection
* Use current time as training data end time  ([#547](https://github.com/opensearch-project/anomaly-detection/pull/547))
* Support writing features using filter aggregation ([#425](https://github.com/opensearch-project/anomaly-detection/pull/425))

### Opensearch Ml Commons
* Add circuit breaker trigger count stat ([#274](https://github.com/opensearch-project/ml-commons/pull/274))

## Bug Fixes

### Opensearch Anomaly Detection Dashboards
* Wait for detector to load before checking indices exist ([#262](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/262))
### Opensearch Observability
* App Analytics bug fixes ([#782](https://github.com/opensearch-project/observability/pull/782))

### Opensearch k-NN
* Change VectorReaderListener to expect number array ([#420](https://github.com/opensearch-project/k-NN/pull/420))

## Maintenance

### Opensearch Ml Commons
* Bump tribuo version to 4.2.1 ([#317](https://github.com/opensearch-project/ml-commons/pull/317))
* Remove local RCF jar, move to maven dependency ([#319](https://github.com/opensearch-project/ml-commons/pull/319))
* Version Increment to 1.3.3 OpenSearch release ([#331](https://github.com/opensearch-project/ml-commons/pull/331))

## Refactoring

### Opensearch Ml Commons
* Refactor stats API ([#334](https://github.com/opensearch-project/ml-commons/pull/334))



