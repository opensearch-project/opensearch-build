# OpenSearch and Dashboards 1.1.0 Release Notes

## Release Highlights

## Release Details

OpenSearch and OpenSearch Dashboards 1.1.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.1.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.1.0.md).


## FEATURES

### OpenSearch Alerting
* Add BucketSelector pipeline aggregation extension ([#144](https://github.com/opensearch-project/alerting/pull/144))
* Add AggregationResultBucket ([#148](https://github.com/opensearch-project/alerting/pull/148))
* Add ActionExecutionPolicy ([#149](https://github.com/opensearch-project/alerting/pull/149))
* Refactor Monitor and Trigger to split into Query-Level and Bucket-Level Monitors ([#150](https://github.com/opensearch-project/alerting/pull/150))
* Update InputService for Bucket-Level Alerting ([#152](https://github.com/opensearch-project/alerting/pull/152))
* Update TriggerService for Bucket-Level Alerting ([#153](https://github.com/opensearch-project/alerting/pull/153))
* Update AlertService for Bucket-Level Alerting ([#154](https://github.com/opensearch-project/alerting/pull/154))
* Add worksheets to help with testing ([#151](https://github.com/opensearch-project/alerting/pull/151))
* Update MonitorRunner for Bucket-Level Alerting ([#155](https://github.com/opensearch-project/alerting/pull/155))
* Fix ktlint formatting issues ([#156](https://github.com/opensearch-project/alerting/pull/156))
* Execute Actions on runTrigger exceptions for Bucket-Level Monitor ([#157](https://github.com/opensearch-project/alerting/pull/157))
* Skip execution of Actions on ACKNOWLEDGED Alerts for Bucket-Level Monitors ([#158](https://github.com/opensearch-project/alerting/pull/158))
* Return first page of input results in MonitorRunResult for Bucket-Level Monitor ([#159](https://github.com/opensearch-project/alerting/pull/159))
* Add setting to limit per alert action executions and don't save Alerts for test Bucket-Level Monitors ([#161](https://github.com/opensearch-project/alerting/pull/161))
* Resolve default for ActionExecutionPolicy at runtime ([#165](https://github.com/opensearch-project/alerting/pull/165))


### OpenSearch Alerting Dashboards Plugin
* Bucket level alerting create monitor page refactor ([#62](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/62))
* Add DefineBucketLevelTrigger component ([#63](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/63))
* Refactor CreateTrigger components to support single-page experience ([#64](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/64))
* Update CreateMonitor to incorporate new single-page experience ([#65](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/65))
* Update Monitor overview page ([#66](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/66))
* Alert dashboard table column update ([#67](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/67))
* Refactored query and bucket-level trigger definitions to align with new mocks ([#68](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/68))
* Alert dashboard update on monitor ([#72](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/72))
* Create monitor page, bucket level monitor showing bar graph  ([#73](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/73))
* Use destination api to validate destination name ([#69](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/69))
* Update Monitor Details panel ([#75](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/75))
* Flyout panel on alert dashboard page ([#78](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/78))
* Add button to refresh graph , add accordion to expand/collapse graph view ([#79](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/79))
* Add success toast message for create and update monitor ([#80](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/80))
* Refactored trigger condition popover to dropdown menu. Refactored actions panel to hide throttling for 'per execution' ([#81](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/81))
* Added Export JSON button and modal to create/edit Monitor page ([#82](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/82))
* Added Monitor state EuiHealth element, replaced state item in overview with Monitor level type ([#83](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/83))
* Update alert history graph for bucket-level monitors ([#84](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/84))
* Refactored query trigger definition components to align with mocks. ([#85](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/85))
* Removed the close button from the top-right of the alert dashboard flyout. Refactored monitor details page for anomaly detection monitors. ([#86](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/86))
* Several changes in query panel ([#87](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/87))
* Implemented test message toast. Fixed alerts dashboard severity display bug. ([#88](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/88))
* Refactored Dashboard::getMonitors to function without using the from and size parameters from getAlerts ([#89](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/89))
* Query level monitor updates ([#90](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/90))
* Changes of metrics expression and graph  ([#95](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/95))
* Update formik conversion for Bucket-Level Trigger to handle throttle change ([#97](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/97))
* Implemented View alert details, and logic for landing page alerts dashboard. ([#98](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/98))
* Added limit text, adjusted spacing/sizing/text, etc. ([#100](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/100))
* Remove pagination and set default size of alerts pert trigger to 10000 ([#99](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/99))


### OpenSearch Anomaly Detection
* multi-category support, rate limiting, and pagination ([#121](https://github.com/opensearch-project/anomaly-detection/pull/121))
* Single flow feature change ([#147](https://github.com/opensearch-project/anomaly-detection/pull/147))
* Compact rcf integration ([#149](https://github.com/opensearch-project/anomaly-detection/pull/149))


### OpenSearch Anomaly Detection Dashboards
* Add single flow functionality ([#63](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/63))
* Support multiple category fields ([#66](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/66))


### OpenSearch Cross Cluster Replication
* Porting replication plugin to OpenSearch ([#8](https://github.com/opensearch-project/cross-cluster-replication/pull/8))
* Pause and Resume API ([#10](https://github.com/opensearch-project/cross-cluster-replication/pull/10))
* Leader Stats API ([#122](https://github.com/opensearch-project/cross-cluster-replication/pull/122))
* Follower stats API ([#126](https://github.com/opensearch-project/cross-cluster-replication/pull/126))
* AutoFollow Stats API Addition ([131](https://github.com/opensearch-project/cross-cluster-replication/pull/131))


### OpenSearch Index Management
* Storing user information as part of the job when security plugin is installed ([#113](https://github.com/opensearch-project/index-management/pull/113))
* Storing user object in all APIs and enabling filter of response based on user ([#115](https://github.com/opensearch-project/index-management/pull/115))
* Security improvements ([#126](https://github.com/opensearch-project/index-management/pull/126))
* Updating security filtering logic ([#137](https://github.com/opensearch-project/index-management/pull/137))


### OpenSearch Index Management Dashboards Plugin
* Adds custom label to use with EuiForm component ([#40](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/40))
* Adds reusable flyout footer ([#41](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/41))
* Adds a small Badge component ([#39](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/39))
* Adds legacy notification UI input ([#42](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/42))
* Adds draggable action component ([#43](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/43))
* Adds notification service to make backend call for getting list of channels for Index Management ([#46](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/46))
* Adds new UI for Channel Notification ([#44](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/44))
* Adds policy info section for new UI ([#45](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/45))
* Adds error notification UI container and updates snapshots ([#47](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/47))
* Adds draggable transitions and transition content ([#48](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/48))
* Adds UI actions for all the supported ISM actions ([#49](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/49))
* Adds individual ISM template UI component ([#51](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/51))
* Adds single state UI component ([#53](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/53))
* Adds timeout retry settings component used in action flyout ([#52](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/52))
* Adds States UI component ([#54](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/54))
* Adds ISM Templates UI component ([#55](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/55))
* Adds create action container shown in flyout ([#56](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/56))
* Adds transition component ([#57](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/57))
* Adds create transition container ([#59](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/59))
* Adds modal for choosing between visual and json editor ([#58](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/58))
* Adds create state container and removes unused props from modal and create transitions ([#60](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/60))
* Added PolicySettings and DeleteModal components for PolicyDetails UI ([#50](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/50))
* Adds VisualCreatePolicy page, missing backend routes/configs, updates all creation paths to show new modal, updates rates, etc. ([#61](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/61))
* Added PolicyDetails page ([#62](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/62))
* Register action hook ([#64](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/64))
* Fixes policy details page ([#80](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/80))
* Removes support for notification channels ([#81](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/81))


### OpenSearch Performance Analyzer
* AdmissionControl RequestSize AutoTuning ([#44](https://github.com/opensearch-project/performance-analyzer-rca/pull/44))


## ENHANCEMENTS

### OpenSearch Alerting Dashboards Plugin
* Show Error Toast Message whenever action execution fails from backend due to incorrect configurations ([#22](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/22))
* Bucket level alerting dev UX review feedback ([#93](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/93))
* Text updates ([#105](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/105))


### OpenSearch Anomaly Detection
* Disable model splitting in single-stream detectors ([#162](https://github.com/opensearch-project/anomaly-detection/pull/162))
* Handle more AD exceptions thrown over the wire/network ([#157](https://github.com/opensearch-project/anomaly-detection/pull/157))
* support historical analysis for multi-category HC ([#159](https://github.com/opensearch-project/anomaly-detection/pull/159))
* Limit the max models shown on the stats and profile API ([#182](https://github.com/opensearch-project/anomaly-detection/pull/182))
* Enable shingle in HCAD ([#187](https://github.com/opensearch-project/anomaly-detection/pull/187))
* add min score for labeling anomalies to thresholding ([#193](https://github.com/opensearch-project/anomaly-detection/pull/193))
* support backward compatibility of historical analysis and realtime task ([#195](https://github.com/opensearch-project/anomaly-detection/pull/195))


### OpenSearch Anomaly Detection Dashboards
* Fix BWC for custom & simple filters ([#68](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/68))
* Fix BWC for legacy detectors ([#69](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/69))
* Enable shingle in HCAD ([#71](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/71))
* Change single size description and fix related places ([#76](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/76))
* Enable zooming in HC entity charts ([#78](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/78))
* Add callouts and make category fields readonly after creation ([#79](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/79))
* Tune wording on category field callouts ([#83](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/83))



### OpenSearch Alerting Dashboards Plugin
* Show Error Toast Message whenever action execution fails from backend due to incorrect configurations ([#22](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/22))
* Bucket level alerting dev UX review feedback ([#93](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/93))
* Text updates ([#105](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/105))


### OpenSearch Anomaly Detection
* Disable model splitting in single-stream detectors ([#162](https://github.com/opensearch-project/anomaly-detection/pull/162))
* Handle more AD exceptions thrown over the wire/network ([#157](https://github.com/opensearch-project/anomaly-detection/pull/157))
* support historical analysis for multi-category HC ([#159](https://github.com/opensearch-project/anomaly-detection/pull/159))
* Limit the max models shown on the stats and profile API ([#182](https://github.com/opensearch-project/anomaly-detection/pull/182))
* Enable shingle in HCAD ([#187](https://github.com/opensearch-project/anomaly-detection/pull/187))
* add min score for labeling anomalies to thresholding ([#193](https://github.com/opensearch-project/anomaly-detection/pull/193))
* support backward compatibility of historical analysis and realtime task ([#195](https://github.com/opensearch-project/anomaly-detection/pull/195))


### OpenSearch Anomaly Detection Dashboards 
* Fix BWC for custom & simple filters ([#68](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/68))
* Fix BWC for legacy detectors ([#69](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/69))
* Enable shingle in HCAD ([#71](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/71))
* Change single size description and fix related places ([#76](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/76))
* Enable zooming in HC entity charts ([#78](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/78))
* Add callouts and make category fields readonly after creation ([#79](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/79))
* Tune wording on category field callouts ([#83](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/83))


### OpenSearch Cross Cluster Replication
* Configure the threadpool for leader cluster ([#14](https://github.com/opensearch-project/cross-cluster-replication/pull/14))
* Renew retention lease with the last known synced checkpoint ([#18](https://github.com/opensearch-project/cross-cluster-replication/pull/18))
* Handling node disconnections and shard movement ([#23](https://github.com/opensearch-project/cross-cluster-replication/pull/23))
* Enforce metadata write block on follower indices ([#120](https://github.com/opensearch-project/cross-cluster-replication/pull/20))
* Support for storing security metadata and Integration with security plugin ([#15](https://github.com/opensearch-project/cross-cluster-replication/pull/15))
* Fix for race condition with snapshot restore ([#28](https://github.com/opensearch-project/cross-cluster-replication/pull/28))
* Status api changes ([#26](https://github.com/opensearch-project/cross-cluster-replication/pull/26))
* Changed names for assume roles to remote and local from leader and follower ([#29](https://github.com/opensearch-project/cross-cluster-replication/pull/29))
* Added preference to fetch the metadata from the primary shard and additional logging for the metadata store ([#29](https://github.com/opensearch-project/cross-cluster-replication/pull/29))
* Handling leader cluster disconnection failure scenarios during bootstrap ([#17](https://github.com/opensearch-project/cross-cluster-replication/pull/17))
* Support for translog fetch at the leader(remote) cluster and enable translog pruning during replication setup ([#25](https://github.com/opensearch-project/cross-cluster-replication/pull/25))
* Added random active shard selector for the getchanges operations ([#33](https://github.com/opensearch-project/cross-cluster-replication/pull/33))
* Settings and Alias replication ([#22](https://github.com/opensearch-project/cross-cluster-replication/pull/34))
* Rename opendistro endpoints ([#36](https://github.com/opensearch-project/cross-cluster-replication/pull/36))
* Added connections alias and doc count in status api ([#38](https://github.com/opensearch-project/cross-cluster-replication/pull/38))
* Bootstrapping bug fix and few integ tests. ([#41](https://github.com/opensearch-project/cross-cluster-replication/pull/41))
* Adding validation on index settings ([#37](https://github.com/opensearch-project/cross-cluster-replication/pull/37))
* Renamed connection alias and changed exception handling ([#44](https://github.com/opensearch-project/cross-cluster-replication/pull/44))
* Added non verbose version of status api. ([#46](https://github.com/opensearch-project/cross-cluster-replication/pull/46))
* Added replication specific settings for recovery ([#46](https://github.com/opensearch-project/cross-cluster-replication/pull/46))
* Add support for parallel reader and writer for ShardReplicationTask ([#48](https://github.com/opensearch-project/cross-cluster-replication/pull/48))
* Changes to fail chain replication ([#50](https://github.com/opensearch-project/cross-cluster-replication/pull/50))
* Using non null RestoreInProgress value in case of no restore in progress ([#54](https://github.com/opensearch-project/cross-cluster-replication/pull/54))
* Not allowing index starting with . for replication ([#55](https://github.com/opensearch-project/cross-cluster-replication/pull/55))
* Changing the default recovery chunk size to 10MB ([#58](https://github.com/opensearch-project/cross-cluster-replication/pull/58))
* Added reason to the replication metadata store ([#57](https://github.com/opensearch-project/cross-cluster-replication/pull/57))
* Propagate shard failures to index task and auto-pause on failures ([#56](https://github.com/opensearch-project/cross-cluster-replication/pull/56))
* Propgate 4xx failures from ShardReplicationTask ([#60](https://github.com/opensearch-project/cross-cluster-replication/pull/60))
* Bug fixes and autofollow task resiliency ([#59](https://github.com/opensearch-project/cross-cluster-replication/pull/59))
* Added permission validation steps at user level and role level ([#62](https://github.com/opensearch-project/cross-cluster-replication/pull/62))
* Async metadata update. Separated metadata reader and updater ([#52](https://github.com/opensearch-project/cross-cluster-replication/pull/52))
* Validate analyzer path when starting/resuming replication ([#64](https://github.com/opensearch-project/cross-cluster-replication/pull/64))
* Prevent starting replication directly on the leader index alias. ([#66](https://github.com/opensearch-project/cross-cluster-replication/pull/66))
* Change to stop showing replication related metrics in case of non running (syncing and bootstrap) state. ([#68](https://github.com/opensearch-project/cross-cluster-replication/pull/68))
* Integ test for follower index deletion ([#68](https://github.com/opensearch-project/cross-cluster-replication/pull/68))
* Adding reason while serializing PauseReplication Request ([#71](https://github.com/opensearch-project/cross-cluster-replication/pull/71))
* Add integ test to verify mapping propagation ([#72](https://github.com/opensearch-project/cross-cluster-replication/pull/72))
* Integ test to verify that delete/index operation are blocked on follower ([#73](https://github.com/opensearch-project/cross-cluster-replication/pull/73))
* Changes to support security plugin integ tests ([#70](https://github.com/opensearch-project/cross-cluster-replication/pull/70))
* Integ test: Verify that replication is paused when remote index is deleted ([#74](https://github.com/opensearch-project/cross-cluster-replication/pull/74))
* added few integ tests when open and close is triggered on leader index ([#77](https://github.com/opensearch-project/cross-cluster-replication/pull/77))
* Integ test to stop replication when remote cluster is unreachable ([#69](https://github.com/opensearch-project/cross-cluster-replication/pull/69))
* Moved validation checks after setup checks ([#85](https://github.com/opensearch-project/cross-cluster-replication/pull/85))
* Modified tests to use custom roles for default tests ([#83](https://github.com/opensearch-project/cross-cluster-replication/pull/83))
* Replication engine tests: Index operations on leader ([#79](https://github.com/opensearch-project/cross-cluster-replication/pull/79))
* Add Handling of IndexReplicationTask cancellation and corresponding ITs ([#87](https://github.com/opensearch-project/cross-cluster-replication/pull/87))
* Updated security plugin with latest changes ([#89](https://github.com/opensearch-project/cross-cluster-replication/pull/89))
* Integ test: forcemerge and snapshot on leader during bootstrap ([#76](https://github.com/opensearch-project/cross-cluster-replication/pull/76))
* Validate that soft delete settings is enabled at leader ([#84](https://github.com/opensearch-project/cross-cluster-replication/pull/84))
* Adding Security for replication APIs and IT for DLS, FLS or FieldMasking ([#90](https://github.com/opensearch-project/cross-cluster-replication/pull/90))
* changed few naming conventions. 1. remote to leader, 2. local to follower, etc ([#75](https://github.com/opensearch-project/cross-cluster-replication/pull/75))
* Refactor code for OpenSearch ([#98](https://github.com/opensearch-project/cross-cluster-replication/pull/98))
* Port terminology from OpenDistroForElasticsearch to OpenSearch. ([#98](https://github.com/opensearch-project/cross-cluster-replication/pull/98))
* Changed the dependency to OS 1.1 ([#100](https://github.com/opensearch-project/cross-cluster-replication/pull/100))
* Rename the replication settings ([#103](https://github.com/opensearch-project/cross-cluster-replication/pull/103))
* Support for mapping update for the replication store system index ([#105](https://github.com/opensearch-project/cross-cluster-replication/pull/105))
* Adding UTs for IndexReplicationTask ([#109](https://github.com/opensearch-project/cross-cluster-replication/pull/109))
* OpenSearch Integ tests for reroutes ([#114](https://github.com/opensearch-project/cross-cluster-replication/pull/114))
* Adding exp backoff for replay and get changes ([#135](https://github.com/opensearch-project/cross-cluster-replication/pull/135))
* Rename to useroles in all the request payloads instead of assumeroles ([#154](https://github.com/opensearch-project/cross-cluster-replication/pull/154))
* Initializing shard metric for UT ([#141](https://github.com/opensearch-project/cross-cluster-replication/pull/141))
* Changing the log level to debug as this information is surfaced in stats ([#149](https://github.com/opensearch-project/cross-cluster-replication/pull/149))
* Pause API should allow reason to be specified in the REST call. ([#151](https://github.com/opensearch-project/cross-cluster-replication/pull/151))
* Verifying shard tasks are up in autofollow test ([#153](https://github.com/opensearch-project/cross-cluster-replication/pull/153))
* Correcting param name for leader API ([#163](https://github.com/opensearch-project/cross-cluster-replication/pull/163))
* Populate "AutoPaused: " prefix in the pause-reason while auto-pausing. ([#170](https://github.com/opensearch-project/cross-cluster-replication/pull/170))


### OpenSearch Dashboards Notebooks
* Improve wording for sample notebooks ([#57](https://github.com/opensearch-project/dashboards-notebooks/pull/57))


### OpenSearch Index Management
* Enhance ISM template ([#105](https://github.com/opensearch-project/index-management/pull/105))


### OpenSearch Performance Analyzer
* Use Collector override disable list for ShardIndexingPressureMetricCollector ([#28](https://github.com/opensearch-project/performance-analyzer/pull/28))
* Adding metric emission + UT for RCA_FRAMEWORK_CRASH ([#36](https://github.com/opensearch-project/performance-analyzer-rca/pull/36))
* Replace String split with Guava Splitter ([#42](https://github.com/opensearch-project/performance-analyzer-rca/pull/42))
* Add master not up writer metric ([#51](https://github.com/opensearch-project/performance-analyzer-rca/pull/51))


### OpenSearch Security
* Added replication specific roles and system index to the configuration ([#1408](https://github.com/opensearch-project/security/pull/1408))
* Handled DLS/FLS/Field masking for replication actions ([#1330](https://github.com/opensearch-project/security/pull/1330))
* Extended role injection support for cross cluster requests ([#1195](https://github.com/opensearch-project/security/pull/1195))
* Added changes to support validation of security roles for plugins ([#1367](https://github.com/opensearch-project/security/pull/1367))
* Adding the default role for IM plugin ([#1427](https://github.com/opensearch-project/security/pull/1427))


### OpenSearch SQL
* Support implicit type conversion from string to boolean ([#166](https://github.com/opensearch-project/sql/pull/166))
* Support distinct count aggregation ([#167](https://github.com/opensearch-project/sql/pull/167))
* Support implicit type conversion from string to temporal ([#171](https://github.com/opensearch-project/sql/pull/171))
* Workbench: auto dump cypress test data, support security ([#199](https://github.com/opensearch-project/sql/pull/199))

## BUG FIXES

### OpenSearch Alerting
* Removing All Usages of Action Get Method Calls and adding the listeners ([#130](https://github.com/opensearch-project/alerting/pull/130))
* Fix bug in paginating multiple bucket paths for Bucket-Level Monitor ([#163](https://github.com/opensearch-project/alerting/pull/163))
* Various bug fixes for Bucket-Level Alerting ([#164](https://github.com/opensearch-project/alerting/pull/164))
* Return only monitors for /monitors/_search ([#162](https://github.com/opensearch-project/alerting/pull/162))


### OpenSearch Anomaly Detection
* don't replace detector user when update ([#126](https://github.com/opensearch-project/anomaly-detection/pull/126))
* avoid sending back verbose error message and wrong 500 error to user; fix hard code query size of historical analysis ([#150](https://github.com/opensearch-project/anomaly-detection/pull/150))
* Bug fixes and unit tests ([#177](https://github.com/opensearch-project/anomaly-detection/pull/177))


### OpenSearch Anomaly Detection Dashboards
* Bug fixes for single flow feature ([#77](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/77))
* Clear HC charts when the date range changes ([#81](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/81))


### OpenSearch Asynchronous Search
* Fix: typo in flag name. ([#32](https://github.com/opensearch-project/asynchronous-search/pull/32))


### OpenSearch Cross Cluster Replication
* Fix submitClusterStateUpdateTask source ([#6](https://github.com/opensearch-project/cross-cluster-replication/pull/6))
* Throw exception if replication is not enabled on the remote domain ([#86](https://github.com/opensearch-project/cross-cluster-replication/pull/86))
* Increase wait time for snapshot/forcemerge integ tests ([#91](https://github.com/opensearch-project/cross-cluster-replication/pull/91))
* Add validation on index name ([#92](https://github.com/opensearch-project/cross-cluster-replication/pull/92))
* Remove opendistro security zip ([#95](https://github.com/opensearch-project/cross-cluster-replication/pull/95))
* Changes to restore default threadcontext after co-routine is suspended ([#102](https://github.com/opensearch-project/cross-cluster-replication/pull/102))
* Remove packaged example as replication plugin will ship with OpenSearch. ([#107](https://github.com/opensearch-project/cross-cluster-replication/pull/107))
* Handled errors during test role update ([#112](https://github.com/opensearch-project/cross-cluster-replication/pull/112))
* Ignore forbidden APIs to access private members of ES datastructure ([#120](https://github.com/opensearch-project/cross-cluster-replication/pull/120))
* Starting missing shard tasks ([#114](https://github.com/opensearch-project/cross-cluster-replication/pull/114))
* Fix for RetentionLeaseInvalidRetainingSeqNoException while adding retention lease ([#128](https://github.com/opensearch-project/cross-cluster-replication/pull/128))
* Fix IT Test ([#137](https://github.com/opensearch-project/cross-cluster-replication/pull/137))
* Fix RetentionLeaseNotFoundException during shard reroute on follower ([#138](https://github.com/opensearch-project/cross-cluster-replication/pull/138))
* Fix Flaky integ test ([#140](https://github.com/opensearch-project/cross-cluster-replication/pull/140))
* Handled rename change for useroles in tests ([#142](https://github.com/opensearch-project/cross-cluster-replication/pull/142))
* Remove the flaky assert in StartReplicationIT ([#144](https://github.com/opensearch-project/cross-cluster-replication/pull/144))
* Blocked k-NN index for replication ([#158](https://github.com/opensearch-project/cross-cluster-replication/pull/158))
* Gracefully fail replication on bootstrap failure. ([#116](https://github.com/opensearch-project/cross-cluster-replication/pull/166))


### OpenSearch Dashboards Reports
* Fix url validation ([#132](https://github.com/opensearch-project/dashboards-reports/pull/132))
* Fix url validation for context menu ([#134](https://github.com/opensearch-project/dashboards-reports/pull/134))


### OpenSearch Index Management
* Removing Usages of Action Get Call and using listeners ([#100](https://github.com/opensearch-project/index-management/pull/100))
* Explain response still use old opendistro policy id ([#109](https://github.com/opensearch-project/index-management/pull/109))
* Only rollover history index onMaster if enabled ([#142](https://github.com/opensearch-project/index-management/pull/142))


### OpenSearch Index Management Dashboards Plugin
* Address data stream API security breaking issue ([#69](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/69))
* Fix flaky ([#76](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/76))
* UI fixes for new ISM UI ([#84](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/84))
* Fixes some small UI touchups/issues for new ISM UI ([#85](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/85))
* Fixes small issues on new ISM UI ([#88](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/88))


### OpenSearch k-NN
* Fix copyright in README ([#76](https://github.com/opensearch-project/k-NN/pull/76))


### OpenSearch Performance Analyzer
* Handling empty flow unit during Cache/Queue RCA execution ([#34](https://github.com/opensearch-project/performance-analyzer-rca/pull/34))
* Fix for OOM error ([#35](https://github.com/opensearch-project/performance-analyzer-rca/pull/35))
* Fix thread name categorizations for Operation dimension in metrics API ([#44](https://github.com/opensearch-project/performance-analyzer-rca/pull/44)) 
* Add privileges for removing files ([#45](https://github.com/opensearch-project/performance-analyzer-rca/pull/45))
* Fix spotbugs failure by removing unused variable ([#47](https://github.com/opensearch-project/performance-analyzer-rca/pull/47))
* Change log level and remove retry ([#50](https://github.com/opensearch-project/performance-analyzer-rca/pull/50))
* Add retries for flaky tests and fix failing tests ([#52](https://github.com/opensearch-project/performance-analyzer-rca/pull/52))
* Fix deleting files within 60sec interval ([#62](https://github.com/opensearch-project/performance-analyzer/pull/62))


### OpenSearch SQL
* Fix for SQL-ODBC AWS Init and Shutdown Behaviour ([#163](https://github.com/opensearch-project/sql/pull/163))
* Fix import path for cypress constant ([#201](https://github.com/opensearch-project/sql/pull/201))


## INFRASTRUCTURE

### OpenSearch Alerting
* Add Integtest.sh for OpenSearch integtest setups ([#121](https://github.com/opensearch-project/alerting/pull/121))
* Fix snapshot build and increment to 1.1.0 ([#142](https://github.com/opensearch-project/alerting/pull/142))


### OpenSearch Anomaly Detection
* add deprecated detector type for bwc; add more test cases for historical analysis ([#197](https://github.com/opensearch-project/anomaly-detection/pull/197))
* Bump OpenSearch core to 1.1 in CI ([#212](https://github.com/opensearch-project/anomaly-detection/pull/212))


### OpenSearch Anomaly Detection Dashboards
* Bump plugin version to 1.1.0.0 ([#82](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/82))


### OpenSearch Asynchronous Search
* Fix snapshot build and increment to 1.1.0 ([#31](https://github.com/opensearch-project/asynchronous-search/pull/31))


### OpenSearch Cross Cluster Replication
* Add OpenSearch build script ([#119](https://github.com/opensearch-project/cross-cluster-replication/pull/119))
* Add basic github workflow for build and test ([#123](https://github.com/opensearch-project/cross-cluster-replication/pull/123))
* Modified github workflow to pick the latest changes ([#173](https://github.com/opensearch-project/cross-cluster-replication/pull/173))


### OpenSearch Dashboards Notebooks
* Fix snapshot build and depend on OpenSearch 1.1. ([#62](https://github.com/opensearch-project/dashboards-notebooks/pull/62))
* Bump opensearch ref to 1.1 in CI ([#73](https://github.com/opensearch-project/dashboards-notebooks/pull/73))


### OpenSearch Dashboards Reports
* Bump opensearch ref to 1.1 in CI ([#155](https://github.com/opensearch-project/dashboards-reports/pull/155))


### OpenSearch Dashboards Visualizations
* Auto dump cypress test data ([#23](https://github.com/opensearch-project/dashboards-visualizations/pull/23))


### OpenSearch Index Management
* Upgrade dependencies to 1.1 and build snapshot by default. ([#121](https://github.com/opensearch-project/index-management/pull/121))
* Update workflow to point to 1.1 ([#146](https://github.com/opensearch-project/index-management/pull/146))


### OpenSearch Job Scheduler
* Using 1.1 snapshot version for OpenSearch ([#48](https://github.com/opensearch-project/job-scheduler/pull/48))
* Use standard snapshot build settings and OpenSearch 1.x. ([#49](https://github.com/opensearch-project/job-scheduler/pull/49))


### OpenSearch k-NN
* Fix snapshot build, build against OpenSearch 1.1 ([#79](https://github.com/opensearch-project/k-NN/pull/79))


### OpenSearch Perftop
* Update version to 1.1 and add release notes ([#17](https://github.com/opensearch-project/perftop/pull/17))


### OpenSearch SQL
* Add Integtest.sh for OpenSearch integtest setups (workbench) ([#157](https://github.com/opensearch-project/sql/pull/157))
* Bump path-parse from 1.0.6 to 1.0.7 in /workbench ([#178](https://github.com/opensearch-project/sql/pull/178))
* Use externally-defined OpenSearch version when specified. ([#179](https://github.com/opensearch-project/sql/pull/179))
* Use OpenSearch 1.1 and build snapshot by default in CI. ([#181](https://github.com/opensearch-project/sql/pull/181))
* Workbench: remove curl commands in integtest.sh ([#200](https://github.com/opensearch-project/sql/pull/200))
* Bump opensearch ref to 1.1 in CI ([#205](https://github.com/opensearch-project/dashboards-reports/pull/205))


### OpenSearch Trace Analytics
* Add security support and auto dump test data for cypress ([#104](https://github.com/opensearch-project/trace-analytics/pull/104))


## DOCUMENTATION

### OpenSearch Alerting
* Update Bucket-Level Alerting RFC ([#145](https://github.com/opensearch-project/alerting/pull/145))


### OpenSearch Anomaly Detection
* Add themed logo to README ([#134](https://github.com/opensearch-project/anomaly-detection/pull/134))


### OpenSearch Anomaly Detection Dashboards
* Add themed logo ([#54](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/54))

### OpenSearch Cross Cluster Replication
* Add OpenSearch build script ([#119](https://github.com/opensearch-project/cross-cluster-replication/pull/119))
* Add basic github workflow for build and test ([#123](https://github.com/opensearch-project/cross-cluster-replication/pull/123))
* Modified github workflow to pick the latest changes ([#173](https://github.com/opensearch-project/cross-cluster-replication/pull/173))

### OpenSearch Dashboards Notebooks
* Update release notes for 1.1.0 release ([#71](https://github.com/opensearch-project/dashboards-notebooks/pull/71))


### OpenSearch Dashboards Visualizations
* Update copyright notice in readme ([#22](https://github.com/opensearch-project/dashboards-visualizations/pull/22))


### OpenSearch Index Management Dashboards Plugin
* Adding support to correctly set the dashboards and opensearch endpoint ([#33](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/33))
* Documentation url update ([#34](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/34))
* Add themed logo to README ([#37](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/37))


### OpenSearch Job Scheduler
* Add Getting Started to Readme ([#50](https://github.com/opensearch-project/job-scheduler/pull/50))


### OpenSearch Performance Analyzer
* Add themed logo to README ([#40](https://github.com/opensearch-project/performance-analyzer/pull/40))
* Fixes typo in APIs to enable PA batch metrics API in readme ([#42](https://github.com/opensearch-project/performance-analyzer/pull/42))


## MAINTENANCE

### OpenSearch Alerting
* Remove default assignee ([#127](https://github.com/opensearch-project/alerting/pull/127))


### OpenSearch Alerting Dashboards Plugin
* Commit the updated yarn lock to maintain consistency.  ([#26](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/26))
*  Add Integtest.sh for OpenSearch integtest setups ([#28](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/28))
* Allow for custom endpoints for cypress tests ([#29](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/29))
* Add Cypress tests for Bucket-Level Alerting ([#91](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/91))
* Update cypress-workflow.yml to use environment variable for OS and OS dashboard versions ([#96](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/96))
* Create opensearch-alerting-dashboards-plugin.release-notes-1.1.0.0.md ([#101](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/101))
* Update version in package.json ([#102](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/102)) 
* Update jest unit tests ([#112](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/112))


### OpenSearch Dashboards Notebooks
* Bump version for opensearch 1.1.0 release ([#70](https://github.com/opensearch-project/dashboards-notebooks/pull/70))


### OpenSearch Dashboards Visualizations
* Bump version for opensearch 1.1.0 release ([#24](https://github.com/opensearch-project/dashboards-visualizations/pull/24))


### OpenSearch Index Management
* License header check ([#142](https://github.com/opensearch-project/index-management/pull/142))


### OpenSearch Index Management Dashboards Plugin
* Provide host parameter in integtest.sh ([#73](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/73))


### OpenSearch Job Scheduler
* Bumping job-scheduler to build with OpenSearch(main) 1.1.0 ([#44](https://github.com/opensearch-project/job-scheduler/pull/44))


### OpenSearch Performance Analyzer
* Fix snapshot build, upgrade to OpenSearch 1.1 ([#55](https://github.com/opensearch-project/performance-analyzer-rca/pull/55))
* Add workflow for gauntlet tests and fix spotbug errors ([#63](https://github.com/opensearch-project/performance-analyzer-rca/pull/63))
* Update version and add release notes for 1.1.0.0 release ([#68](https://github.com/opensearch-project/performance-analyzer/pull/68))


### OpenSearch Perftop
* Bump path-parse from 1.0.6 to 1.0.7 ([#16](https://github.com/opensearch-project/perftop/pull/16))


### OpenSearch Security
* Upgrade OpenSearch version to 1.1.0 ([#1335](https://github.com/opensearch-project/security/pull/1335))
* Incremented version to 1.1.0.0-SNAPSHOT. ([#1429](https://github.com/opensearch-project/security/pull/1429))
* Remove alerting and ism indices from protected indices usage in sample configuration ([#1416](https://github.com/opensearch-project/security/pull/1416))
* Build against OpenSearch 1.1.0-SNAPSHOT. ([#1430](https://github.com/opensearch-project/security/pull/1430))
* Create release notes 1.1.0.0 ([#1440](https://github.com/opensearch-project/security/pull/1440))
* Switch opensearch from 1.x to 1.1 ([#1445](https://github.com/opensearch-project/security/pull/1445))


### OpenSearch Security Dashboards Plugin
* Bump version to 1.1.0.0 ([#823](https://github.com/opensearch-project/security-dashboards-plugin/pull/823))
* Build OpenSearch 1.1 branch in CI ([#827](https://github.com/opensearch-project/security-dashboards-plugin/pull/827))


### OpenSearch Trace Analytics
* Bump version for opensearch 1.1.0 release ([#105](https://github.com/opensearch-project/trace-analytics/pull/105))


## REFACTORING

### OpenSearch Alerting
* Refactor MonitorRunner ([#143](https://github.com/opensearch-project/alerting/pull/143))


### OpenSearch Performance Analyzer
* Addressing changes for StatsCollector ([#37](https://github.com/opensearch-project/performance-analyzer-rca/pull/37))
* Refactor stats collector ([#46](https://github.com/opensearch-project/performance-analyzer/pull/46))


