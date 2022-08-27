# OpenSearch and Dashboards 1.0.0-rc1 Release Notes

## Release Highlights
This Release Candidate is a version of the project that is feature complete and passing automated testing with the intent to validate expected functionality before moving to a General Availability (GA) launch. There are multiple enhancements and fixes that are part of this release including span filtering support in Trace Analytics, tenant support in Notebooks, K-NN field level algorithm selection, support for index management transforms, and support for scheduling and tenants in reporting.

## Release Details

OpenSearch and Dashboards 1.0.0-rc1 includes the following OpenSearch Migration, features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

## FEATURES

### Opensearch Index Management
* Adds support for Transform feature ([#17](https://github.com/opensearch-project/index-management/pull/17))


### Opensearch Index Management Dashboards Plugin
* Introducing transforms ([#16](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/16))


### Opensearch k-NN
* Refactor interface to support method configuration in field mapping ([#20](https://github.com/opensearch-project/k-NN/pull/20))


## ENHANCEMENTS

### Opensearch Anomaly Detection Dashboards
* Update sample data naming conventions ([#24](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/24))
* Update API call endpoints from _opendistro to _plugins ([#25](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/25))


### Opensearch Dashboards Notebooks
* Add output only parameter to Context Menu Base URL ([#18](https://github.com/opensearch-project/dashboards-notebooks/pull/18))
* Add Query Parameter for Selected View ([#17](https://github.com/opensearch-project/dashboards-notebooks/pull/17))


### Opensearch Dashboards Notebooks
* Add output only parameter to Context Menu Base URL ([#18](https://github.com/opensearch-project/dashboards-notebooks/pull/18))
* Add Query Parameter for Selected View ([#17](https://github.com/opensearch-project/dashboards-notebooks/pull/17))


### Opensearch Dashboards Reports
* Use output_only parameter for notebook reports ([#32](https://github.com/opensearch-project/dashboards-reports/pull/32))
* Add Logic to Auto-populate Notebooks from Context menu ([#30](https://github.com/opensearch-project/dashboards-reports/pull/30))
* [Query Builder] Correctly handle matched phrases when a single value is specified or when the match phrases is negated ([#33](https://github.com/opensearch-project/dashboards-reports/pull/33))
* Replace osd header in context menu ([#37](https://github.com/opensearch-project/dashboards-reports/pull/37))
* Remove visualization editor in visualization reports ([#50](https://github.com/opensearch-project/dashboards-reports/pull/50))
* Increase chromium timeout to 100s ([#58](https://github.com/opensearch-project/dashboards-reports/pull/58))


### Opensearch Index Management
* Improve integration with data streams ([#13](https://github.com/opensearch-project/index-management/pull/13))


### Opensearch k-NN
* Add extra place to increase k-NN graph query errors ([#26](https://github.com/opensearch-project/k-NN/pull/26))


### Opensearch Performance Analyzer
* Add CONFIG_DIR_NOT_FOUND in StatExceptionCode ([#11](https://github.com/opensearch-project/performance-analyzer-rca/pull/11))


### Opensearch Perftop
* Add env.js to store global property ([#10](https://github.com/opensearch-project/perftop/pull/10))


### Opensearch Security
* Allow attempt to load security config in case of plugin restart even if security index already exists ([#1154](https://github.com/opensearch-project/security/pull/1154))
* Allowing granular access for data-stream related transport actions ([#1170](https://github.com/opensearch-project/security/pull/1170))


### Opensearch Security Dashboards Plugin
* Add svg content ([#766](https://github.com/opensearch-project/security-dashboards-plugin/pull/766))
* Changes regarding the anonymous auth flow ([#768](https://github.com/opensearch-project/security-dashboards-plugin/pull/768))


## BUG FIXES

### Opensearch Alerting Dashboards Plugin
* Update .opensearch_dashboards-plugin-helpers.json ([#8](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/8))
* Fix AD backend name to opensearch-anomaly-detection ([#9](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/9))


### Opensearch Dashboards Notebooks
* Fix run all paragraphs for visualizations ([#20](https://github.com/opensearch-project/dashboards-notebooks/pull/20))


### Opensearch Dashboards Notebooks
* Fix run all paragraphs for visualizations ([#20](https://github.com/opensearch-project/dashboards-notebooks/pull/20))


### Opensearch Dashboards Reports
* Configure index to have default one replica and upper bound 2 ([#62](https://github.com/opensearch-project/dashboards-reports/pull/62))
* Fix case-sensitive directory name for chromium zip ([#35](https://github.com/opensearch-project/dashboards-reports/pull/35))
* Add condition to fix negative value display ([#51](https://github.com/opensearch-project/dashboards-reports/pull/51))
* Fix csv parsing function ([#53](https://github.com/opensearch-project/dashboards-reports/pull/53))


### Opensearch Index Management Dashboards Plugin
* Rename plugin helper file ([#11](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/11))


### Opensearch Performance Analyzer
* Create conf directory if not exist to avoid NoSuchFile exceptions ([#9](https://github.com/opensearch-project/performance-analyzer/pull/9))
* Update docker artifact link ([#9](https://github.com/opensearch-project/performance-analyzer-rca/pull/9))
* Modify JVM gen tuning policy and update the Unit test ([#12](https://github.com/opensearch-project/performance-analyzer-rca/pull/12))


### Opensearch Security
* Delay the security index initial bootstrap when the index is red ([#1153](https://github.com/opensearch-project/security/pull/1153))
* Remove redundant isEmpty check and incorrect string equals operator ([#1181](https://github.com/opensearch-project/security/pull/1181))


### Opensearch Security Dashboards Plugin
* Fixing JSON parsing in SAML for strings that contain '' character ([#749](https://github.com/opensearch-project/security-dashboards-plugin/pull/749))
* Fix login redirect ([#777](https://github.com/opensearch-project/security-dashboards-plugin/pull/777))


### Opensearch Trace Analytics
* Pick latest commits from opendistro trace analytics ([#13](https://github.com/opensearch-project/trace-analytics/pull/13))


## INFRASTRUCTURE

### Opensearch Alerting
* Upgrading the Ktlint Version and applying the formatting to the project ([#20](https://github.com/opensearch-project/alerting/pull/20))


### Opensearch Anomaly Detection
* Update dependencies for opensearch ([#56](https://github.com/opensearch-project/anomaly-detection/pull/56))
* Update the AD version from beta1 to rc1. ([#62](https://github.com/opensearch-project/anomaly-detection/pull/62))


### Opensearch Anomaly Detection Dashboards
* Fix CI workflows; change to run against PR ([#29](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/29))
* Bump plugin version to 1.0.0.0-rc1 ([#32](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/32))


### Opensearch Asynchronous Search
* Update dependencies for opensearch and update the version from beta1 to rc1([#14](https://github.com/opensearch-project/asynchronous-search/pull/14))


### Opensearch Dashboards Notebooks
* Add more delay for cypress when running sql ([#21](https://github.com/opensearch-project/dashboards-notebooks/pull/21))


### Opensearch Dashboards Notebooks
* Add more delay for cypress when running sql ([#21](https://github.com/opensearch-project/dashboards-notebooks/pull/21))


### Opensearch Dashboards Reports
* Update issue template with multiple labels ([#36](https://github.com/opensearch-project/dashboards-reports/pull/36))
* Bump path-parse version to 1.0.7 to address CVE ([#59](https://github.com/opensearch-project/dashboards-reports/pull/59))
* Update README CoC Link ([#56](https://github.com/opensearch-project/dashboards-reports/pull/56))


### Opensearch Index Management
* Update issue template with multiple labels ([#10](https://github.com/opensearch-project/index-management/pull/10))
  

### Opensearch k-NN
* Update upstream to use 1.0 ([#30](https://github.com/opensearch-project/k-NN/pull/30))


### Opensearch Performance Analyzer
* Upgrade Jackson version to 2.11.4 ([#13](https://github.com/opensearch-project/performance-analyzer/pull/13))
* Upgrade Jackson version to 2.11.4 ([#15](https://github.com/opensearch-project/performance-analyzer-rca/pull/15))
* Update version to rc1 ([#16](https://github.com/opensearch-project/performance-analyzer/pull/16))
* Update to rc1 version and opendistro links ([#17](https://github.com/opensearch-project/performance-analyzer-rca/pull/17))


### Opensearch Perftop
* Update version to rc1 ([#10](https://github.com/opensearch-project/perftop/pull/10))


## DOCUMENTATION

### Opensearch Alerting
* Update issue template with multiple labels ([#13](https://github.com/opensearch-project/alerting/pull/13))


### Opensearch Alerting Dashboards Plugin
* Update issue template with multiple labels ([#11](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/11))


### Opensearch Anomaly Detection Dashboards
* Update doc links to point to OpenSearch ([#30](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/30))


### Opensearch Common Utils
* Update issue template with multiple labels ([#18](https://github.com/opensearch-project/common-utils/pull/18))


### Opensearch Index Management Dashboards Plugin
* Update issue template with multiple labels ([#12](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/12))


### Opensearch Job Scheduler
* Update issue template with multiple labels ([#21](https://github.com/opensearch-project/job-scheduler/pull/21))


### Opensearch Performance Analyzer
* Update rest endpoint names in README ([#15](https://github.com/opensearch-project/performance-analyzer/pull/15))


### Opensearch Perftop
* Update issue template with multiple labels([#7](https://github.com/opensearch-project/perftop/pull/7))
* Update OpenSearch documents link ([#9](https://github.com/opensearch-project/perftop/pull/9))
* Update REST endpoint in document ([#10](https://github.com/opensearch-project/perftop/pull/10))


### Opensearch SQL
* Migrate SQL/PPL, JDBC, ODBC docs to OpenSearch ([#68](https://github.com/opensearch-project/sql/pull/68))


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


### Opensearch Index Management
* Renaming Namespaces ([#14](https://github.com/opensearch-project/index-management/pull/14))
* Rest APIs Backward Compatibility ([#15](https://github.com/opensearch-project/index-management/pull/15))
* Settings Backwards Compatibility ([#16](https://github.com/opensearch-project/index-management/pull/16))
* Point to correct version of notification ([#18](https://github.com/opensearch-project/index-management/pull/18))


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


### Opensearch Perftop
* Upgrade the version of vulnerable dependencies ([#8](https://github.com/opensearch-project/perftop/pull/8))
* Add REST API backward compatibility ([#10](https://github.com/opensearch-project/perftop/pull/10))


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


### Opensearch Security Dashboards Plugin
* move issue templates to ISSUE_TEMPLATE ([#758](https://github.com/opensearch-project/security-dashboards-plugin/pull/758))
* Update issue template with multiple labels ([#756](https://github.com/opensearch-project/security-dashboards-plugin/pull/756))
* Naming convention change in repo ([#764](https://github.com/opensearch-project/security-dashboards-plugin/pull/764))
* Point document links to opensearch.org ([#763](https://github.com/opensearch-project/security-dashboards-plugin/pull/763))
* Create release notes for rc-1 and Bump version to 1.0.0.0-rc1 ([#771](https://github.com/opensearch-project/security-dashboards-plugin/pull/771))
* Point OpenSearch Dashboards to to new back end APIs ([#770](https://github.com/opensearch-project/security-dashboards-plugin/pull/770))
* Change the titles of release notes ([#772](https://github.com/opensearch-project/security-dashboards-plugin/pull/772))


## REFACTORING

### Opensearch Alerting
* Rename namespaces from com.amazon.opendistroforelasticsearch to org.opensearch ([#15](https://github.com/opensearch-project/alerting/pull/15))


### Opensearch Alerting Dashboards Plugin
* Update API, settings, and doc link renaming ([#14](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/14))


### Opensearch Common Utils
* Rename namespaces from OpenDistro to OpenSearch ([#20](https://github.com/opensearch-project/common-utils/pull/20))
* Rename classes, variables, methods to incorporate OpenSearch ([#21](https://github.com/opensearch-project/common-utils/pull/21))
* Rename remaining identifiers to OpenSearch ([#23](https://github.com/opensearch-project/common-utils/pull/23))
* Rename consts as per changes in security plugin ([#25](https://github.com/opensearch-project/common-utils/pull/25))
* Move workflow tags to rc1 ([#26](https://github.com/opensearch-project/common-utils/pull/26))


### Opensearch Index Management Dashboards Plugin
* Update API, settings, and doc link renaming ([#15](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/15))


### Opensearch Job Scheduler
* Change plugin setting name from 'opensearch.' to 'plugins.' ([#27](https://github.com/opensearch-project/job-scheduler/pull/27))
* Rename namespaces from odfe to opensearch ([#24](https://github.com/opensearch-project/job-scheduler/pull/24))
* Change path of REST APIs for 'Sample Extension Plugin' and naming convension in filename and comments ([#25](https://github.com/opensearch-project/job-scheduler/pull/25))
* Rename other identifiers from opendistro or elasticsearch to OpenSearch ([#28](https://github.com/opensearch-project/job-scheduler/pull/28))


### Opensearch k-NN
* Renaming RestAPIs while supporting backwards compatibility. ([#18](https://github.com/opensearch-project/k-NN/pull/18))
* Rename namespace from opendistro to opensearch ([#21](https://github.com/opensearch-project/k-NN/pull/21))
