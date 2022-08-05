# OpenSearch and Dashboards 2.0.0 Release Notes

## Release Highlights

* Document level alerting allows users to create monitors that can generate alerts per document
* Lucene 9 is now used in OpenSearch
* The Geo Map Tiles in OpenSearch Dashboards are updated and now have a pipeline to update them more frequently
* Document level security now supports term lookup queries

### OpenSearch Notifications
* OpenSearch 2.0.0 is the first official release with OpenSearch Notifications
* Notifications consist of three plugins, `notifications-core` and `notifications` backend plugins for OpenSearch, and a `notificationsDashboards` frontend plugin for OpenSearch Dashboards


## Release Details

OpenSearch and OpenSearch Dashboards 2.0.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates:

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.0/release-notes/opensearch.release-notes-2.0.0.md)

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.0/release-notes/opensearch-dashboards.release-notes-2.0.0.md)

## FEATURES

### OpenSearch Alerting
* Integrate Document Level Alerting changes ([#410](https://github.com/opensearch-project/alerting/pull/410]))
* Alias support for Document Level Monitors ([#416](https://github.com/opensearch-project/alerting/pull/416]))


### OpenSearch Index Management
* Adds shrink action to ISM ([#326](https://github.com/opensearch-project/index-management/pull/326))
* Notification integration with IM ([#338](https://github.com/opensearch-project/index-management/pull/338))


### OpenSearch Index Management Dashboards Plugin
* Adds UI for shrink action ([#176](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/176))


### OpenSearch Job Scheduler
* Enables locking on an arbitrary lockID ([164](https://github.com/opensearch-project/job-scheduler/pull/164))


### OpenSearch Notifications
* Use Notifications to manage your notification channel configurations in a centralized location and send messages to these channels
* This release also adds notification-specific REST APIs for CRUD operations on channels and internal transport APIs for integrating/communicating with other plugins


### OpenSearch Performance Analyzer
* Adds setting to enable/disable Thread Contention Monitoring ([#171](https://github.com/opensearch-project/performance-analyzer/pull/171))


### OpenSearch SQL
* Add Kmeans and AD command documentation ([#493](https://github.com/opensearch-project/sql/pull/493))
* Support more parameters for AD and KMEANS command, and update related documentation ([#515](https://github.com/opensearch-project/sql/pull/515))


### OpenSearch Security
* Add support for DLS Term Lookup Queries ([#1541](https://github.com/opensearch-project/security/pull/1541))

## ENHANCEMENT

### OpenSearch Alerting
* Add automated migration for Destinations to Notification configs ([#379](https://github.com/opensearch-project/alerting/pull/379]))
* Integrate with Notifications plugin for Alerting backend ([#401](https://github.com/opensearch-project/alerting/pull/401]))


### OpenSearch Alerting Dashboards Plugin
* Implemented UX support for configuring doc level monitors ([#218](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/218))
* Integrate Alerting Dashboards with Notifications Plugin ([#220](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/220))
* Added document column to alerts dashboard for doc level monitors. Adjusted alerts dashboard configuration to remove unused alert states for doc level monitors. Refactored style of alerts flyout based on UX feedback ([#223](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/223))
* Refactored alerts table for doc level monitors to display a flyout containing finding information ([#232](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/232))
* Added documentation ticket workflow ([#242](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/242))


### OpenSearch Anomaly Detection
* Changed usages of "master" to "clusterManager" in variable names ([#504](https://github.com/opensearch-project/anomaly-detection/pull/504))


### OpenSearch Common Utils
* Add SQL/PPL transport request/response models for SQL plugin ([#155](https://github.com/opensearch-project/common-utils/pull/155))
* Support sending email message via Notifications pass-through API ([#158](https://github.com/opensearch-project/common-utils/pull/158))


### OpenSearch Cross Cluster Replication
* Change the "Master" nomenclature ([#319](https://github.com/opensearch-project/cross-cluster-replication/issues/319))
* Replace checked-in ZIPs with dynamic dependencies ([#335](https://github.com/opensearch-project/cross-cluster-replication/issues/335))
* Add support for build version qualifiers ([#334](https://github.com/opensearch-project/cross-cluster-replication/issues/334))


### OpenSearch Dashboards Visualizations
* Support advanced settings ([#68](https://github.com/opensearch-project/dashboards-visualizations/pull/68))


### OpenSearch Index Management Dashboards Plugin
* Add refresh button to rollup page ([#132](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/132))
* Adding support to edit/create notifications using channels in IM ([#181](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/181))


### OpenSearch k-NN
* Add Abstraction for BWC tests with a basic test ([#388](https://github.com/opensearch-project/k-NN/pull/388))
* Add restart upgrade BWC Tests ([#387](https://github.com/opensearch-project/k-NN/pull/387))


### OpenSearch Ml Commons
* Add circuit breaker trigger count stat ([#274](https://github.com/opensearch-project/ml-commons/pull/274))


### OpenSearch Observability
* Remove button toggle and add stop button ([#623](https://github.com/opensearch-project/observability/pull/623))
* Add availability entry points ([#731](https://github.com/opensearch-project/observability/pull/731))


### OpenSearch Performance Analyzer
* Fixes calculation of average thread blocked time and average thread waited time ([#118](https://github.com/opensearch-project/performance-analyzer-rca/pull/118))


### OpenSearch Security
* Remove checked-in zip files ([#1774](https://github.com/opensearch-project/security/pull/1774))
* Introduce dfm_empty_overrides_all setting to enable role without dls/fls to override roles with dls/fls ([#1735](https://github.com/opensearch-project/security/pull/1735))
* Add depreciation notice to security tools ([#1756](https://github.com/opensearch-project/security/pull/1756))
* [Practice] Reverting changes ([#1754](https://github.com/opensearch-project/security/pull/1754))
* Renames securityconfig folder to config in bundle step and makes relevant changes ([#1749](https://github.com/opensearch-project/security/pull/1749))
* Updated issue templates from .github ([#1740](https://github.com/opensearch-project/security/pull/1740))
* Updates Dev guide ([#1590](https://github.com/opensearch-project/security/pull/1590))
* List out test failures in CI log ([#1737](https://github.com/opensearch-project/security/pull/1737))
* Make Git ignore out/ directory ([#1734](https://github.com/opensearch-project/security/pull/1734))
* Fix data-stream name resolution for wild-cards ([#1723](https://github.com/opensearch-project/security/pull/1723))
* Remove support for JDK14 ([#1720](https://github.com/opensearch-project/security/pull/1720))
* Speeding up tests ([#1715](https://github.com/opensearch-project/security/pull/1715))
* Fix min_doc_count handling when using Document Level Security ([#1714](https://github.com/opensearch-project/security/pull/1714))
* Set the mapped security roles of the user so these can be used by the DLS privileges evaluator. Allow security roles to be used for DLS parameter substitution. Fixes opensearch-project/security/#1568 ([#1588](https://github.com/opensearch-project/security/pull/1588))
* Convert Plugin install to only build once ([#1708](https://github.com/opensearch-project/security/pull/1708))
* Upgrade to Gradle 7 ([#1710](https://github.com/opensearch-project/security/pull/1710))
* Move CodeQL into parallel workfow ([#1705](https://github.com/opensearch-project/security/pull/1705))
* Seperate BWC tests into parallel workflow ([#1706](https://github.com/opensearch-project/security/pull/1706))
* Fixes broken test due to unsupported EC using JDK-17 ([#1711](https://github.com/opensearch-project/security/pull/1711))
* Centralize version settings ([#1702](https://github.com/opensearch-project/security/pull/1702))
* Remove TransportClient auth/auth ([#1701](https://github.com/opensearch-project/security/pull/1701))
* Add new code hygiene workflow ([#1699](https://github.com/opensearch-project/security/pull/1699))
* Remove JDK8 from CI ([#1703](https://github.com/opensearch-project/security/pull/1703))
* Add CI check for demo script ([#1690](https://github.com/opensearch-project/security/pull/1690))
* Introduce BWC tests in security plugin ([#1685](https://github.com/opensearch-project/security/pull/1685))
* Correct the step name in CI ([#1683](https://github.com/opensearch-project/security/pull/1683))
* Add Alerting getFindings cluster permission ([#1844](https://github.com/opensearch-project/security/pull/1844))
* Introduce new API _plugins/_security/ssl/certs ([#1841](https://github.com/opensearch-project/security/pull/1841))
* Add default roles for Notifications plugin ([#1847](https://github.com/opensearch-project/security/pull/1847))


### OpenSearch Security Dashboards Plugin
* Change 2.0-alpha1 to 2.0-rc1 ([#946](https://github.com/opensearch-project/security-dashboards-plugin/pull/946))
* Make Git ignore .idea/ folder ([#944](https://github.com/opensearch-project/security-dashboards-plugin/pull/944))
* Updated issue templates from .github ([#931](https://github.com/opensearch-project/security-dashboards-plugin/pull/931))
* Bumps version of main to 2.0.0.0 ([#928](https://github.com/opensearch-project/security-dashboards-plugin/pull/928))
* Enforce authentication on api/status route by default ([#968](https://github.com/opensearch-project/security-dashboards-plugin/pull/968))


### OpenSearch SQL
* AD and Kmeans grammar edits ([#500](https://github.com/opensearch-project/sql/pull/500))


## BUG FIXES

### OpenSearch Alerting
* Completely fix docker pull and install plugin ([#376](https://github.com/opensearch-project/alerting/pull/376))
* Make sure alerting is using the build script in its own repo ([#377](https://github.com/opensearch-project/alerting/pull/377))
* fix security test workflow ([#407](https://github.com/opensearch-project/alerting/pull/407))
* Fixed a flaky test condition ([#375](https://github.com/opensearch-project/alerting/pull/375]))
* Remove actionGet and fix minor bugs ([#424](https://github.com/opensearch-project/alerting/pull/424]))
* Fix UnsupportedOperation error while alert categorization in BucketLevel monitor ([#428](https://github.com/opensearch-project/alerting/pull/428]))
* Fix minor bugs and support per alert action execution for Document Level Monitors ([#441](https://github.com/opensearch-project/alerting/pull/441]))
* Fix minor bugs and pass in user context when retrieving user's notification channels ([#447](https://github.com/opensearch-project/alerting/pull/447]))
* Fix elevated security permission with Notification and minor bug fixes ([#449](https://github.com/opensearch-project/alerting/pull/449]))
* Improve error messaging on exceptions from notification channel retrieval and fix bug ([#451](https://github.com/opensearch-project/alerting/pull/451]))


### OpenSearch Alerting Dashboards Plugin
* Fixed a bug that was causing the UX to reset visual editor trigger conditions to their default values when a trigger name contained periods ([#204](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/204))
* Fixed a bug that was preventing the configured schedule from displaying when editing a monitor that was created through backend commands ([#197](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/197))
* Fixed bugs associated with alerts table, and addressed UX review feedback ([#222](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/222))
* Document level monitor UX bug fixes ([#226](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/226))
* Fixed issues found during bug bash, and implemented tests ([#240](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/240))


### OpenSearch Anomaly Detection
* Changed default description to empty string instead of null ([#438](https://github.com/opensearch-project/anomaly-detection/pull/438))
* Fixed ADTaskProfile toXContent bug and added to .gitignore ([#447](https://github.com/opensearch-project/anomaly-detection/pull/447))
* Fix restart HCAD detector bug ([#460](https://github.com/opensearch-project/anomaly-detection/pull/460))
* Check if indices exist in the presence of empty search results ([#495](https://github.com/opensearch-project/anomaly-detection/pull/495))


### OpenSearch Anomaly Detection Dashboards
* Remove extra loading spinners ([#238](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/238))
* Remove additional loading spinners and removing master from docker compose ([#243](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/243))
* Wait for detector to load before checking indices exist ([#262](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/262))


### OpenSearch Cross Cluster Replication
* Bugfix: 2.0 Changes for CI workflows ([#354](https://github.com/opensearch-project/cross-cluster-replication/issues/354))
* Remove mapping types ([#318](https://github.com/opensearch-project/cross-cluster-replication/issues/318))


### OpenSearch Dashboards Reports
* Bump async from 3.2.0 to 3.2.3 in /dashboards-reports ([#338](https://github.com/opensearch-project/dashboards-reports/pull/338))
* Bump moment from 2.29.1 to 2.29.3 in /dashboards-reports ([#344](https://github.com/opensearch-project/dashboards-reports/pull/344))
* Bump minimist from 1.2.5 to 1.2.6 in /dashboards-reports ([#321](https://github.com/opensearch-project/dashboards-reports/pull/321))


### OpenSearch Dashboards Visualizations
* Bump async from 3.2.0 to 3.2.3 in /gantt-chart ([#67](https://github.com/opensearch-project/dashboards-visualizations/pull/67))
* Bump moment from 2.29.1 to 2.29.2 in /gantt-chart ([#66](https://github.com/opensearch-project/dashboards-visualizations/pull/66))
* Bump minimist from 1.2.5 to 1.2.6 in /gantt-chart ([#57](https://github.com/opensearch-project/dashboards-visualizations/pull/57))
* Remove duplicated dependencies ([#64](https://github.com/opensearch-project/dashboards-visualizations/pull/64))


### OpenSearch Index Management
* Fix metadata migration logic error when update setting call failed ([#328](https://github.com/opensearch-project/index-management/pull/328))
* Updates search text field to keyword subfield for policies and managed indices ([#267](https://github.com/opensearch-project/index-management/pull/267))
* Fixes shard allocation checks ([#335](https://github.com/opensearch-project/index-management/pull/335))
* BugFix: Notification integration issues ([#339](https://github.com/opensearch-project/index-management/pull/339))
* Fixes flaky continuous transforms and shrink tests ([#340](https://github.com/opensearch-project/index-management/pull/340))
* Minor improvements ([#345](https://github.com/opensearch-project/index-management/pull/345))
* Strengthen scroll search in Coordinator ([#356](https://github.com/opensearch-project/index-management/pull/356))
* Refactors shrink action steps and adds unit tests ([#349](https://github.com/opensearch-project/index-management/pull/349))


### OpenSearch Index Management Dashboards Plugin
* Fix rendering in transforms UI ([#179](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/179))
* Fix channels URI ([#184](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/184))


### OpenSearch Ml Commons
* Support dispatching execute task; don't dispatch ML task again ([#279](https://github.com/opensearch-project/ml-commons/pull/279))
* Fix NPE in anomaly localization ([#280](https://github.com/opensearch-project/ml-commons/pull/280))
* Create model/task index with correct mapping ([#284](https://github.com/opensearch-project/ml-commons/pull/284))


### OpenSearch Observability
* Edit visualization time change ([#617](https://github.com/opensearch-project/observability/pull/617))
* Remove duplicated node dependencies ([#620](https://github.com/opensearch-project/observability/pull/620))
* Bug fixes for application analytics ([#608](https://github.com/opensearch-project/observability/pull/608))
* Fixes trace analytics invalid service map and increase span limit ([#629](https://github.com/opensearch-project/observability/pull/629))
* Adding legacy UI route for traces ([#653](https://github.com/opensearch-project/observability/pull/653))
* Fix change availability bug ([#667](https://github.com/opensearch-project/observability/pull/667))
* Fix test to check for empty event analytics ([#669](https://github.com/opensearch-project/observability/pull/669))
* Bump prismjs from 1.25.0 to 1.27.0 in /dashboards-observability ([#508](https://github.com/opensearch-project/observability/pull/508))
* Bump minimist from 1.2.5 to 1.2.6 in /dashboards-observability ([#614](https://github.com/opensearch-project/observability/pull/614))
* Bump moment from 2.29.1 to 2.29.2 in /dashboards-observability ([#636](https://github.com/opensearch-project/observability/pull/636))
* Bump async from 3.2.1 to 3.2.3 in /dashboards-observability ([#654](https://github.com/opensearch-project/observability/pull/654))
* Update availabilityVizId if visualization is removed from panel ([#732](https://github.com/opensearch-project/observability/pull/732))
* Issue fix not a function error ([#739](https://github.com/opensearch-project/observability/pull/739))


### OpenSearch Performance Analyzer
* Fix EventLogFileHandlerTests flaky test ([#178](https://github.com/opensearch-project/performance-analyzer/pull/178))
* Add retry for tests ([#180](https://github.com/opensearch-project/performance-analyzer/pull/180))


### OpenSearch Security
* Add signal/wait model for TestAuditlogImpl ([#1758](https://github.com/opensearch-project/security/pull/1758))
* Switch to log4j logger ([#1751](https://github.com/opensearch-project/security/pull/1751))
* Remove sleep when waiting for node closure ([#1722](https://github.com/opensearch-project/security/pull/1722))
* Remove explictt dependency on jackson-databind ([#1709](https://github.com/opensearch-project/security/pull/1709))
* Fix break thaat was missed during a merge ([#1707](https://github.com/opensearch-project/security/pull/1707))
* Revert "Replace opensearch class names with opendistro class names during serialization and restore them back during deserialization (#1278)" ([#1691](https://github.com/opensearch-project/security/pull/1691))
* Update to most recent verson of jackson-databind ([#1679](https://github.com/opensearch-project/security/pull/1679))
* Fixed rest status for the replication action failure with DLS/FLS and ([#1677](https://github.com/opensearch-project/security/pull/1677))
* Downgrade Gradle version ([#1661](https://github.com/opensearch-project/security/pull/1661))
* Fix 'openserach' typo in roles.yml ([#1770](https://github.com/opensearch-project/security/pull/1770))


### OpenSearch Security Dashboards Plugin
* Fix broken `nextUrl=` parameter logic ([#940](https://github.com/opensearch-project/security-dashboards-plugin/pull/940))
* Fix 'openserach' typo in constants.tsx ([#953](https://github.com/opensearch-project/security-dashboards-plugin/pull/953))
* Select tenant popup only appears when mutli-tenacy is enabled ([#965](https://github.com/opensearch-project/security-dashboards-plugin/pull/965))


### OpenSearch SQL
* Bump async from 3.2.0 to 3.2.3 in /workbench ([#559](https://github.com/opensearch-project/sql/pull/559))
* Bump moment from 2.29.1 to 2.29.2 in /workbench ([#546](https://github.com/opensearch-project/sql/pull/546))
* Version Bump: spring-beans-5.2.19 -> spring-beans-5.2.20 ([#527](https://github.com/opensearch-project/sql/pull/527))
* Bug Fix, return default ID when log4j ThreadContext is empty ([#538](https://github.com/opensearch-project/sql/pull/538))
* Removed ES reference from build.gradle ([#562](https://github.com/opensearch-project/sql/pull/562))


## INFRASTRUCTURE

### OpenSearch Alerting
* Removed the Beta label from the bug report template ([#353](https://github.com/opensearch-project/alerting/pull/353))
* Update alerting with qualifier support in releases ([#366](https://github.com/opensearch-project/alerting/pull/366))
* Use OpenSearch 2.0.0-alpha1 ([#370](https://github.com/opensearch-project/alerting/pull/370))
* Add build qualifier default to alpha1 for 2.0.0 ([#373](https://github.com/opensearch-project/alerting/pull/373))
* Remove JDK 14 and Add JDK 17 ([#383](https://github.com/opensearch-project/alerting/pull/383))
* Updated issue templates from .github ([#382](https://github.com/opensearch-project/alerting/pull/382))
* Incremented version to 2.0-rc1 ([#404](https://github.com/opensearch-project/alerting/pull/404))
* Replace checked-in ZIP for bwc tests with a dynamic dependency ([#411](https://github.com/opensearch-project/alerting/pull/411))
* Update integTest gradle scripts to run via remote cluster independently ([#418](https://github.com/opensearch-project/alerting/pull/418))


### OpenSearch Alerting Dashboards Plugin
* Removed the Beta label from the bug report template ([#196](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/196))
* Updated issue templates from .github ([#205](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/205))


### OpenSearch Anomaly Detection
* Reduced jacoco exclusions and added more tests ([#446](https://github.com/opensearch-project/anomaly-detection/pull/446))
* Refactor SearchADResultTransportAction to be more testable ([#517](https://github.com/opensearch-project/anomaly-detection/pull/517))
* Remove oss flavor ([#449](https://github.com/opensearch-project/anomaly-detection/pull/449))
* Add auto labeler workflow ([#455](https://github.com/opensearch-project/anomaly-detection/pull/455))
* Gradle 7 and Opensearch 2.0 upgrade ([#464](https://github.com/opensearch-project/anomaly-detection/pull/464))
* Adding test-retry plugin ([#456](https://github.com/opensearch-project/anomaly-detection/pull/456))
* Updated issue templates from .github ([#488](https://github.com/opensearch-project/anomaly-detection/pull/488))
* Removing job-scheduler zip and replacing with distribution build ([#487](https://github.com/opensearch-project/anomaly-detection/pull/487))
* JDK 17 support ([#489](https://github.com/opensearch-project/anomaly-detection/pull/489))
* Moving script file in scripts folder  for file location standardization ([#494](https://github.com/opensearch-project/anomaly-detection/pull/494))
* Removed rcf jar for 3.0-rc1 and fixed zip fetching for AD and JS ([#500](https://github.com/opensearch-project/anomaly-detection/pull/500))
* Remove BWC zips for dynamic dependency  ([#505](https://github.com/opensearch-project/anomaly-detection/pull/505))
* Bump rcf to 3.0-rc2.1 ([#519](https://github.com/opensearch-project/anomaly-detection/pull/519))
* Increase more coverage and reduce jacocoExclusions ([#533](https://github.com/opensearch-project/anomaly-detection/pull/533))


### OpenSearch Anomaly Detection Dashboards
* Add auto labeler workflow ([#205](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/205))
* Updated issue templates from .github ([#226](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/226))
* 2.0 version bump ([#230](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/230))
* Change 2.0-alpha1 to 2.0-rc1 ([#241](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/241))
* Update labeler to default backports to 2.x ([#246](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/246))


### OpenSearch Asynchronous Search
* Adding support for integration tests with remote cluster ([#111](https://github.com/opensearch-project/asynchronous-search/pull/111))
* Remove support for JDK 8 ([#114](https://github.com/opensearch-project/asynchronous-search/pull/114))
* Remove support for JDK 14 ([#125](https://github.com/opensearch-project/asynchronous-search/pull/125))
* Updated issue templates from .github ([#126](https://github.com/opensearch-project/asynchronous-search/pull/126))
* Replace checked-in ZIP with a dynamic dependency ([#133](https://github.com/opensearch-project/asynchronous-search/pull/133))


### OpenSearch Common Utils
* Upgrade gradle artifacts to 7.3.3 ([#135](https://github.com/opensearch-project/common-utils/pull/135)
* Update common-utils to depend on the OpenSearch repositories plugin ([#137](https://github.com/opensearch-project/common-utils/pull/137))
* Add sign-off option for version workflow PR ([#143](https://github.com/opensearch-project/common-utils/pull/143))
* Add qualifier default to alpha1 in build.gradle ([#151](https://github.com/opensearch-project/common-utils/pull/151))
* Update issue templates from github for bugs and features ([#154](https://github.com/opensearch-project/common-utils/pull/154))
* Remove support for JDK 14 ([#159](https://github.com/opensearch-project/common-utils/pull/159))
* Remove RC1 as the qualifier from Common Utils ([#168](https://github.com/opensearch-project/common-utils/pull/168))


### OpenSearch Cross Cluster Replication
* [CI] Add support for JDK 17 ([#331](https://github.com/opensearch-project/cross-cluster-replication/issues/331))
* Remove support for JDK 8 ([#330](https://github.com/opensearch-project/cross-cluster-replication/issues/330))
* Drop support for JDK 14 ([#346](https://github.com/opensearch-project/cross-cluster-replication/issues/346))


### OpenSearch Dashboards Reports
* Added missing zip for bwc tests ([#329](https://github.com/opensearch-project/dashboards-reports/pull/329))
* Remove JDK14 from CI ([#335](https://github.com/opensearch-project/dashboards-reports/pull/335))
* Updated issue templates from .github ([#328](https://github.com/opensearch-project/dashboards-reports/pull/328))
* Remove zips and download from remote at build time ([#337](https://github.com/opensearch-project/dashboards-reports/pull/337))
* Support integTestRemote with security enabled endpoint ([#354](https://github.com/opensearch-project/dashboards-reports/pull/354))


### OpenSearch Index Management
* Replace checked-in ZIPs with dynamic dependencies ([#327](https://github.com/opensearch-project/index-management/pull/327))
* Only download JS zip when integTest is running ([#334](https://github.com/opensearch-project/index-management/pull/334))


### OpenSearch Job Scheduler
* Fix qualifier to be added as version number matching with core ([152](https://github.com/opensearch-project/job-scheduler/pull/152))
* Adding signoff option for version workflow PR ([156](https://github.com/opensearch-project/job-scheduler/pull/156))
* Add default alpha1 to JS qualifier ([162](https://github.com/opensearch-project/job-scheduler/pull/162))
* Remove hardcoding snapshot for JS in gradle ([163](https://github.com/opensearch-project/job-scheduler/pull/163))


### OpenSearch k-NN
* Update jacoco version to 0.8.7 to support JDK 17  ([#372](https://github.com/opensearch-project/k-NN/pull/372))
* Remove rc1 build qualifier for 2.0 GA release ([#395](https://github.com/opensearch-project/k-NN/pull/395))


### OpenSearch Ml Commons
* Drop support for JDK 14 ([#267](https://github.com/opensearch-project/ml-commons/pull/267))
* Add UT/IT Coverage for action/models and action/tasks ([#268](https://github.com/opensearch-project/ml-commons/pull/268))
* Default qualifier to alpha1 and fix workflows ([#269](https://github.com/opensearch-project/ml-commons/pull/269))
* Remove additional vars in build.gradle that are not used ([#271](https://github.com/opensearch-project/ml-commons/pull/271))
* Add UT for Search transport action ([#272](https://github.com/opensearch-project/ml-commons/pull/272))
* Updated issue templates for bugs and features ([#273](https://github.com/opensearch-project/ml-commons/pull/273))
* Add more test to improve coverage of abstract search action([#275](https://github.com/opensearch-project/ml-commons/pull/275))
* Add UT for RestMLExecuteAction, and remove it out from the jacoco exclusive list ([#278](https://github.com/opensearch-project/ml-commons/pull/278))
* Add coverage badges ([#281](https://github.com/opensearch-project/ml-commons/pull/281))
* Re-enable docker image tests for 2.0 ([#288](https://github.com/opensearch-project/ml-commons/pull/288))


### OpenSearch Observability
* Bwc update ([#604](https://github.com/opensearch-project/observability/pull/604))
* Event cypress tests ([#611](https://github.com/opensearch-project/observability/pull/611))
* Test 2.0 ([#624](https://github.com/opensearch-project/observability/pull/624))
* Updated panel flaky cypress tests ([#633](https://github.com/opensearch-project/observability/pull/633))
* Updated notebook cypress tests ([#637](https://github.com/opensearch-project/observability/pull/637))
* Updated events flyout ui, unskip jest tests ([#638](https://github.com/opensearch-project/observability/pull/638))
* Remove zips used by bwc tests ([#648](https://github.com/opensearch-project/observability/pull/648))
* Fix trace analytics cypress ([#652](https://github.com/opensearch-project/observability/pull/652))
* Event analytics jest tests ([#651](https://github.com/opensearch-project/observability/pull/651))
* 2.0 cypress tests ([#658](https://github.com/opensearch-project/observability/pull/658))
* Updated issue templates from .github ([#662](https://github.com/opensearch-project/observability/pull/662))
* Removing add sample data test from panels cypress ([#668](https://github.com/opensearch-project/observability/pull/668))
* [OSD][Tests] add test subject to app title for app analytics ([#686](https://github.com/opensearch-project/observability/pull/686))
* Support integTestRemote with security enabled endpoint ([#699](https://github.com/opensearch-project/observability/pull/699))
* Add data test subj to fix cypress tests ([#704](https://github.com/opensearch-project/observability/pull/704))


### OpenSearch SQL
* Fix bwc build issue with jdk17 ([#520](https://github.com/opensearch-project/sql/pull/520))
* Updated issue templates from .github ([#531](https://github.com/opensearch-project/sql/pull/531))
* Removing JDK14 from CI ([#547](https://github.com/opensearch-project/sql/pull/547))
* Replace checked-in ZIP with a dynamic dependency ([#514](https://github.com/opensearch-project/sql/pull/514))


## DOCUMENTATION

### OpenSearch Alerting
* Add Document Level Alerting RFC ([#388](https://github.com/opensearch-project/alerting/pull/388]))
* Deprecate the Master nomenclature in 2.0 ([#415](https://github.com/opensearch-project/alerting/pull/415]))
* Add release notes for version 2.0.0-rc1 ([#426](https://github.com/opensearch-project/alerting/pull/426))


### OpenSearch Alerting Dashboards Plugin
* Add release notes for version 2.0.0-rc1 ([#227](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/227))
* Drafted release notes for 2.0.0 ([#248](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/248))


### OpenSearch Anomaly Detection
* Add Visualization integration RFC docs ([#477](https://github.com/opensearch-project/anomaly-detection/pull/477))


### OpenSearch Anomaly Detection Dashboards
* Update integ tests badge in README ([#215](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/215))


### OpenSearch Asynchronous Search
* Change master nomenclature ([#116](https://github.com/opensearch-project/asynchronous-search/pull/116))


### OpenSearch Common Utils
* Add release notes for version 2.0.0-rc1 ([#162](https://github.com/opensearch-project/common-utils/pull/162))
* Add release notes for version 2.0.0.0 ([#177](https://github.com/opensearch-project/common-utils/pull/177))


### OpenSearch Dashboards Reports
* Remove master and whitelist text ([#342](https://github.com/opensearch-project/dashboards-reports/pull/342))


### OpenSearch Dashboards Visualizations
* Updated issue templates from .github ([#59](https://github.com/opensearch-project/dashboards-visualizations/pull/59))


### OpenSearch Index Management
* Updated issue templates from .github ([#324](https://github.com/opensearch-project/index-management/pull/324))


### OpenSearch Index Management Dashboards Plugin
* Updated issue templates from .github ([#168](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/168))
* Adds release notes for 2.0.0.0-rc1 ([#182](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/182))


### OpenSearch Job Scheduler
* Updated issue templates from .github ([165](https://github.com/opensearch-project/job-scheduler/pull/165))


### OpenSearch Observability
* Remove master and whitelist text ([#657](https://github.com/opensearch-project/observability/pull/657))


### OpenSearch Performance Analyzer
* Updated issue templates from .github ([#177](https://github.com/opensearch-project/performance-analyzer/pull/177))
* Removing metrics which are not required now as were removed in OS 2.0 ([#159](https://github.com/opensearch-project/performance-analyzer-rca/pull/159))


### OpenSearch SQL
* Change master nomenclature ([#551](https://github.com/opensearch-project/sql/pull/551))
* Change blacklist and whitelist nomenclature ([#560](https://github.com/opensearch-project/sql/pull/560))


## MAINTENANCE

### OpenSearch Alerting
* Upgrade kotlin to 1.16.10 ([#356](https://github.com/opensearch-project/alerting/pull/356]))
* Upgrade Alerting to 2.0 ([#357](https://github.com/opensearch-project/alerting/pull/357]))
* Remove rc1 qualifier from plugin version ([#442](https://github.com/opensearch-project/alerting/pull/442]))


### OpenSearch Alerting Dashboards Plugin
* Bumped main branch version to 2.0 to align with OpenSearch-Dashboards. Added alpha1 qualifier to align with backend snapshot version ([#202](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/202))
* [Build] bump plugin version to 2.0.0.0-rc1 ([#213](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/213))
* Incremented version to 2.0-rc1 ([#216](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/216))
* Updated versions of various dependencies to address CVEs ([#235](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/235))
* Removed the rc1 qualifier from the plugin version, changed OSD version used by test workflows to 2.0, added test environment ([#238](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/238))
* Enabled CI for 2.* branches, and removed redundant bug report template ([#246](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/246))


### OpenSearch Asynchronous Search
* Upgrades to Opensearch 2.0, Gradle 7.3 and fixes ([#110](https://github.com/opensearch-project/asynchronous-search/pull/110))
* Add support for -Dbuild.version_qualifier ([#115](https://github.com/opensearch-project/asynchronous-search/pull/115))
* Remove usage of mapping types ([#119](https://github.com/opensearch-project/asynchronous-search/pull/119))
* Remove hardcoding of versions in workflow ([#120](https://github.com/opensearch-project/asynchronous-search/pull/120))
* Add qualifier default as alpha ([#123](https://github.com/opensearch-project/asynchronous-search/pull/123))
* Change 2.0-alpha1 to 2.0-rc1 ([#131](https://github.com/opensearch-project/asynchronous-search/pull/131))
* Change 2.0-rc1 to 2.0 ([#143](https://github.com/opensearch-project/asynchronous-search/pull/143))


### OpenSearch Dashboards Reports
* Bump version to 2.0.0 ([#311](https://github.com/opensearch-project/dashboards-reports/pull/311))
* Support build version qualifier for reports-scheduler ([#322](https://github.com/opensearch-project/dashboards-reports/pull/322))
* Bump to 2.0 alpha1 and gradle 7 ([#325](https://github.com/opensearch-project/dashboards-reports/pull/325))
* Make sure qualifier is applied in 2.0.0 ([#327](https://github.com/opensearch-project/dashboards-reports/pull/327))
* Change alpha1 to rc1 for first 2.0 release ([#333](https://github.com/opensearch-project/dashboards-reports/pull/333))
* Change 2.0-alpha1 to 2.0-rc1 ([#341](https://github.com/opensearch-project/dashboards-reports/pull/341))
* Remove rc1 qualifier reference ([#358](https://github.com/opensearch-project/dashboards-reports/pull/358))


### OpenSearch Dashboards Visualizations
* Change alpha1 to rc1 for first 2.0 release ([#65](https://github.com/opensearch-project/dashboards-visualizations/pull/65))
* Bump version to 2.0.0 ([#56](https://github.com/opensearch-project/dashboards-visualizations/pull/56))
* Add alpha1 qualifiers for dashboards plugin ([#58](https://github.com/opensearch-project/dashboards-visualizations/pull/58))
* Remove rc1 qualifier for 2.0 ([#80](https://github.com/opensearch-project/dashboards-visualizations/pull/80))


### OpenSearch Index Management
* Upgrades Index Management to use 2.0.0-alpha1 of OpenSearch and dependencies ([#318](https://github.com/opensearch-project/index-management/pull/318))
* Make sure qualifier default is alpha1 in IM ([#323](https://github.com/opensearch-project/index-management/pull/323))
* Incremented version to 2.0-rc1 ([#331](https://github.com/opensearch-project/index-management/pull/331))
* Non-inclusive nonmenclature update ([#337](https://github.com/opensearch-project/index-management/pull/337))
* Removes rc1 qualifier ([#353](https://github.com/opensearch-project/index-management/pull/353))


### OpenSearch Index Management Dashboards Plugin
* Upgrades IM Dashboard plugin to OpenSearch Dashboards 2.0 ([#169](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/169))
* Bumps version to 2.0.0.0-rc1 ([#172](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/172))
* Incremented version to 2.0-rc1 ([#175](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/175))
* Removes rc1 version qualifier ([#192](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/192))
* Remove node version in package.json ([#186](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/186))
* Wrap up node removal and bump as dependabot suggest ([#193](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/193))

### OpenSearch Job Scheduler
* Removes usage of mapping types ([155](https://github.com/opensearch-project/job-scheduler/pull/155))
* Dropping support for jdk 14 ([168](https://github.com/opensearch-project/job-scheduler/pull/168))
* Incremented version to 2.0-rc1  ([169](https://github.com/opensearch-project/job-scheduler/pull/169))
* Removes rc1 version qualifier  ([178](https://github.com/opensearch-project/job-scheduler/pull/178))


### OpenSearch Ml Commons
* Change 2.0-alpha1 to 2.0-rc1 ([#282](https://github.com/opensearch-project/ml-commons/pull/282))
* Bump RCF version to 3.0-rc2.1 ([#289](https://github.com/opensearch-project/ml-commons/pull/289))
* Bump tribuo version to 4.2.1 ([#312](https://github.com/opensearch-project/ml-commons/pull/312))


### OpenSearch Observability
* Bump plugins to 2.0 and support build.version_qualifier ([#602](https://github.com/opensearch-project/observability/pull/602))
* Add alpha1 qualifier and JDK 17 for backend ([#607](https://github.com/opensearch-project/observability/pull/607))
* Add alpha1 qualifiers for dashboards plugin ([#616](https://github.com/opensearch-project/observability/pull/616))
* Tweak build.gradle to have the correct qualifiers in 2.0.0 ([#619](https://github.com/opensearch-project/observability/pull/619))
* Change alpha1 to rc1 for first 2.0 release ([#635](https://github.com/opensearch-project/observability/pull/635))
* Change 2.0-alpha1 to 2.0-rc1 ([#655](https://github.com/opensearch-project/observability/pull/655))
* Remove Candlestick chart from Visualizations ([#690](https://github.com/opensearch-project/observability/pull/690))
* Remove rc1 reference ([#730](https://github.com/opensearch-project/observability/pull/730))


### OpenSearch Performance Analyzer
* Gradle 7, JDK related changes and OS 2.0 ([#179](https://github.com/opensearch-project/performance-analyzer/pull/179))
* Add additional logs for Integration Tests ([#182](https://github.com/opensearch-project/performance-analyzer/pull/182))
* Enable dependency license check and removing unused license ([#183](https://github.com/opensearch-project/performance-analyzer/pull/183))
* Moving build script file here from opensearch build package ([#184](https://github.com/opensearch-project/performance-analyzer/pull/184))
* Update directory names and remove jar for integTest ([#187](https://github.com/opensearch-project/performance-analyzer/pull/187))
* Update PA directories from plugins to root ([#189](https://github.com/opensearch-project/performance-analyzer/pull/189))
* Changes to add jdk17, remove jdk 8,14, OS 2.0 and upgrade to gradle 7 ([#156](https://github.com/opensearch-project/performance-analyzer-rca/pull/156))
* Update directory names ([#166](https://github.com/opensearch-project/performance-analyzer-rca/pull/166))
* Update PA directories from plugins to root ([#168](https://github.com/opensearch-project/performance-analyzer-rca/pull/168))


### OpenSearch Security
* Incremented version to 2.0-rc1 ([#1764](https://github.com/opensearch-project/security/pull/1764))
* Upgrade to opensearch 2.0.0 alpha1 ([#1741](https://github.com/opensearch-project/security/pull/1741))
* Upgrade to OpenSearch 2.0.0 ([#1698](https://github.com/opensearch-project/security/pull/1698))
* Move to version 2.0.0.0 ([#1695](https://github.com/opensearch-project/security/pull/1695))
* Generate release notes for 2.0.0 ([#1772](https://github.com/opensearch-project/security/pull/1772))
* Switch from RC1 to the GA of OpenSearch 2.0 ([#1826](https://github.com/opensearch-project/security/pull/1826))
* Updates dependency vulnerabilities versions ([#1806](https://github.com/opensearch-project/security/pull/1806))
* Update org.springframework:spring-core to 5.3.20 ([#1850](https://github.com/opensearch-project/security/pull/1850))


### OpenSearch Security Dashboards Plugin
* Revert "Enforce authentication on api/status route by default (#943)" ([#950](https://github.com/opensearch-project/security-dashboards-plugin/pull/950))
* Enforce authentication on api/status route by default ([#943](https://github.com/opensearch-project/security-dashboards-plugin/pull/943))
* [Build] restore osdVersion to 2.0.0 ([#947](https://github.com/opensearch-project/security-dashboards-plugin/pull/947))
* [Build] bump to 2.0.0.0-rc1 ([#941](https://github.com/opensearch-project/security-dashboards-plugin/pull/941))
* Generate release notes for 2.0.0 ([#955](https://github.com/opensearch-project/security-dashboards-plugin/pull/955))
* Build OSD on 2.0 branch ([#986](https://github.com/opensearch-project/security-dashboards-plugin/pull/986))
* Remove redundant DCO check for the GitHub app ([#974](https://github.com/opensearch-project/security-dashboards-plugin/pull/974))
* Fixes broken main build which was caused due to version mismatch ([#989](https://github.com/opensearch-project/security-dashboards-plugin/pull/989))


### OpenSearch SQL
* Version 2.0 ([#507](https://github.com/opensearch-project/sql/pull/507))
* Removed changes introduced to support JDK8 ([#513](https://github.com/opensearch-project/sql/pull/513))
* Add JDK 17 support ([#512](https://github.com/opensearch-project/sql/pull/512))
* Upgrade OS Version to 2.0.0-alpha1-SNAPSHOT ([#518](https://github.com/opensearch-project/sql/pull/518))
* Add alpha1 qualifiers for dashboards plugin ([#523](https://github.com/opensearch-project/sql/pull/523))
* 2.0 build fix ([#535](https://github.com/opensearch-project/sql/pull/535))
* Change ODBC version to 1.4 for release ([#542](https://github.com/opensearch-project/sql/pull/542))
* Change workbench alpha1 to rc1 for first 2.0 release ([#545](https://github.com/opensearch-project/sql/pull/545))
* Change 2.0-alpha1 to 2.0-rc1. ([#555](https://github.com/opensearch-project/sql/pull/555))
* Replace checked-in ml-commons dependency for 2.0 ([#563](https://github.com/opensearch-project/sql/pull/563))
* Delete ml-commons zip file ([#565](https://github.com/opensearch-project/sql/pull/565))
* Bump ml-client to 2.0 ([#568](https://github.com/opensearch-project/sql/pull/568))
* Remove rc1 qualifier for 2.0 ([#600](https://github.com/opensearch-project/sql/pull/600))


## REFACTORING

### OpenSearch Alerting
* Remove write Destination APIs ([#412](https://github.com/opensearch-project/alerting/pull/412]))
* Remove Alerting's notification subproject ([#413](https://github.com/opensearch-project/alerting/pull/413]))
* Skipping destination migration if alerting index is not initialized ([#417](https://github.com/opensearch-project/alerting/pull/417]))
* Fix Finding action naming and update release notes ([#432](https://github.com/opensearch-project/alerting/pull/432]))


### OpenSearch Alerting Dashboards Plugin
* Temporarily disabled destination use in some cypress tests to resolve flakiness ([#214](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/214))
* Remove disabled buttons and update Destination flows to reflect read-only state ([#221](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/221))


### OpenSearch Common Utils
* Remove feature and feature_list usage for Notifications ([#136](https://github.com/opensearch-project/common-utils/pull/136))
* Rename references for Get Channels API for Notifications ([#140](https://github.com/opensearch-project/common-utils/pull/140))
* Remove allowedConfigFeatureList from GetPluginFeaturesResponse for Notifications ([#144](https://github.com/opensearch-project/common-utils/pull/144))
* Remove NotificationEvent Request, Response and SearchResults ([#153](https://github.com/opensearch-project/common-utils/pull/153))
* Add NotificationEvent to SendNotificationResponse and Removal of NotificationID ([#156](https://github.com/opensearch-project/common-utils/pull/156))
* Change BaseModel to extend ToXContentObject instead of ToXContent ([#173](https://github.com/opensearch-project/common-utils/pull/173))


### OpenSearch Ml Commons
* Removed RCF jars and updated to fetch RCF 3.0-rc2 from maven ([#277](https://github.com/opensearch-project/ml-commons/pull/277))


### OpenSearch Observability
* Modularize and cleanup traces ([#601](https://github.com/opensearch-project/observability/pull/601))
* Modularize and cleanup panel ([#603](https://github.com/opensearch-project/observability/pull/603))
* Modularize event Analytics live tail and fix bug ([#647](https://github.com/opensearch-project/observability/pull/647))
* Fix lint and modularize dashboard ([#583](https://github.com/opensearch-project/observability/pull/583))
* Modularize service and fix issues ([#595](https://github.com/opensearch-project/observability/pull/595))

