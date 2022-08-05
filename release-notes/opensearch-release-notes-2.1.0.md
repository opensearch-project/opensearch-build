# OpenSearch and Dashboards 2.1.0 Release Notes

## Release Highlights


* OpenSearch 2.1.0 supports version spoofing against 2.0.0 where it was [removed](https://github.com/opensearch-project/opensearch/pull/3530).
* You can now configure nodes with [dynamic nodes roles](https://github.com/opensearch-project/OpenSearch/pull/3436), which allows for custom node roles that won't affect node start processes.
* The [ML node role](https://github.com/opensearch-project/ml-commons/pull/346) can be configured for ML functions and tasks.
* SQL and PPL queries now supports [relevance-based search](https://github.com/opensearch-project/sql/issues/182), including [match_function](https://github.com/opensearch-project/sql/pull/204), [match_phrase](https://github.com/opensearch-project/sql/pull/604), and [match_bool_prefix](https://github.com/opensearch-project/sql/pull/634).
* OpenSearch now supports [multi-term aggregation](https://github.com/opensearch-project/OpenSearch/pull/2687).

## Release Details

OpenSearch and OpenSearch Dashboards 2.1.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.1.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.1.0.md).

## FEATURES

### Opensearch Index Management
* Merge snapshot management into main branch ([#390](https://github.com/opensearch-project/index-management/pull/390))
* Adds snapshot management notification implementation ([#387](https://github.com/opensearch-project/index-management/pull/387))
* Snapshot management default date format in snapshot name ([#392](https://github.com/opensearch-project/index-management/pull/392))


### Opensearch Index Management Dashboards Plugin
* Merge snapshot management into main branch ([#205](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/205))


### Opensearch Ml Common
* Dispatch ML task to ML node first ([#346](https://github.com/opensearch-project/ml-commons/pull/346))


### Opensearch Performance Analyzer
* Thread Metrics RCA ([#180](https://github.com/opensearch-project/performance-analyzer/pull/180))


### Opensearch SQL
* Support match_phrase filter function in SQL and PPL ([#604](https://github.com/opensearch-project/sql/pull/604))
* Add implementation for `simple_query_string` relevance search function in SQL and PPL ([#635](https://github.com/opensearch-project/sql/pull/635))
* Add multi_match to SQL plugin ([#649](https://github.com/opensearch-project/sql/pull/649))
* Integ match bool prefix #187 ([#634](https://github.com/opensearch-project/sql/pull/634))
* PPL describe command ([#646](https://github.com/opensearch-project/sql/pull/646))


## ENHANCEMENT

### Opensearch Index Management Dashboards Plugin
* Snapshot management small fixes ([#208](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/208))
* Tune the column width, fix the problem of showing snapshot failures ([#210](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/210))


### Opensearch Security Dashboards Plugin
* Dynamically compute OpenID redirectUri from proxy HTTP headers ([#929](https://github.com/opensearch-project/security-dashboards-plugin/pull/929))
* Clear the sessionStorage when logging out ([#1003](https://github.com/opensearch-project/security-dashboards-plugin/pull/1003))
S

## BUG FIX

### Opensearch Security
* Cluster permissions evaluation logic will now include `index_template` type action ([#1885](https://github.com/opensearch-project/security/pull/1885))
* Add missing settings to plugin allowed list ([#1814](https://github.com/opensearch-project/security/pull/1814))
* Updates license headers ([#1829](https://github.com/opensearch-project/security/pull/1829))
* Prevent recursive action groups ([#1868](https://github.com/opensearch-project/security/pull/1868))
* Update `org.springframework:spring-core` to `5.3.20` ([#1850](https://github.com/opensearch-project/security/pull/1850))


### Opensearch Security Dashboards Plugin
* Disable private tenant for read only users ([#868](https://github.com/opensearch-project/security-dashboards-plugin/pull/868))
* Replace _opendistro route with _plugins ([#895](https://github.com/opensearch-project/security-dashboards-plugin/pull/895))
ES

### Opensearch SQL
* Integ replace junit assertthat with hamcrest import ([#616](https://github.com/opensearch-project/sql/pull/616))
* Integ relevance function it fix ([#608](https://github.com/opensearch-project/sql/pull/608))
* Fix merge conflict on function name ([#664](https://github.com/opensearch-project/sql/pull/664))
* Fix `fuzziness` parsing in `multi_match` function. Update tests. ([#668](https://github.com/opensearch-project/sql/pull/668))
* ODBC SSL Compliance Fix ([#653](https://github.com/opensearch-project/sql/pull/653))


## INFRASTRUCTURE

### Opensearch Anomaly Detection
* Cluster manager revert fix ([#584](https://github.com/opensearch-project/anomaly-detection/pull/584))
* Adding HCAD data ingestion script to AD ([#585](https://github.com/opensearch-project/anomaly-detection/pull/585))
* Update ingestion ([#592](https://github.com/opensearch-project/anomaly-detection/pull/592))
* Adding custom plugin to publish zip to maven ([#594](https://github.com/opensearch-project/anomaly-detection/pull/594))


### Opensearch Anomaly Detection Dashboards
* Added UT for validation API related components ([#252](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/252))
* Run UT/IT on all branches ([#228](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/228))


### Opensearch Index Management
* Uses custom plugin to publish zips to maven ([#366](https://github.com/opensearch-project/index-management/pull/366))


### Opensearch k-NN
 
* Update opensearch version in BWCWorkflow ([#402](https://github.com/opensearch-project/k-NN/pull/402))
* Adding workflow for creating documentation issues ([#403](https://github.com/opensearch-project/k-NN/pull/403))
* Add Querying Functionality to OSB ([#409](https://github.com/opensearch-project/k-NN/pull/409))
* Add OpenSearch Benchmark index workload for k-NN ([#364](https://github.com/opensearch-project/k-NN/pull/364))
* Set tests.security.manager flag to false in integTestRemote task
([#410](https://github.com/opensearch-project/k-NN/pull/410))


### Opensearch Ml Common
* Bump RCF version to 3.0-rc3 ([#340](https://github.com/opensearch-project/ml-commons/pull/340))


### Opensearch Observability
* Uses custom plugin to publish zips to maven ([#786](https://github.com/opensearch-project/observability/pull/786))


### Opensearch SQL
* Match Query Unit Tests ([#614](https://github.com/opensearch-project/sql/pull/614))
* Uses custom plugin to publish zips to maven  ([#638](https://github.com/opensearch-project/sql/pull/638))


## DOCUMENTATION

### Opensearch Alerting
* Added 2.1 release notes. ([#485](https://github.com/opensearch-project/alerting/pull/485))


### Opensearch Alerting Dashboards Plugin
* Added 2.1 release notes. ([#284](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/284))


### Opensearch Common Utils
* Added 2.1 release notes. ([#194](https://github.com/opensearch-project/common-utils/pull/194))


### Opensearch Index Management
* Updated issue templates from .github. ([#324](https://github.com/opensearch-project/index-management/pull/324))


### Opensearch Index Management Dashboards Plugin
* Adding workflow for creating documentation issues. ([#197](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/197))


### OpenSearch Job Scheduler
* Added 2.1 release notes. ([#198](https://github.com/opensearch-project/job-scheduler/pull/198))


## MAINTENANCE

### Opensearch Anomaly Detection
* 2.1 version bump and Gradle bump ([#582](https://github.com/opensearch-project/anomaly-detection/pull/582))


### Opensearch Anomaly Detection Dashboards
* Bump to 2.1.0 compatibility ([#282](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/282))

### Opensearch Alerting
* Bumped version to 2.1.0, and gradle to 7.4.2. ([#475](https://github.com/opensearch-project/alerting/pull/475]))


### Opensearch Alerting Dashboards Plugin
* Bumped version from 2.0.1 to 2.1.0. ([#277](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/277))
* Bumped OpenSearch-Dashboards branch used by by the unit-tests-workflow. ([#278](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/278))


### Opensearch Common Utils
* Upgrade gradle to 7.4.2. ([#191](https://github.com/opensearch-project/common-utils/pull/191))
* Bump up the version to 2.1. ([#190](https://github.com/opensearch-project/common-utils/pull/190))


### Opensearch Dashboards Visualizations
* Version bump to 2.1.0 ([#89](https://github.com/opensearch-project/dashboards-visualizations/pull/89))


### Opensearch Index Management
* Version upgrade to 2.1.0 ([#389](https://github.com/opensearch-project/index-management/pull/389))


### Opensearch k-NN
* Bumping main version to opensearch core 2.1.0 ([#411](https://github.com/opensearch-project/k-NN/pull/411))


### Opensearch Index Management Dashboards Plugin
* Version bump 2.1.0 ([#206](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/206))


### OpenSearch Job Scheduler
* Bump up the OS version to 2.1. ([#195](https://github.com/opensearch-project/job-scheduler/pull/195))


### Opensearch Notifications
* Upgrade Notifications and Notifications Dashboards to 2.1 ([#468](https://github.com/opensearch-project/notifications/pull/468))
* Fix Email test for security integration test ([#462](https://github.com/opensearch-project/notifications/pull/462))


### Opensearch Observability
* Bump version to 2.1.0 and gradle version to 7.4.2 ([#817](https://github.com/opensearch-project/observability/pull/817))


### Opensearch Performance Analyzer
* Update 2.1 release version ([#192](https://github.com/opensearch-project/performance-analyzer-rca/pull/192))
* Update 2.1 release version ([#232](https://github.com/opensearch-project/performance-analyzer/pull/232))


### Opensearch Security
* Revert "Bump version to 2.1.0.0 (#1865)" ([#1882](https://github.com/opensearch-project/security/pull/1882))
* Bump version to 2.1.0.0 ([#1865](https://github.com/opensearch-project/security/pull/1865))
* Revert "Bump version to 2.1.0.0 (#1855)" ([#1864](https://github.com/opensearch-project/security/pull/1864))
* Bump version to 2.1.0.0 ([#1855](https://github.com/opensearch-project/security/pull/1855))
* Add suppression for all removal warnings ([#1828](https://github.com/opensearch-project/security/pull/1828))
* Update support link ([#1851](https://github.com/opensearch-project/security/pull/1851))
* Create 2.0.0 release notes ([#1854](https://github.com/opensearch-project/security/pull/1854))
* Switch to standard OpenSearch gradle build ([#1888](https://github.com/opensearch-project/security/pull/1888))
* Fix build break from cluster manager changes ([#1911](https://github.com/opensearch-project/security/pull/1911))
* Update org.apache.zookeeper:zookeeper to 3.7.1 ([#1912](https://github.com/opensearch-project/security/pull/1912))


### Opensearch Security Dashboards Plugin
* Bump version to 2.1.0.0 ([#1004](https://github.com/opensearch-project/security-dashboards-plugin/pull/1004))
* Adds 1.3.1.0 release notes ([#988](https://github.com/opensearch-project/security-dashboards-plugin/pull/988))
* Create release notes 2.0.0 ([#996](https://github.com/opensearch-project/security-dashboards-plugin/pull/996))


### Opensearch SQL
* Change plugin folder name to opensearch-sql-plugin ([#670](https://github.com/opensearch-project/sql/pull/670))
* Version bump to 2.1.0 and gradle version bump ([#655](https://github.com/opensearch-project/sql/pull/655))


## REFACTORING

### Opensearch k-NN
* Adding support for Lombok ([#393](https://github.com/opensearch-project/k-NN/pull/393))


### Opensearch Observability
* Make common delete modal for components ([#766](https://github.com/opensearch-project/observability/pull/766))
* Sync app and app list types ([#763](https://github.com/opensearch-project/observability/pull/763))


### Opensearch Security
* Remove master keywords ([#1886](https://github.com/opensearch-project/security/pull/1886))


