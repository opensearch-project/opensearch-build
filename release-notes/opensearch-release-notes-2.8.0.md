Release Notes 2.8.0


## BREAKING

## FEATURE


### Alerting
* Integrate security-analytics & alerting for correlation engine. ([#878](https://github.com/opensearch-project/alerting/pull/878))
* DocLevel Monitor - generate findings when 0 triggers. ([#856](https://github.com/opensearch-project/alerting/pull/856))
* DocLevelMonitor Error Alert - rework. ([#892](https://github.com/opensearch-project/alerting/pull/892))
* Update endtime for DocLevelMonitor Error State Alerts and move them to history index when monitor execution succeeds. ([#905](https://github.com/opensearch-project/alerting/pull/905))
* Log error messages and clean up monitor when indexing doc level queries or metadata creation fails. ([#900](https://github.com/opensearch-project/alerting/pull/900))
* Adds transport layer actions for CRUD workflows. ([#934](https://github.com/opensearch-project/alerting/pull/934))



### Common-Utils
* Integrate security-analytics & alerting for correlation engine. ([#412](https://github.com/opensearch-project/common-utils/pull/412))
* NoOpTrigger. ([#420](https://github.com/opensearch-project/common-utils/pull/420))



### Dashboards-Observability

- Add reporting on-demand menu items back in notebooks ([#500](https://github.com/opensearch-project/dashboards-observability/pull/500))
- Updating trace DSL request handler ([#496](https://github.com/opensearch-project/dashboards-observability/pull/496))



### Index-Management-Dashboards-Plugin
* Feature: Add refresh index operation to UI  ([#761](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/761))
* Feature: Add clear cache operation to UI  ([#728](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/728),[#773](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/773))
* Feature: Add flush index operation to UI  ([#713](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/713),[#718](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/718),[#751](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/751),[#753](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/753),[#779](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/779))
* Feature: Add notification settings page and runtime notification option for long running index operations  ([#731](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/731),[#732](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/732)),[#784](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/784))
* Feature: Composable templates enhancement  ([#730](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/730))
* Implemented alias action UX. ([#754](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/754))



### Index-Management
* Support notification integration with long running operations. ([#712](https://github.com/opensearch-project/index-management/pull/712), [#722](https://github.com/opensearch-project/index-management/pull/722))



### Security-Analytics-Dashboards-Plugin
* [Correlations] Added link to rule details; simplified rule parsing. ([#571](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/571))
* [FEATURE] Finding flyout loading state. ([#562](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/562))
* Add correlation rule details into the finding details flyout. ([#565](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/565))
* UX improvements for correlation engine. ([#561](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/561))
* Add a details button to open the findings flyout from the correlations page. ([#572](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/572))
* [Overview page] Fixed recent alerts & finding order; count for pie chart. ([#574](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/574))
* Detection rule new detection ux. ([#575](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/575))



### Security-Analytics
* Add correlation engine for security-analytics. ([#405](https://github.com/opensearch-project/security-analytics/pull/405))
* SearchRule API - source filtering. ([#374](https://github.com/opensearch-project/security-analytics/pull/374))
* Alias and dataStream end-to-end ITs. ([#373](https://github.com/opensearch-project/security-analytics/pull/373))
* Add rules to correlations for correlation engine. ([#423](https://github.com/opensearch-project/security-analytics/pull/423))



### Security

* Identify extension Transport requests and permit handshake and extension registration actions ([#2599](https://github.com/opensearch-project/security/pull/2599))
* Use ExtensionsManager.lookupExtensionSettingsById when verifying extension unique id ([#2749](https://github.com/opensearch-project/security/pull/2749))
* Generate auth tokens for service accounts ([#2716](https://github.com/opensearch-project/security/pull/2716))
* Security User Refactor ([#2594](https://github.com/opensearch-project/security/pull/2594))
* Add score based password verification ([#2557](https://github.com/opensearch-project/security/pull/2557))
* Usage of JWKS with JWT (w/o OpenID connect) ([#2808](https://github.com/opensearch-project/security/pull/2808))



### Sql

* Support for pagination in v2 engine of SELECT * FROM <table> queries ([#1666](https://github.com/opensearch-project/sql/pull/1666))
* Support Alternate Datetime Formats ([#1664](https://github.com/opensearch-project/sql/pull/1664))
* Create new anonymizer for new engine ([#1665](https://github.com/opensearch-project/sql/pull/1665))
* Add Support for Nested Function Use In WHERE Clause Predicate Expresion ([#1657](https://github.com/opensearch-project/sql/pull/1657))
* Cross cluster search in PPL ([#1512](https://github.com/opensearch-project/sql/pull/1512))
* Added COSH to V2 engine ([#1428](https://github.com/opensearch-project/sql/pull/1428))
* REST API for GET,PUT and DELETE ([#1482](https://github.com/opensearch-project/sql/pull/1482))



### Job-Scheduler
* Add auto-release github workflow ([#385](https://github.com/opensearch-project/job-scheduler/pull/385))


## ENHANCE


### Cross-Cluster-Replication
* Support CCR for k-NN enabled indices ([#760](https://github.com/opensearch-project/cross-cluster-replication/pull/760))



### K-NN

* Bulk allocate objects for nmslib index creation to avoid malloc fragmentation ([#773](https://github.com/opensearch-project/k-NN/pull/773))



### Ml-Commons

* Add a setting to enable/disable model url in register API ([#871](https://github.com/opensearch-project/ml-commons/pull/871))
* Add a setting to enable/disable local upload while registering model ([#873](https://github.com/opensearch-project/ml-commons/pull/873))
* Check hash value for the pretrained models ([#878](https://github.com/opensearch-project/ml-commons/pull/878))
* Add pre-trained model list ([#883](https://github.com/opensearch-project/ml-commons/pull/883))
* Add content hash value for the correlation model. ([#885](https://github.com/opensearch-project/ml-commons/pull/885))
* Set default access_control_enabled setting to false ([#935](https://github.com/opensearch-project/ml-commons/pull/935))
* Enable model access control in secure reset IT ([#940](https://github.com/opensearch-project/ml-commons/pull/940))
* Add model group rest ITs ([#942](https://github.com/opensearch-project/ml-commons/pull/942))



### Security-Dashboards-Plugin

* Add new cluster permissions constants for long-running operation notification feature in Index-Management repo ([#1444](https://github.com/opensearch-project/security-dashboards-plugin/pull/1444))
* Adds the newly created admin api permissions to the static dropdown list ([#1426](https://github.com/opensearch-project/security-dashboards-plugin/pull/1426))


### Security

* Add default roles for SQL plugin: PPL and cross-cluster search ([#2729](https://github.com/opensearch-project/security/pull/2729))
* Update security-analytics roles to add correlation engine apis ([#2732](https://github.com/opensearch-project/security/pull/2732))
* Changes in role.yml for long-running operation notification feature in Index-Management repo ([#2789](https://github.com/opensearch-project/security/pull/2789))
* Rest admin permissions ([#2411](https://github.com/opensearch-project/security/pull/2411))
* Separate config option to enable restapi: permissions ([#2605](https://github.com/opensearch-project/security/pull/2605))



### Sql

* Minor clean up of datetime and other classes ([#1310](https://github.com/opensearch-project/sql/pull/1310))
* Add integration JDBC tests for cursor/fetch_size feature ([#1315](https://github.com/opensearch-project/sql/pull/1315))
* Refactoring datasource changes to a new module. ([#1504](https://github.com/opensearch-project/sql/pull/1504))


## BUG FIX


### Alerting
* Fix getAlerts API for standard Alerting monitors. ([#870](https://github.com/opensearch-project/alerting/issues/870))
* Fixed a bug that prevented alerts from being generated for doc level monitors that use wildcard characters in index names. ([#894](https://github.com/opensearch-project/alerting/issues/894))
* Revert to deleting monitor metadata after deleting doc level queries to fix delete monitor regression. ([#931](https://github.com/opensearch-project/alerting/issues/931))



### Anomaly-Detection-Dashboards-Plugin

* Fixing test to pass with node 18 ([#491](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/491))



### Cross-Cluster-Replication
* Handle serialization issues with UpdateReplicationStateDetailsRequest ([#866](https://github.com/opensearch-project/cross-cluster-replication/pull/866))
* Two followers using same remote alias can result in replication being auto-paused ([#833](https://github.com/opensearch-project/cross-cluster-replication/pull/833))


### Dashboards-Observability

- Remove styling causing issue for banner in advanced settings ([#502](https://github.com/opensearch-project/dashboards-observability/pull/502))
- Add Metrics cypress and bug fixes ([#505](https://github.com/opensearch-project/dashboards-observability/pull/505))


### Dashboards-Query-Workbench
* Add fix for CVE-2023-2251 ([#62](https://github.com/opensearch-project/dashboards-query-workbench/pull/62))
* Use valid json for mock data in unit tests ([#76](https://github.com/opensearch-project/dashboards-query-workbench/pull/76))



### Dashboards-Reporting
* Add fix for CVE-2023-2251 ([#104](https://github.com/opensearch-project/dashboards-reporting/pull/104))



### Index-Management-Dashboards-Plugin
* Update path parameter to follow RFC/generic HTTP convention. ([#742](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/742))



### Index-Management
* Remove recursion call when checking permission on indices. ([#779](https://github.com/opensearch-project/index-management/pull/779))
* Added trimming of nanos part of "epoch_millis" timestamp when date_histogram type used is date_nanos. ([#772](https://github.com/opensearch-project/index-management/pull/772))
* Added proper resolving of sourceIndex inside RollupInterceptor, it's required for QueryStringQuery parsing. ([#773](https://github.com/opensearch-project/index-management/pull/773))



### Ml-Commons

* Fix class not found exception when deserialize model ([#899](https://github.com/opensearch-project/ml-commons/pull/899))
* Fix publish shadow publication dependency issue ([#919](https://github.com/opensearch-project/ml-commons/pull/919))
* Fix model group index not existing model version query issue and SecureMLRestIT failure ITs ([#933](https://github.com/opensearch-project/ml-commons/pull/933))
* Fix model access mode upper case bug ([#937](https://github.com/opensearch-project/ml-commons/pull/937))



### Notifications
* Modify the default values in the bindle file to make them consistent with the values in code ([#672](https://github.com/opensearch-project/notifications/pull/672))



### Observability
* Fix guava jar hell issue ([#1536](https://github.com/opensearch-project/observability/pull/1536))



### Performance-Analyzer
* Fix ShardStateCollector which was impacted by [core refactoring](https://github.com/opensearch-project/OpenSearch/pull/7301) [445](https://github.com/opensearch-project/performance-analyzer/pull/445)



### Reporting
* Update json version to 20230227 ([#692](https://github.com/opensearch-project/reporting/pull/692))
* Update Gradle Wrapper to 7.6.1 ([#695](https://github.com/opensearch-project/reporting/pull/695))
* Removing guava dependency to fix jarhell ([#709](https://github.com/opensearch-project/reporting/pull/709))



### Security-Analytics-Dashboards-Plugin
* Finding's fly-out has no correlations if open from alerts. ([#558](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/558))
* Wrong field mappings for the cloud trail logs. ([#574](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/574))



### Security-Analytics
* Findings index mappings fix. ([#409](https://github.com/opensearch-project/security-analytics/pull/409))
* Fix for input validation of correlation rule names. ([#428](https://github.com/opensearch-project/security-analytics/pull/428))
* Fix for failure in syslogs mappings view api. ([#435](https://github.com/opensearch-project/security-analytics/pull/435))



### Security-Dashboards-Plugin

* Fix the test cases to adapt the security password validation feature ([#1437](https://github.com/opensearch-project/security-dashboards-plugin/pull/1437))



### Security

* `DeserializeSafeFromHeader` uses `context.getHeader(headerName)` instead of `context.getHeaders()` ([#2768](https://github.com/opensearch-project/security/pull/2768))
* Fix multitency config update ([#2758](https://github.com/opensearch-project/security/pull/2758))



### Sql

* Fixing bug where Nested functions used in WHERE, GROUP BY, HAVING, and ORDER BY clauses don't fallback to legacy engine. ([#1549](https://github.com/opensearch-project/sql/pull/1549))


## INFRASTRUCTURE


### Anomaly-Detection
* Partial Cherry-pick of #886 from anomaly-detection and Additional Adjustments. ([#914](https://github.com/opensearch-project/anomaly-detection/pull/914))

### Common-Utils
* Switch publish maven branches to list. ([#423](https://github.com/opensearch-project/common-utils/pull/423))



### Geospatial
* Make jacoco report to be generated faster in local ([#267](https://github.com/opensearch-project/geospatial/pull/267))
* Exclude lombok generated code from jacoco coverage report ([#268](https://github.com/opensearch-project/geospatial/pull/268))



### K-NN

* Bump requests version from 2.26.0 to 2.31.0 ([#913](https://github.com/opensearch-project/k-NN/pull/913))
* Disable index refresh for system indices ([#773](https://github.com/opensearch-project/k-NN/pull/915))


### Ml-Commons-Dashboards

* Update husky to 8.0.3 to remove execa as development dependency. ([#160](https://github.com/opensearch-project/ml-commons-dashboards/pull/160))


### Neural-Search

* Bump gradle version to 8.1.1 ([#169](https://github.com/opensearch-project/neural-search/pull/169))


### Notifications
* Upgrade gradle version to 8.1.1 ([#663](https://github.com/opensearch-project/notifications/pull/663))
* Fix gradle run failed on windows platform and fix weak password test failure ([#684](https://github.com/opensearch-project/notifications/pull/684))



### Observability
* Update Gradle Wrapper to 7.6.1 ([#1512](https://github.com/opensearch-project/observability/pull/1512))



### Performance-Analyzer
* Upgrade gradle to 7.6.1, upgrade gradle test-retry plugin to 1.5.2. ([#438](https://github.com/opensearch-project/performance-analyzer/pull/438))
* Introduce protobuf and guava dependency from core versions file [#437](https://github.com/opensearch-project/performance-analyzer/pull/437)
* Update dependency org.xerial:sqlite-jdbc to v3.41.2.2 [#375](https://github.com/opensearch-project/performance-analyzer-rca/pull/375)


## DOCUMENT


### Alerting-Dashboards-Plugin
* Added 2.8.0 release notes. ([#561](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/561))

### Alerting
* Added 2.8 release notes. ([#939](https://github.com/opensearch-project/alerting/pull/939))

### Anomaly-Detection-Dashboards-Plugin

* Updating maintainers and code owners ([#476](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/476))

### Common-Utils
* Added 2.8 release notes. ([#441](https://github.com/opensearch-project/common-utils/pull/441))

### Dashboards-Notifications
* Drafted 2.8 release notes. ([#52](https://github.com/opensearch-project/dashboards-notifications/pull/52))

### Index-Management-Dashboards-Plugin
* 2.8 release note ([#765](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/765))


### Index-Management
* Added 2.8 release notes. ([#794](https://github.com/opensearch-project/index-management/pull/794))

### Ml-Commons




### Notifications
* Add 2.8.0 release notes ([#682](https://github.com/opensearch-project/notifications/pull/682))


### Security-Analytics-Dashboards-Plugin
* Added 2.8 release notes. ([#597](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/597))

### Security-Analytics
* Added 2.8.0 release notes. ([#444](https://github.com/opensearch-project/security-analytics/pull/444))

### Sql

* Add Nested Documentation for 2.7 Related Features ([#1620](https://github.com/opensearch-project/sql/pull/1620))
* Update usage example doc for PPL cross-cluster search ([#1610](https://github.com/opensearch-project/sql/pull/1610))
* Documentation and other papercuts for datasource api launch ([#1530](https://github.com/opensearch-project/sql/pull/1530))


## MAINT


### Alerting-Dashboards-Plugin
* Baseline codeowners and maintainers. ([#547](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/547))
* Updating the CODEOWNERS file to use the right format. ([#550](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/550))



### Alerting
* Baseline codeowners and maintainers. ([#818](https://github.com/opensearch-project/alerting/pull/818))
* Upgrade gradle to 8.1.1. ([#893](https://github.com/opensearch-project/alerting/pull/893))
* Update codeowners and maintainers. ([#899](https://github.com/opensearch-project/alerting/pull/899))
* Updating the CODEOWNERS file with the right format. ([#911](https://github.com/opensearch-project/alerting/pull/911))
* Compile fix - Strings package change. ([#924](https://github.com/opensearch-project/alerting/pull/924))



### Asynchronous-Search
* Updating maintainers file ([275](https://github.com/opensearch-project/asynchronous-search/pull/275))

### Common-Utils
* Upgrade gradle to 8.1.1. ([#418](https://github.com/opensearch-project/common-utils/pull/418))
* Sync up MAINTAINERS to CODEOWNERS. ([#427](https://github.com/opensearch-project/common-utils/pull/427))
* Fix build errors after refactoring of Strings class in core. ([#432](https://github.com/opensearch-project/common-utils/pull/432))
* Updating maintainers and codeowners. ([#438](https://github.com/opensearch-project/common-utils/pull/438))
* Fix codeowners file format. ([#440](https://github.com/opensearch-project/common-utils/pull/440))



### Dashboards-Maps
* Remove package-lock.json ([#400](https://github.com/opensearch-project/dashboards-maps/pull/400))


### Dashboards-Notifications
* Bumped version to 2.8. ([#40](https://github.com/opensearch-project/dashboards-notifications/pull/40))
* Fix CI on Node.js v18. ([#56](https://github.com/opensearch-project/dashboards-notifications/pull/56))



### Dashboards-Query-Workbench
* Increment version to 2.8.0.0 ([#67](https://github.com/opensearch-project/dashboards-query-workbench/pull/67))

### Dashboards-Reporting
* Increment version to 2.8.0.0 ([#108](https://github.com/opensearch-project/dashboards-reporting/pull/108))


### Dashboards-Visualizations
* Increment version to 2.8.0.0 ([#182](https://github.com/opensearch-project/dashboards-visualizations/pull/182))


### Geospatial
* Change package for Strings.hasText ([#314](https://github.com/opensearch-project/geospatial/pull/314))

### Index-Management-Dashboards-Plugin
* Bumped version to 2.8. ([#721](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/721))
* Fix CI on Node.js v18. ([#785](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/785))



### Index-Management
* Upgrade to gradle 8.1.1. ([#777](https://github.com/opensearch-project/index-management/pull/777))
* Bump version to 2.8. ([#759](https://github.com/opensearch-project/index-management/pull/759))



### Job-Scheduler
* Consuming breaking changes from moving ExtensionActionRequest ([#381](https://github.com/opensearch-project/job-scheduler/pull/381))
* Fix the Maven publish ([#379](https://github.com/opensearch-project/job-scheduler/pull/379))
* Fixes issue with publishing Job Scheduler artifacts to correct maven coordinates ([#377](https://github.com/opensearch-project/job-scheduler/pull/377))
* Bumping JS main BWC test version for sample extension plugin to 2.8 ([#371](https://github.com/opensearch-project/job-scheduler/pull/371))


### Ml-Commons

* Increment version to 2.8.0-SNAPSHOT ([#896](https://github.com/opensearch-project/ml-commons/pull/896))



### Notifications
* [AUTO] Increment version to 2.8.0-SNAPSHOT ([#657](https://github.com/opensearch-project/notifications/pull/657))



### Observability
* Increment version to 2.8.0-SNAPSHOT ([#1505](https://github.com/opensearch-project/observability/pull/1505))


### Performance-Analyzer
* Update RestController constructor for tests [#440](https://github.com/opensearch-project/performance-analyzer/pull/440)
* Dependencies change in favor of Commons repo [#448](https://github.com/opensearch-project/performance-analyzer/pull/448)
* WriterMetrics and config files dependency redirection [#450](https://github.com/opensearch-project/performance-analyzer/pull/450)
* Refactor code related to Commons change, fixing unit tests [#451](https://github.com/opensearch-project/performance-analyzer/pull/451)
* Remove remaining dependencies from PA-RCA due to commons repo [#453](https://github.com/opensearch-project/performance-analyzer/pull/453)
* Fix BWC Integration tests [#413](https://github.com/opensearch-project/performance-analyzer/pull/413)
* Fix SHA update for PA-Commons repo in build.gradle  [#454](https://github.com/opensearch-project/performance-analyzer/pull/454)
* Refactor Service/Stat Metrics [#376](https://github.com/opensearch-project/performance-analyzer-rca/pull/376)

### Reporting
* Increment version to 2.8.0-SNAPSHOT ([#688](https://github.com/opensearch-project/reporting/pull/688))


### Security-Analytics-Dashboards-Plugin
* Cypress | create detector specs update. ([#518](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/518))
* Rule's cypress tests update. ([#581](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/581))
* Moving the CODEOWNERS to the right location ([#583](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/583))



### Security-Analytics
* Fixed compile issues related to latest OS core repo changes. ([#412](https://github.com/opensearch-project/security-analytics/pull/412))
* Moved CODEOWNERS files to align with org requirements. ([#418](https://github.com/opensearch-project/security-analytics/pull/418))
* Update CODEOWNERS. ([#434](https://github.com/opensearch-project/security-analytics/pull/434))



### Security

* Update to Gradle 8.1.1 ([#2738](https://github.com/opensearch-project/security/pull/2738))
* Upgrade spring-core from 5.3.26 to 5.3.27 ([#2717](https://github.com/opensearch-project/security/pull/2717))


### Sql

* Fix IT - address breaking changes from upstream. ([#1659](https://github.com/opensearch-project/sql/pull/1659))
* Increment version to 2.8.0-SNAPSHOT ([#1552](https://github.com/opensearch-project/sql/pull/1552))
* Backport maintainer list update to `2.x`. ([#1650](https://github.com/opensearch-project/sql/pull/1650))
* Backport jackson and gradle update from #1580 to 2.x ([#1596](https://github.com/opensearch-project/sql/pull/1596))
* Adding reflections as a dependency ([#1559](https://github.com/opensearch-project/sql/pull/1596))
* Bump org.json dependency version ([#1586](https://github.com/opensearch-project/sql/pull/1586))
* Integ Test Fix ([#1541](https://github.com/opensearch-project/sql/pull/1541))
## REFACTOR


### Ml-Commons

* Change mem_size_estimation to memory_size_estimation ([#868](https://github.com/opensearch-project/ml-commons/pull/868))

