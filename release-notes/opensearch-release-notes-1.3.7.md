# OpenSearch and OpenSearch Dashboards 1.3.7 Release Notes

## Release Highlights

This release introduces Windows x64 distributions for OpenSearch and OpenSearch Dashboards for the 1.3 line. Available in ZIP format, the distributions allow users to deploy OpenSearch 1.3.7 directly in their Windows environment.

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.7 includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.7.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.7.md).

## ENHANCEMENTS

### OpenSearch k-NN
* Add windows support ([#583](https://github.com/opensearch-project/k-NN/pull/583))

## BUG FIXES

### OpenSearch SQL
* Bump jackson version to 2.14.1 ([#1125](https://github.com/opensearch-project/sql/pull/1125))
* Bump node library versions for 1.3 ([#1134](https://github.com/opensearch-project/sql/pull/1134))

### OpenSearch Dashboards Reporting
* Upgraded loader-utils, async, cross-fetch, terser, node-fetch, minimatch, moment, jsdom, qs, execa to resolve CVE ([#555](https://github.com/opensearch-project/dashboards-reports/pull/555))
* Upgraded detekt, snakyaml, and ktlint to resolve CVE ([#557](https://github.com/opensearch-project/dashboards-reports/pull/557))
* Upgraded decode-uri-component to resolve CVE-2022-38900 ([#559](https://github.com/opensearch-project/dashboards-reports/pull/559))

### OpenSearch Cross Cluster Replication
* Include default index settings during leader setting validation ([#609](https://github.com/opensearch-project/cross-cluster-replication/pull/609))
* Changed version of jackson databind to 2.13.4.2 for OS 1.3([#608](https://github.com/opensearch-project/cross-cluster-replication/pull/608))


### OpenSearch Dashboards Visualizations
* Bump node library versions ([#133](https://github.com/opensearch-project/dashboards-visualizations/pull/133))
* Force ansi-regex to ^5.0.1 ([#135](https://github.com/opensearch-project/dashboards-visualizations/pull/135))

## INFRASTRUCTURE

### OpenSearch k-NN
* Add Windows Build.sh Related Changes ([#602](https://github.com/opensearch-project/k-NN/pull/602))
* Apply Spotless ([#640](https://github.com/opensearch-project/k-NN/pull/640))
* Increment version to 1.3.7 ([#641](https://github.com/opensearch-project/k-NN/pull/641))
* Get rid of Rachet to fix failing build ([#648](https://github.com/opensearch-project/k-NN/pull/648))
* Exclude jacocoTestReport in distribution build script ([#652](https://github.com/opensearch-project/k-NN/pull/652))
* Update build script to build JNI lib and gradlew assemble ([#659](https://github.com/opensearch-project/k-NN/pull/659))

### OpenSearch ML Commons
* Windows ci build ([#595](https://github.com/opensearch-project/ml-commons/pull/595))

### OpenSearch Dashboards Reporting
* Enable windows build ([#562](https://github.com/opensearch-project/dashboards-reports/pull/562))

### OpenSearch Cross Cluster Replication
* Update the CI workflow to run the integ tests on all platforms ([#649](https://github.com/opensearch-project/cross-cluster-replication/pull/649))

### OpenSearch Dashboards Visualizations
* Add support for windows ([#139](https://github.com/opensearch-project/dashboards-visualizations/pull/139))

## MAINTENANCE

### OpenSearch ML Commons
* Increment version to 1.3.7-SNAPSHOT ([#461](https://github.com/opensearch-project/ml-commons/pull/461))
* Backport: Address CVE-2022-42889 by updating commons-text ([#520](https://github.com/opensearch-project/ml-commons/pull/520))
* Force protobuf-java version as 3.21.9 ([#587](https://github.com/opensearch-project/ml-commons/pull/587))
* Fix junit version ([#596](https://github.com/opensearch-project/ml-commons/pull/596))

### OpenSearch Dashboards Reporting
* Bump version to 1.3.7 ([#502](https://github.com/opensearch-project/dashboards-reporting/pull/502))

### OpenSearch Dashboards Visualizations
* Version bump to 1.3.7 ([#131](https://github.com/opensearch-project/dashboards-visualizations/pull/131))

