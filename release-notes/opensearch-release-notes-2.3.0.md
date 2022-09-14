# OpenSearch and Dashboards 2.3.0 Release Notes

## Release Highlights
OpenSearch and OpenSearch Dashboards 2.3.0 unlocks new approaches to data replication, storage, and visualization with three experimental features. These features are disabled by default and can be enabled per the [release documentation](https://opensearch.org/docs/latest).
* Segment replication offers users a new data replication strategy. With segment replication, OpenSearch copies Lucene file segments from the primary shard to its replicas, offering performance improvements for high-ingestion workloads.
* Remote-backed storage lets users deploy cloud storage for increased data durability. Users can back up and restore data from their clusters on a per-index basis using cloud-based storage solutions.
* A new drag-and-drop visualization tool lets users generate different types of visualizations more quickly and intuitively. Users can drag and drop data fields to generate line, bar, area, and metric charts.

## Release Details

OpenSearch and OpenSearch Dashboards 2.3.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.3.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.3.0.md).

## FEATURES

### OpenSearch SQL
* Add maketime and makedate datetime functions ([#755](https://github.com/opensearch-project/sql/pull/755))


## ENHANCEMENTS

### OpenSearch Cross Cluster Replication
* Add lastExecutionTime for autofollow coroutine ([#508](https://github.com/opensearch-project/cross-cluster-replication/pull/508))
* Modified security artifacts to fetch from latest build version ([#474](https://github.com/opensearch-project/cross-cluster-replication/pull/474))
* add updateVersion task ([#489](https://github.com/opensearch-project/cross-cluster-replication/pull/489))
* Bumped snakeyaml version to address CVE-2022-25857 ([#540](https://github.com/opensearch-project/cross-cluster-replication/pull/540))

### OpenSearch Dashboards Maps
* Adds integration tests in the repo for customImportMap plugin ([#30](https://github.com/opensearch-project/dashboards-maps/pull/30))


### OpenSearch Index Management
* Replica Count Validation when awareness replica balance is enabled ([#429](https://github.com/opensearch-project/index-management/pull/429))
* Updated detekt plugin, snakeyaml dependency and code to reduce the number of issues after static analysis ([#483](https://github.com/opensearch-project/index-management/pull/483))
* Transform max_clauses optimization: limit amount of modified buckets being processed at a time and added capping of pageSize to avoid maxClause exception ([#477](https://github.com/opensearch-project/index-management/pull/477))
* Remove HOST_DENY_LIST usage as Notification plugin will own it ([#488](https://github.com/opensearch-project/index-management/pull/488))
* Deprecate Master nonmenclature ([#502](https://github.com/opensearch-project/index-management/pull/502))


### OpenSearch Index Management Dashboards Plugin
* Change alignment of Snapshot Management panels in pages/Main/Main.tsx ([#236](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/236))


### OpenSearch k-NN
* Change initial size of DocIdSetBuilder ([#502](https://github.com/opensearch-project/k-NN/pull/502))


### OpenSearch Notifications
* Change the SendTestMessage API to be a POST call ([#506](https://github.com/opensearch-project/notifications/pull/506))


### OpenSearch Security
* Point in time API security changes ([#2033](https://github.com/opensearch-project/security/pull/2033))


### OpenSearch SQL
* Refactor implementation of relevance queries ([#746](https://github.com/opensearch-project/sql/pull/746))
* Extend query size limit using scroll ([#716](https://github.com/opensearch-project/sql/pull/716))
* Add any case of arguments in relevancy based functions to be allowed ([#744](https://github.com/opensearch-project/sql/pull/744))


## BUG FIXES

### OpenSearch Cross Cluster Replication
* Updating filters as well during Alias update ([#491](https://github.com/opensearch-project/cross-cluster-replication/pull/491))
* Modified _stop replication API to remove any stale replication settings on existing index ([#410](https://github.com/opensearch-project/cross-cluster-replication/pull/410))
* Fix for missing ShardReplicationTasks on new nodes ([#497](https://github.com/opensearch-project/cross-cluster-replication/pull/497))
* For segrep enabled indices, use NRTReplicationEngine for replica shards ([#486](https://github.com/opensearch-project/cross-cluster-replication/pull/486))

### OpenSearch Index Management
* Failed concurrent creates of ISM policies should return http 409 ([#464](https://github.com/opensearch-project/index-management/pull/464))
* Disable detekt to avoid the CVE issues ([#500](https://github.com/opensearch-project/index-management/pull/500))


### OpenSearch Index Management Dashboards Plugin
* Remove extra forward slash for URL to snapshot management docs ([#231](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/231))


### OpenSearch k-NN
* Remove overallocation in faiss query path ([#501](https://github.com/opensearch-project/k-NN/pull/501))


### OpenSearch Security
* Triple audit logging fix ([#1996](https://github.com/opensearch-project/security/pull/1996))
* Add allowlist.yml to 3 places in securityadmin tool ([#2046](https://github.com/opensearch-project/security/pull/2046))
* Fix legacy check in SecurityAdmin ([#2052](https://github.com/opensearch-project/security/pull/2052))


### OpenSearch Security Dashboards Plugin
* Use expiration of tokens from the id token ([#1040](https://github.com/opensearch-project/security-dashboards-plugin/pull/1040))


### OpenSearch SQL
* Fix unit test in PowerBI connector  ([#800](https://github.com/opensearch-project/sql/pull/800))


## INFRASTRUCTURE

### OpenSearch Alerting
* Deprecate the Master nomenclature. ([#548](https://github.com/opensearch-project/alerting/pull/548))


### OpenSearch Index Management
* Staging for version increment automation ([#409](https://github.com/opensearch-project/index-management/pull/409))


### OpenSearch Notifications
* Disable detekt to fix snakeyaml vulnerability ([#528](https://github.com/opensearch-project/notifications/pull/528))


### OpenSearch Security Dashboards Plugin
* Add prerequisite check github workflow ([#1083](https://github.com/opensearch-project/security-dashboards-plugin/pull/1083))


### OpenSearch SQL
* Schedule request in worker thread ([#748](https://github.com/opensearch-project/sql/pull/748))
* Deprecated ClusterService and Using NodeClient to fetch metadata ([#774](https://github.com/opensearch-project/sql/pull/774))
* Change master node timeout to new API ([#793](https://github.com/opensearch-project/sql/pull/793))


## DOCUMENTATION

### OpenSearch Anomaly Detection
* Adding external property customDistributionUrl to let developer override default distribution Download url ([#380](https://github.com/opensearch-project/anomaly-detection/pull/380))
* Replace Forum link in Anomaly Detection plugin README.md ([#659](https://github.com/opensearch-project/anomaly-detection/pull/659))


### OpenSearch Alerting
* Added 2.3 release notes. ([#551](https://github.com/opensearch-project/alerting/pull/551))

### OpenSearch Index Management
* Added 2.3 release note ([#507](https://github.com/opensearch-project/index-management/pull/507))


### OpenSearch Index Management Dashboards Plugin
* Added release notes for 2.3 ([#250](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/250))


### OpenSearch Ml Commons
* Algorithm links added to javadoc ([#400](https://github.com/opensearch-project/ml-commons/pull/400))


### OpenSearch SQL
* Adding documentation about double quote implementation ([#723](https://github.com/opensearch-project/sql/pull/723))
* Add PPL security setting documentation ([#777](https://github.com/opensearch-project/sql/pull/777))
* Update PPL docs link for workbench ([#758](https://github.com/opensearch-project/sql/pull/758))


## MAINTENANCE

### OpenSearch Anomaly Detection
* Removed additional non-inclusive terms ([#644](https://github.com/opensearch-project/anomaly-detection/pull/644))
* Bump version to 2.3 ([#658](https://github.com/opensearch-project/anomaly-detection/pull/658))



### OpenSearch Alerting
* Bumped version to 2.3.0. ([#547](https://github.com/opensearch-project/alerting/pull/547))


### OpenSearch Anomaly Detection Dashboards
* Bump to 2.3 ([#317](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/317))


### OpenSearch Asynchronous Search
* Bump version to 2.3.0 ([#174](https://github.com/opensearch-project/asynchronous-search/pull/174))
* Replace terminology 'master' with 'cluster manager' ([#175](https://github.com/opensearch-project/asynchronous-search/pull/175))


### OpenSearch Dashboards Reports
* Bump version to 2.3.0 ([#454](https://github.com/opensearch-project/dashboards-reports/pull/454))


### OpenSearch Dashboards Visualizations
* Version bump to 2.3.0 ([#111](https://github.com/opensearch-project/dashboards-visualizations/pull/111))


### OpenSearch Index Management
* Version upgrade to 2.3.0 ([#484](https://github.com/opensearch-project/index-management/pull/484))


### OpenSearch Index Management Dashboards Plugin
* Version bump 2.3.0 ([#247](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/247))
* Bumped moment version to resolve dependabot alert ([#230](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/230))
* Refactored dependency used by test mock. Adjusted OSD version used by test workflows ([#229](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/229))


### OpenSearch Job Scheduler
* Removed version.yml ([#233](https://github.com/opensearch-project/job-scheduler/pull/233)) ([#235](https://github.com/opensearch-project/job-scheduler/pull/235))
* Update to Gradle 7.5 ([#208](https://github.com/opensearch-project/job-scheduler/pull/208)) ([#228](https://github.com/opensearch-project/job-scheduler/pull/228))
* Staging for version increment automation ([#204](https://github.com/opensearch-project/job-scheduler/pull/204)) ([#212](https://github.com/opensearch-project/job-scheduler/pull/212))


### OpenSearch k-NN
* Updated the BWC workflow to have 2.2.0 as the backward supported version in BWC tests ([#536](https://github.com/opensearch-project/k-NN/pull/536))
* [AUTO] Increment version to 2.3.0-SNAPSHOT ([#526](https://github.com/opensearch-project/k-NN/pull/526))


### OpenSearch Ml Commons
* Reenable KMEANS predict IT tests ([#401](https://github.com/opensearch-project/ml-commons/pull/401))
* Upgrade to lucene snapshot ([#405](https://github.com/opensearch-project/ml-commons/pull/405))
* Bump to version 2.3 ([#417](https://github.com/opensearch-project/ml-commons/pull/417))


### OpenSearch Notifications
* Bump to version 2.3.0 ([#513](https://github.com/opensearch-project/notifications/pull/513))
* Bump moment from 2.29.3 to 2.29.4 in dashboards-notifications ([#487](https://github.com/opensearch-project/notifications/pull/487))


### OpenSearch Observability
* Bump version to 2.3.0 ([#997](https://github.com/opensearch-project/observability/pull/997))


### OpenSearch Performance Analyzer
* Upgrade netty version to 4.1.79 ([#249](https://github.com/opensearch-project/performance-analyzer/pull/249))
* Jackson version bump ([#247](https://github.com/opensearch-project/performance-analyzer/pull/247))


### OpenSearch Security
* Increment version to 2.3.0.0 ([#2022](https://github.com/opensearch-project/security/pull/2022))
* Update Gradle to 7.5.1 ([#2027](https://github.com/opensearch-project/security/pull/2027))


### OpenSearch Security Dashboards Plugin
* Increment version to 2.3.0.0 ([#1068](https://github.com/opensearch-project/security-dashboards-plugin/pull/1068))


### OpenSearch Geospatial
* Increment version to 2.3.0-SNAPSHOT ([#137](https://github.com/opensearch-project/geospatial/pull/137))


## REFACTORING

### OpenSearch k-NN
* Replace terminology 'master' with 'cluster manager' ([#521](https://github.com/opensearch-project/k-NN/pull/521))
* Nomenclature changes from Whitelist to Allowlist ([#534](https://github.com/opensearch-project/k-NN/pull/534))


