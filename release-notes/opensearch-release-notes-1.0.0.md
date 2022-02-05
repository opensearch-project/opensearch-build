# OpenSearch and Dashboards 1.0.0 Release Notes

## Release Highlights

Version 1.0 has multiple enhancements and fixes including span filtering support in Trace Analytics, tenant support in Notebooks, K-NN field level algorithm selection, support for index management transforms, and support for scheduling and tenants in reporting.

## Release Details

OpenSearch and Dashboards 1.0.0 includes the following OpenSearch Migration, features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.0.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.0.0.md).

## FEATURES

### Opensearch Index Management
* Adds support for Transform feature ([#17](https://github.com/opensearch-project/index-management/pull/17))


### Opensearch Index Management Dashboards Plugin
* Introducing transforms ([#16](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/16))
* Show data streams in 'Indices' and 'Managed Indices' sections ([#24](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/24))


### Opensearch k-NN
* Add support for L-inf distance in AKNN, custom scoring and painless scripting ([#315](https://github.com/opendistro-for-elasticsearch/k-NN/pull/315))
* Add support for inner product in ANN, custom scoring and painless ([#324](https://github.com/opendistro-for-elasticsearch/k-NN/pull/324))
* Refactor interface to support method configuration in field mapping ([#20](https://github.com/opensearch-project/k-NN/pull/20))


## ENHANCEMENTS

### Opensearch Alerting
* Adding check for security enabled ([#24](https://github.com/opensearch-project/alerting/pull/24))
* Adding Workflow to test the Security Integration tests with the Security Plugin Installed on Opensearch Docker Image ([#25](https://github.com/opensearch-project/alerting/pull/25))
* Adding Ktlint formatting check to the Gradle build task ([#26](https://github.com/opensearch-project/alerting/pull/26))
* Updating UTs for the Destination Settings ([#102](https://github.com/opensearch-project/alerting/pull/102))
* Adding additional null checks for URL not present ([#112](https://github.com/opensearch-project/alerting/pull/112))
* Enable license headers check ([118](https://github.com/opensearch-project/alerting/pull/118))


### Opensearch Anomaly Detection Dashboards
* Update sample data naming conventions ([#24](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/24))
* Update API call endpoints from _opendistro to _plugins ([#25](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/25))


### Opensearch Dashboards Notebooks
* Add sample notebooks ([#50](https://github.com/opensearch-project/dashboards-notebooks/pull/50))
* Memoize QueryDataGrid to Reduce Re-renders ([#49](https://github.com/opensearch-project/dashboards-notebooks/pull/49))
* Update placeholder for search bar to "Search notebook name" ([#42](https://github.com/opensearch-project/dashboards-notebooks/pull/42))
* Add output only parameter to Context Menu Base URL ([#18](https://github.com/opensearch-project/dashboards-notebooks/pull/18))
* Add Query Parameter for Selected View ([#17](https://github.com/opensearch-project/dashboards-notebooks/pull/17))


### Opensearch Dashboards Reports
* Use output_only parameter for notebook reports ([#32](https://github.com/opensearch-project/dashboards-reports/pull/32))
* Add Logic to Auto-populate Notebooks from Context menu ([#30](https://github.com/opensearch-project/dashboards-reports/pull/30))
* [Query Builder] Correctly handle matched phrases when a single value is specified or when the match phrases is negated ([#33](https://github.com/opensearch-project/dashboards-reports/pull/33))
* Replace osd header in context menu ([#37](https://github.com/opensearch-project/dashboards-reports/pull/37))
* Remove visualization editor in visualization reports ([#50](https://github.com/opensearch-project/dashboards-reports/pull/50))
* Increase chromium timeout to 100s ([#58](https://github.com/opensearch-project/dashboards-reports/pull/58))
* configure index setting to have default 1 replica and upper bound 2 ([#52](https://github.com/opensearch-project/dashboards-reports/pull/52))
* Add i18n translation support ([#82](https://github.com/opensearch-project/dashboards-reports/pull/82))
* PDF report is no more a screenshot, increasing the overall quality ([#82](https://github.com/opensearch-project/dashboards-reports/pull/82))
* Change Delivery Request Body for Notifications ([#85](https://github.com/opensearch-project/dashboards-reports/pull/85))
* Remove legacy notifications/delivery related code ([#94](https://github.com/opensearch-project/dashboards-reports/pull/94))


### Opensearch Index Management
* Improve integration with data streams ([#13](https://github.com/opensearch-project/index-management/pull/13))
* Skip rollover on non-write indices ([#88](https://github.com/opensearch-project/index-management/pull/88))


### Opensearch Index Management Dashboards Plugin
* Support edit transformation name ([#27](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/27))


### Opensearch k-NN
* Change mode for jni arrays release to prevent unnecessary copy backs ([#317](https://github.com/opendistro-for-elasticsearch/k-NN/pull/317))
* Update minimum score to 0. ([#318](https://github.com/opendistro-for-elasticsearch/k-NN/pull/318))
* Expose getValue method from KNNScriptDocValues ([#339](https://github.com/opendistro-for-elasticsearch/k-NN/pull/339))
* Add extra place to increase knn graph query errors ([#26](https://github.com/opensearch-project/k-NN/pull/26))


### Opensearch Performance Analyzer
* Add CONFIG_DIR_NOT_FOUND in StatExceptionCode ([#11](https://github.com/opensearch-project/performance-analyzer-rca/pull/11))


### Opensearch PerfTop
* Add env.js to store global property ([#10](https://github.com/opensearch-project/perftop/pull/10))


### Opensearch Security
* Allow attempt to load security config in case of plugin restart even if security index already exists ([#1154](https://github.com/opensearch-project/security/pull/1154))
* Allowing granular access for data-stream related transport actions ([#1170](https://github.com/opensearch-project/security/pull/1170))
* Introducing passive_intertransport_auth to facilitate communication between nodes with adv sec enabled and nodes without adv sec enabled. ([#1156](https://github.com/opensearch-project/security/pull/1156))
* Add static action group for managing data streams ([#1258](https://github.com/opensearch-project/security/pull/1258))


### Opensearch Security Dashboards Plugin
* Adding data-stream related permissions ([#784](https://github.com/opensearch-project/security-dashboards-plugin/pull/784))
* Align with conventions ([#789](https://github.com/opensearch-project/security-dashboards-plugin/pull/789))
* add svg content ([#766](https://github.com/opensearch-project/security-dashboards-plugin/pull/766))
* Changes regarding the anonymous auth flow ([#768](https://github.com/opensearch-project/security-dashboards-plugin/pull/768))


### Opensearch SQL
* Support querying a data stream ([#56](https://github.com/opensearch-project/sql/pull/56))


## BUG FIXES

### Opensearch Alerting Dashboards Plugin
* Update .opensearch_dashboards-plugin-helpers.json ([#8](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/8))
* Fix AD backend name to opensearch-anomaly-detection ([#9](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/9))
* Remove validation constraints for characters used in the Date Math ([#18](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/18))
* Fixed an issue preventing emails from being added to an email group using the Kibana interface ([#24](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/24))


### Opensearch Dashboards Notebooks
* Remove dependency on dashboards version for requests ([#48](https://github.com/opensearch-project/dashboards-notebooks/pull/48))
* Bump prismjs from 1.23.0 to 1.24.0 in /dashboards-notebooks ([#44](https://github.com/opensearch-project/dashboards-notebooks/pull/44))
* Fix error message when paragraph exceeds max_payload ([#40](https://github.com/opensearch-project/dashboards-notebooks/pull/40))
* Update glob-parent dependency ([#35](https://github.com/opensearch-project/dashboards-notebooks/pull/35))
* Fix dashboards index name ([#31](https://github.com/opensearch-project/dashboards-notebooks/pull/31))
* Address UX Fixes and hidden columns bug ([#30](https://github.com/opensearch-project/dashboards-notebooks/pull/30))
* Fix run all paragraphs for visualizations ([#20](https://github.com/opensearch-project/dashboards-notebooks/pull/20))


### Opensearch Dashboards Reports
* Configure index to have default one replica and upper bound 2 ([#62](https://github.com/opensearch-project/dashboards-reports/pull/62))
* Fix case-sensitive directory name for chromium zip ([#35](https://github.com/opensearch-project/dashboards-reports/pull/35))
* Add condition to fix negative value display ([#51](https://github.com/opensearch-project/dashboards-reports/pull/51))
* Fix csv parsing function ([#53](https://github.com/opensearch-project/dashboards-reports/pull/53))
* Revert .opensearch_dashboards index references to .kibana ([#67](https://github.com/opensearch-project/dashboards-reports/pull/67))
* Bump ws from 7.3.1 to 7.4.6 in /dashboards-reports ([#68](https://github.com/opensearch-project/dashboards-reports/pull/68))
* Better support sorting for csv report based on saved search ([#86](https://github.com/opensearch-project/dashboards-reports/pull/86))
* bump dependency version ([#101](https://github.com/opensearch-project/dashboards-reports/pull/101))
* fix failed cypress integ-testing ([#106](https://github.com/opensearch-project/dashboards-reports/pull/106))
* Fix notebooks context menu ([#109](https://github.com/opensearch-project/dashboards-reports/pull/109))
* Update context menu download request body after schema change ([#115](https://github.com/opensearch-project/dashboards-reports/pull/115))
* Exclude time range from report details for Notebooks ([#117](https://github.com/opensearch-project/dashboards-reports/pull/117))


### Opensearch Dashboards Visualizations
* Bump glob-parent from 5.1.1 to 5.1.2 in /gantt-chart ([#14](https://github.com/opensearch-project/dashboards-visualizations/pull/14))


### Opensearch Index Management
* Fix 7.10 rollover blocking thread issue ([#70](https://github.com/opensearch-project/index-management/pull/70))
* Fix issue with Rollup start/stop API ([#79](https://github.com/opensearch-project/index-management/pull/79))
* Fix to support custom source index type in Rollup jobs ([#4](https://github.com/opensearch-project/index-management/pull/4)) 


### Opensearch Index Management Dashboards Plugin
* Rename plugin helper file ([#11](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/11))
* Transform feature cleanup and bug fixes ([#20](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/20))
* Rollup bugfix ([#25](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/25))
* Adding correct dropdown options for different fields in transforms ([#28](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/28))


### Opensearch Job Scheduler
* Correcting failure logging ([#35](https://github.com/opensearch-project/job-scheduler/pull/35))


### Opensearch k-NN
* Add equals and hashcode to KNNMethodContext MethodComponentContext ([#48](https://github.com/opensearch-project/k-NN/pull/48))
* Add dimension validation to ANN QueryBuilder ([#332](https://github.com/opendistro-for-elasticsearch/k-NN/pull/332))
* Change score normalization for negative raw scores ([#337](https://github.com/opendistro-for-elasticsearch/k-NN/pull/337))


### Opensearch Performance Analyzer
* Create conf directory if not exist to avoid NoSuchFile exceptions ([#9](https://github.com/opensearch-project/performance-analyzer/pull/9))
* Update docker artifact link ([#9](https://github.com/opensearch-project/performance-analyzer-rca/pull/9))
* Modify JVM gen tuning policy and update the Unit test ([#12](https://github.com/opensearch-project/performance-analyzer-rca/pull/12))
* Fix actions by legacy cluster endpoints ([#21](https://github.com/opensearch-project/performance-analyzer/pull/21))


### Opensearch Security
* Delay the security index initial bootstrap when the index is red ([#1153](https://github.com/opensearch-project/security/pull/1153))
* Remove redundant isEmpty check and incorrect string equals operator ([#1181](https://github.com/opensearch-project/security/pull/1181))
* Do not trim SAML roles ([#1207](https://github.com/opensearch-project/security/pull/1207))
* Replace opensearch class names with opendistro class names during serialization and restore them back during deserialization ([#1278](https://github.com/opensearch-project/security/pull/1278))


### Opensearch Security Dashboards Plugin
* Refactoring the redirect logic for anonymous auth, added new type ParsedUrlQueryParams ([#778](https://github.com/opensearch-project/security-dashboards-plugin/pull/778))
* Fixing JSON parsing in SAML for strings that contain '' character ([#749](https://github.com/opensearch-project/security-dashboards-plugin/pull/749))
* Fix login redirect ([#777](https://github.com/opensearch-project/security-dashboards-plugin/pull/777))


### Opensearch SQL
* Bug Fix: Enable legacy settings in new setting action ([#97](https://github.com/opensearch-project/sql/pull/97))
* Fix NPE for SHOW statement without filter ([#150](https://github.com/opensearch-project/sql/pull/150))


### Opensearch Trace Analytics
* Bump glob-parent from 5.1.1 to 5.1.2 ([#40](https://github.com/opensearch-project/trace-analytics/pull/40))
* Pick latest commits from opendistro trace analytics ([#13](https://github.com/opensearch-project/trace-analytics/pull/13))


## INFRASTRUCTURE

### Opensearch Alerting
* Upgrading the Ktlint Version and applying the formatting to the project ([#20](https://github.com/opensearch-project/alerting/pull/20))
* Upgrade google-java-format to 1.10.0 to pick guava v30 ([#115](https://github.com/opensearch-project/alerting/pull/115))


### Opensearch Alerting Dashboards Plugin
* Update formik version that uses a good version of lodash ([#20](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/20))


### Opensearch Anomaly Detection
* Update dependencies for opensearch ([#56](https://github.com/opensearch-project/anomaly-detection/pull/56))
* Update the AD version from beta1 to rc1. ([#62](https://github.com/opensearch-project/anomaly-detection/pull/62))
* Add broken link check workflow ([#103](https://github.com/opensearch-project/anomaly-detection/pull/103))
* Bump plugin version to 1.0.0.0 ([#110](https://github.com/opensearch-project/anomaly-detection/pull/110))


### Opensearch Anomaly Detection Dashboards
* Fix CI workflows; change to run against PR ([#29](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/29))
* Bump plugin version to 1.0.0.0-rc1 ([#32](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/32))
* Add broken link check workflow ([#37](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/37))
* Rename default zip to anomaly-detection-dashboards ([#41](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/41))
* Bump to version 1.0.0.0 ([#45](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/45))


### Opensearch Asynchronous Search
* Update dependencies for opensearch and update the version from beta1 to rc1([#14](https://github.com/opensearch-project/asynchronous-search/pull/14))
* Bump plugin version to 1.0.0.0 ([#22](https://github.com/opensearch-project/asynchronous-search/pull/22))


### Opensearch Common Utils
  * Support for kotlin and JUnit5 with mockito ([#29](https://github.com/opensearch-project/common-utils/pull/29))
  * Removing Kotlin Runtime library bundled into library ([#30](https://github.com/opensearch-project/common-utils/pull/30))
  * Bump to version 1.0.0.0 #34 ([#34](https://github.com/opensearch-project/common-utils/pull/34))


### Opensearch Dashboards Notebooks
* Update testDistribution to fix CI ([#43](https://github.com/opensearch-project/dashboards-notebooks/pull/43))
* Update workflow to rename artifact in kebab case ([#41](https://github.com/opensearch-project/dashboards-notebooks/pull/41))
* Remove checking toasts in cypress ([#34](https://github.com/opensearch-project/dashboards-notebooks/pull/34))
* Add more delay for cypress when running sql ([#21](https://github.com/opensearch-project/dashboards-notebooks/pull/21))


### Opensearch Dashboards Reports
* Update issue template with multiple labels ([#36](https://github.com/opensearch-project/dashboards-reports/pull/36))
* Bump path-parse version to 1.0.7 to address CVE ([#59](https://github.com/opensearch-project/dashboards-reports/pull/59))
* Update README CoC Link ([#56](https://github.com/opensearch-project/dashboards-reports/pull/56))
* Remove dependency on demo.elastic and use local mock html for testing ([#100](https://github.com/opensearch-project/dashboards-reports/pull/100))
* Add code cov back ([#98](https://github.com/opensearch-project/dashboards-reports/pull/98))
* update workflow to rename artifact in kebab case ([#102](https://github.com/opensearch-project/dashboards-reports/pull/102))
* Bump test resource(job-scheduler) to 1.0.0.0 ([#105](https://github.com/opensearch-project/dashboards-reports/pull/105))
* Bump node version, fix workflow and gradle build ([#108](https://github.com/opensearch-project/dashboards-reports/pull/108))


### Opensearch Dashboards Visualizations
* Add unit tests and codecov ([#19](https://github.com/opensearch-project/dashboards-visualizations/pull/19))


### Opensearch Index Management
* Update issue template with multiple labels ([#10](https://github.com/opensearch-project/index-management/pull/10))


### Opensearch k-NN
* Enabled automated license header checks ([#41](https://github.com/opensearch-project/k-NN/pull/41))
* Comment out flaky test ([#54](https://github.com/opensearch-project/k-NN/pull/54))
* Update OpenSearch upstream to 1.0.0 ([#58](https://github.com/opensearch-project/k-NN/pull/58))


### Opensearch Performance Analyzer
* Upgrade Jackson version to 2.11.4 ([#13](https://github.com/opensearch-project/performance-analyzer/pull/13))
* Upgrade Jackson version to 2.11.4 ([#15](https://github.com/opensearch-project/performance-analyzer-rca/pull/15))
* Update version to rc1 ([#16](https://github.com/opensearch-project/performance-analyzer/pull/16))
* Update to rc1 version and opendistro links ([#17](https://github.com/opensearch-project/performance-analyzer-rca/pull/17))
* Enabled automated license header checks ([#22](https://github.com/opensearch-project/performance-analyzer/pull/22))
* Standardize processes across all plugins - Checklist items ([#26](https://github.com/opensearch-project/performance-analyzer/pull/26))
* Standardize processes across all plugins - Checklist items ([#22](https://github.com/opensearch-project/performance-analyzer-rca/pull/22))


### Opensearch PerfTop
* Update version to rc1 ([#10](https://github.com/opensearch-project/perftop/pull/10))
* Standardize processes across all plugins - Checklist items ([#13](https://github.com/opensearch-project/perftop/pull/13))


### Opensearch SQL
* Bump glob-parent from 5.1.1 to 5.1.2 in /workbench ([#125](https://github.com/opensearch-project/sql/pull/125))


### Opensearch Trace Analytics
* Add codecov ([#60](https://github.com/opensearch-project/trace-analytics/pull/60))


## DOCUMENTATION

### Opensearch Alerting
* Update issue template with multiple labels ([#13](https://github.com/opensearch-project/alerting/pull/13))
* Update and add documentation files ([#117](https://github.com/opensearch-project/alerting/pull/117))


### Opensearch Alerting Dashboards Plugin
* Update issue template with multiple labels ([#11](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/11))
* Update and add documentation files ([#21](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/21))


### Opensearch Anomaly Detection
* Update and add documentation files ([#105](https://github.com/opensearch-project/anomaly-detection/pull/105))


### Opensearch Anomaly Detection Dashboards
* Update doc links to point to OpenSearch ([#30](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/30))
* Update and add documentation files ([#38](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/38))


### Opensearch Common Utils
  * Update OpenSearch branch to 1.0 ([#28](https://github.com/opensearch-project/common-utils/pull/28)) 
  * Cleanup READMEs. ([#32](https://github.com/opensearch-project/common-utils/pull/32))


### Opensearch Dashboards Notebooks
* Update dependency versions and release notes ([#47](https://github.com/opensearch-project/dashboards-notebooks/pull/47))
* Level up markdown content and add link checker workflow ([#37](https://github.com/opensearch-project/dashboards-notebooks/pull/37))
* Add release notes for version 1.0.0.0 ([#46](https://github.com/opensearch-project/dashboards-notebooks/pull/46))


### Opensearch Dashboards Reports
* Add diagrams for integration with Notifications plugin ([#75](https://github.com/opensearch-project/dashboards-reports/pull/75))
* Add Notifications to docs ([#87](https://github.com/opensearch-project/dashboards-reports/pull/87))
* level up markdowns and readme ([#97](https://github.com/opensearch-project/dashboards-reports/pull/97))


### Opensearch Dashboards Visualizations
* Level up markdown contents ([#16](https://github.com/opensearch-project/dashboards-visualizations/pull/16))


### Opensearch Index Management Dashboards Plugin
* Update issue template with multiple labels ([#12](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/12))


### Opensearch Job Scheduler
  * Update issue template with multiple labels ([#21](https://github.com/opensearch-project/job-scheduler/pull/21))


### Opensearch k-NN
* Update template files ([#50](https://github.com/opensearch-project/k-NN/pull/50))
* Include codecov badge ([#52](https://github.com/opensearch-project/k-NN/pull/52))


### Opensearch Performance Analyzer
* Update rest endpoint names in README ([#15](https://github.com/opensearch-project/performance-analyzer/pull/15))


### Opensearch PerfTop
* Update issue template with multiple labels([#7](https://github.com/opensearch-project/perftop/pull/7))
* Update OpenSearch documents link ([#9](https://github.com/opensearch-project/perftop/pull/9))
* Update REST endpoint in document ([#10](https://github.com/opensearch-project/perftop/pull/10))
* Add opensearch-perftop 1.0.0.0-rc1 release note ([#11](https://github.com/opensearch-project/perftop/pull/11))


### Opensearch SQL
* Migrate SQL/PPL, JDBC, ODBC docs to OpenSearch ([#68](https://github.com/opensearch-project/sql/pull/68))
* Level up README markdown ([#148](https://github.com/opensearch-project/sql/pull/148))


### Opensearch Trace Analytics
* Level up markdown contents ([#57](https://github.com/opensearch-project/trace-analytics/pull/57))


## MAINTENANCE

### Opensearch Alerting
* Adding Rest APIs Backward Compatibility with ODFE ([#16](https://github.com/opensearch-project/alerting/pull/16))
* Moving the ODFE Settings to Legacy Settings and adding the new settings compatible with Opensearch ([#18](https://github.com/opensearch-project/alerting/pull/18))


### Opensearch Anomaly Detection
* Renaming RestAPIs while supporting backwards compatibility. ([#35](https://github.com/opensearch-project/anomaly-detection/pull/35))
* Rename namespaces from opendistro to opensearch. ([#43](https://github.com/opensearch-project/anomaly-detection/pull/43))
* update the AD settings for opensearch. ([#47](https://github.com/opensearch-project/anomaly-detection/pull/47))
* Update several minor things from opendistro to opensearch ([#57](https://github.com/opensearch-project/anomaly-detection/pull/57))


### Opensearch Asynchronous Search
* Renaming RestAPIs while supporting backwards compatibility. ([#9](https://github.com/opensearch-project/asynchronous-search/pull/9))
* Rename namespaces from opendistro to opensearch. ([#12](https://github.com/opensearch-project/asynchronous-search/pull/12))
* update the settings for opensearch. ([#13](https://github.com/opensearch-project/asynchronous-search/pull/13))


### Opensearch Dashboards Notebooks
* Bump version to 1.0.0.0 ([#45](https://github.com/opensearch-project/dashboards-notebooks/pull/45))


### Opensearch Dashboards Reports
* Bump OpenSearch Dashboards version to 1.0 ([#64](https://github.com/opensearch-project/dashboards-reports/pull/64))
* Bump to version 1.0.0.0 ([#103](https://github.com/opensearch-project/dashboards-reports/pull/103))


### Opensearch Dashboards Visualizations
* Bump version to 1.0.0.0 and add release notes ([#20](https://github.com/opensearch-project/dashboards-visualizations/pull/20))


### Opensearch Index Management
* Renaming Namespaces ([#14](https://github.com/opensearch-project/index-management/pull/14))
* Rest APIs Backward Compatibility ([#15](https://github.com/opensearch-project/index-management/pull/15))
* Settings Backwards Compatibility ([#16](https://github.com/opensearch-project/index-management/pull/16))
* Point to correct version of notification ([#18](https://github.com/opensearch-project/index-management/pull/18))
* Enable security plugin integrated tests ([#93](https://github.com/opensearch-project/index-management/pull/93))


### Opensearch Index Management Dashboards Plugin
* CVE fix ([#29](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/29))


### Opensearch Job Scheduler
  * Rename settings from OpenDistro and OpenSearch, with backwards compatibility, using fallback ([#20](https://github.com/opensearch-project/job-scheduler/pull/20))


### Opensearch Performance Analyzer
* Modify printing stacktrace to logger instead of stdout ([#10](https://github.com/opensearch-project/performance-analyzer-rca/pull/10))
* Modify namespace from opendistro to opensearch ([#12](https://github.com/opensearch-project/performance-analyzer/pull/12))
* Modify namespace to opensearch ([#14](https://github.com/opensearch-project/performance-analyzer-rca/pull/14))
* Update REST resources to follow new OpenSearch naming convention ([#14](https://github.com/opensearch-project/performance-analyzer/pull/14))
* Replace references to /_opendistro with /_plugins ([#16](https://github.com/opensearch-project/performance-analyzer-rca/pull/16))
* Add legacy REST endpoints to integration tests ([#17](https://github.com/opensearch-project/performance-analyzer/pull/17))
* Create HTTP contexts for legacy resource name ([#18](https://github.com/opensearch-project/performance-analyzer-rca/pull/18))
* Add backward compatible resource names to RcaController ([#19](https://github.com/opensearch-project/performance-analyzer-rca/pull/19))
* Update licenses sha and add release notes ([#18](https://github.com/opensearch-project/performance-analyzer/pull/18))
* Update upstream dependency and README ([#21](https://github.com/opensearch-project/performance-analyzer-rca/pull/21))
* Update version from 1.0.0.0-rc1 to 1.0.0.0 ([#24](https://github.com/opensearch-project/performance-analyzer-rca/pull/24))
* Update OS upstream version and add release notes for 1.0.0.0 release ([#32](https://github.com/opensearch-project/performance-analyzer/pull/32))


### Opensearch PerfTop
* Upgrade the version of vulnerable dependencies ([#8](https://github.com/opensearch-project/perftop/pull/8))
* Add REST API backward compatibility ([#10](https://github.com/opensearch-project/perftop/pull/10))
* Bump glob-parent from 5.1.1 to 5.1.2 ([#12](https://github.com/opensearch-project/perftop/pull/12))
* Update OS upstream version and add release notes for 1.0.0.0 release ([#14](https://github.com/opensearch-project/perftop/pull/14))


### Opensearch Security
* Bump commons-io from 2.6 to 2.7 ([#1137](https://github.com/opensearch-project/security/pull/1137))
* Update issue template with multiple labels ([#1164](https://github.com/opensearch-project/security/pull/1164))
* move issue templates to ISSUE_TEMPLATE ([#1166](https://github.com/opensearch-project/security/pull/1166))
* Rename kibana substrings with OpenSearchDashboards in class name, method name and comments ([#1160](https://github.com/opensearch-project/security/pull/1160))
* Rename 'Open Distro' to follow open search naming convention ([#1149](https://github.com/opensearch-project/security/pull/1149))
* Build plugin on top of 1.x branch of OpenSearch core ([#1174](https://github.com/opensearch-project/security/pull/1174))
* Add build.version_qualifier and make security plugin compatible with OpenSearch 1.0.0-rc1 ([#1179](https://github.com/opensearch-project/security/pull/1179))
* Update anchor link for documentation and apply opensearch-security naming convention in PR template ([#1180](https://github.com/opensearch-project/security/pull/1180))
* Force the version of json-path 2.4.0 ([#1175](https://github.com/opensearch-project/security/pull/1175))
* Bump version to rc1, create release notes and fix the url used in release notes drafter ([#1186](https://github.com/opensearch-project/security/pull/1186))
* Rename settings constant value and related testing yml files for migration to Opensearch ([#1184](https://github.com/opensearch-project/security/pull/1184))
* Remove prefix "OPENDISTRO_" for identifier for settings ([#1185](https://github.com/opensearch-project/security/pull/1185))
* Rename documents and demo for settings ([#1188](https://github.com/opensearch-project/security/pull/1188))
* Add fallback for opendistro_security_config.ssl_dual_mode_enabled ([#1190](https://github.com/opensearch-project/security/pull/1190))
* Change security plugin REST API to support both opensearch and opendistro routes ([#1172](https://github.com/opensearch-project/security/pull/1172))
* Fix CODEOWNERS file ([#1193](https://github.com/opensearch-project/security/pull/1193))
* Dashboards rename related changes ([#1192](https://github.com/opensearch-project/security/pull/1192))
* Build OpenSearch 1.0 branch on CI ([#1189](https://github.com/opensearch-project/security/pull/1189))
* Fix install_demo_configuration.sh ([#1211](https://github.com/opensearch-project/security/pull/1211))
* Move AdvancedSecurityMigrationTests.java to opensearch directory ([#1255](https://github.com/opensearch-project/security/pull/1255))
* upgrade CXF to v3.4.3 ([#1210](https://github.com/opensearch-project/security/pull/1210))
* Bump httpclient version from 4.5.3 to 4.5.13 ([#1257](https://github.com/opensearch-project/security/pull/1257))
* Cleanup md files ([#1298](https://github.com/opensearch-project/security/pull/1298))
* Upgrade json-smart from 2.4.2 to 2.4.7 ([#1299](https://github.com/opensearch-project/security/pull/1299))
* Bump version to 1.0.0.0 and create release notes ([#1303](https://github.com/opensearch-project/security/pull/1303))
* Build on OpenSearch 1.0.0 ([#1304](https://github.com/opensearch-project/security/pull/1304))
* Consolidate the release notes for RC1 and GA ([#1305](https://github.com/opensearch-project/security/pull/1305))


### Opensearch Security Dashboards Plugin
* Remove rc1 postfixes ([#791](https://github.com/opensearch-project/security-dashboards-plugin/pull/791))
* move issue templates to ISSUE_TEMPLATE ([#758](https://github.com/opensearch-project/security-dashboards-plugin/pull/758))
* Update issue template with multiple labels ([#756](https://github.com/opensearch-project/security-dashboards-plugin/pull/756))
* Naming convention change in repo ([#764](https://github.com/opensearch-project/security-dashboards-plugin/pull/764))
* Point document links to opensearch.org ([#763](https://github.com/opensearch-project/security-dashboards-plugin/pull/763))
* Create release notes for rc-1 and Bump version to 1.0.0.0-rc1 ([#771](https://github.com/opensearch-project/security-dashboards-plugin/pull/771))
* Point OpenSearch Dashboards to to new back end APIs ([#770](https://github.com/opensearch-project/security-dashboards-plugin/pull/770))
* Change the titles of release notes ([#772](https://github.com/opensearch-project/security-dashboards-plugin/pull/772))
* Update ga release notes with rc1 PRs [#797](https://github.com/opensearch-project/security-dashboards-plugin/pull/797)


### Opensearch Trace Analytics
* Bump version to 1.0.0.0 and add release notes ([#61](https://github.com/opensearch-project/trace-analytics/pull/61))


## REFACTORING

### Opensearch Alerting
* Rename namespaces from com.amazon.opendistroforelasticsearch to org.opensearch ([#15](https://github.com/opensearch-project/alerting/pull/15))


### Opensearch Alerting Dashboards Plugin
* Update API, settings, and doc link renaming ([#14](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/14))


### Opensearch Index Management Dashboards Plugin
* Update API, settings, and doc link renaming ([#15](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/15))


### Opensearch Job Scheduler
  * Change plugin setting name from 'opensearch.' to 'pluigns.' ([#27](https://github.com/opensearch-project/job-scheduler/pull/27))
  * Rename namespaces from odfe to opensearch ([#24](https://github.com/opensearch-project/job-scheduler/pull/24))
  * Change path of REST APIs for 'Sample Extension Plugin' and naming convension in filename and comments ([#25](https://github.com/opensearch-project/job-scheduler/pull/25))
  * Rename other identifiers from opendistro or elasticsearch to OpenSearch ([#28](https://github.com/opensearch-project/job-scheduler/pull/28))


### Opensearch k-NN
* Renaming RestAPIs while supporting backwards compatibility. ([#18](https://github.com/opensearch-project/k-NN/pull/18))
* Rename namespace from opendistro to opensearch ([#21](https://github.com/opensearch-project/k-NN/pull/21))
* Move constants out of index folder into common ([#320](https://github.com/opendistro-for-elasticsearch/k-NN/pull/320))
* Expose inner_product space type, refactoring SpaceTypes ([#328](https://github.com/opendistro-for-elasticsearch/k-NN/pull/328))


