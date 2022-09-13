# OpenSearch and Dashboards 2.3.0 Release Notes

## Release Highlights

## Release Details

OpenSearch and OpenSearch Dashboards 2.3.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.3.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.3.0.md).

## BREAKING CHANGES

## FEATURES

### OpenSearch SQL
* Add maketime and makedate datetime functions ([#755](https://github.com/opensearch-project/sql/pull/755))


## ENHANCEMENTS

### OpenSearch Index Management
* Replica Count Validation when awareness replica balance is enabled ([#429](https://github.com/opensearch-project/index-management/pull/429))
* Updated detekt plugin, snakeyaml dependency and code to reduce the number of issues after static analysis ([#483](https://github.com/opensearch-project/index-management/pull/483))
* Transform max_clauses optimization: limit amount of modified buckets being processed at a time and added capping of pageSize to avoid maxClause exception ([#477](https://github.com/opensearch-project/index-management/pull/477))
* Remove HOST_DENY_LIST usage as Notification plugin will own it ([#488](https://github.com/opensearch-project/index-management/pull/488))
* Deprecate Master nonmenclature ([#502](https://github.com/opensearch-project/index-management/pull/502))


### OpenSearch k-NN
* Change initial size of DocIdSetBuilder (#502)


### OpenSearch Notifications
* Change the SendTestMessage API to be a POST call ([#506](https://github.com/opensearch-project/notifications/pull/506))


### OpenSearch Security
* Point in time API security changes ([#2033](https://github.com/opensearch-project/security/pull/2033))


### OpenSearch Security
* Point in time API security changes ([#2033](https://github.com/opensearch-project/security/pull/2033))


### OpenSearch SQL
* Refactor implementation of relevance queries ([#746](https://github.com/opensearch-project/sql/pull/746))
* Extend query size limit using scroll ([#716](https://github.com/opensearch-project/sql/pull/716))
* Add any case of arguments in relevancy based functions to be allowed ([#744](https://github.com/opensearch-project/sql/pull/744))


## BUG FIXES

### OpenSearch Index Management
* Failed concurrent creates of ISM policies should return http 409 ([#464](https://github.com/opensearch-project/index-management/pull/464))
* Disable detekt to avoid the CVE issues ([#500](https://github.com/opensearch-project/index-management/pull/500))


### OpenSearch Index Management Dashboards Plugin
* Remove extra forward slash for URL to snapshot management docs ([#231](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/231))


### OpenSearch k-NN
* Remove overallocation in faiss query path (#501)


### OpenSearch Security
* Triple audit logging fix ([#1996](https://github.com/opensearch-project/security/pull/1996))
* Add allowlist.yml to 3 places in securityadmin tool ([#2046](https://github.com/opensearch-project/security/pull/2046))
* Fix legacy check in SecurityAdmin ([#2052](https://github.com/opensearch-project/security/pull/2052))


### OpenSearch Security
* Triple audit logging fix ([#1996](https://github.com/opensearch-project/security/pull/1996))
* Add allowlist.yml to 3 places in securityadmin tool ([#2046](https://github.com/opensearch-project/security/pull/2046))
* Fix legacy check in SecurityAdmin ([#2052](https://github.com/opensearch-project/security/pull/2052))


### OpenSearch Security Dashboards Plugin
* Use expiration of tokens from the id token ([#1040](https://github.com/opensearch-project/security-dashboards-plugin/pull/1040))


### OpenSearch SQL
* Fix unit test in PowerBI connector  ([#800](https://github.com/opensearch-project/sql/pull/800))


## INFRASTRUCTURE

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

### OpenSearch Index Management
* Added 2.3 release note ([#507](https://github.com/opensearch-project/index-management/pull/507))


### OpenSearch Index Management Dashboards Plugin
* Added release notes for 2.3 ([#250](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/250))


### OpenSearch Ml Common
* Algorithm links added to javadoc ([#400](https://github.com/opensearch-project/ml-commons/pull/400))


### OpenSearch SQL
* Adding documentation about double quote implementation ([#723](https://github.com/opensearch-project/sql/pull/723))
* Add PPL security setting documentation ([#777](https://github.com/opensearch-project/sql/pull/777))
* Update PPL docs link for workbench ([#758](https://github.com/opensearch-project/sql/pull/758))


## MAINTENANCE

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


### OpenSearch Ml Common
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


### OpenSearch Security
* Increment version to 2.3.0.0 ([#2022](https://github.com/opensearch-project/security/pull/2022))
* Update Gradle to 7.5.1 ([#2027](https://github.com/opensearch-project/security/pull/2027))


### OpenSearch Security Dashboards Plugin
* Increment version to 2.3.0.0 ([#1068](https://github.com/opensearch-project/security-dashboards-plugin/pull/1068))


## REFACTORING

### OpenSearch k-NN
* Replace terminology 'master' with 'cluster manager' (#521)
* Nomenclature changes from Whitelist to Allowlist (#534)


