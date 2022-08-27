# OpenSearch and Dashboards 1.0.0-beta1 Release Notes

## Release Highlights
With this beta release, we have refactored all the Open Distro for Elasticsearch plugins to work with OpenSearch and provide the community with downloadable artifacts (Linux tars and Docker images) to run OpenSearch and OpenSearch Dashboards with these plugins installed. 

## Release Details
OpenSearch and Dashboards 1.0.0-beta1 includes the following OpenSearch Migration, features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

## OpenSearch Migration

### Opensearch SQL
* OpenSearch migration for JDBC driver ([#3](https://github.com/opensearch-project/sql/pull/3))
* OpenSearch Migration for SQL/PPL ([#2](https://github.com/opensearch-project/sql/pull/2))
* OpenSearch migration for ODBC driver ([#7](https://github.com/opensearch-project/sql/pull/7))
* Migrate workbench to OpenSearch Dashboards ([#6](https://github.com/opensearch-project/sql/pull/6))
* OpenSearch Readiness: SQL/PPL, JDBC, ODBC ([#8](https://github.com/opensearch-project/sql/pull/8))
* Opensearch migration for sql-cli and doctest module ([#4](https://github.com/opensearch-project/sql/pull/4))
* Remove CodeCov Usage ([#9](https://github.com/opensearch-project/sql/pull/9))
* Add license header to SQL/PPL, CLI, JDBC, ODBC ([#11](https://github.com/opensearch-project/sql/pull/11))
* Add License Headers to Workbench ([#10](https://github.com/opensearch-project/sql/pull/10))
* SQL/PPL API migration for OpenSearch ([#14](https://github.com/opensearch-project/sql/pull/14))
* SQL/PPL artifact renaming and version reset ([#15](https://github.com/opensearch-project/sql/pull/15))
* Change workbench version to 1.0.0, change api to _opensearch ([#17](https://github.com/opensearch-project/sql/pull/17))
* Migrate SQL/PPL to OpenSearch namespace ([#16](https://github.com/opensearch-project/sql/pull/16))
* Rename ODBC driver and DSN name ([#20](https://github.com/opensearch-project/sql/pull/20))
* Doctest/SQL-CLI API migration to OpenSearch, renaming and version reset ([#19](https://github.com/opensearch-project/sql/pull/19))
* Add release notes for OpenSearch 1.0.0.0-beta1 ([#21](https://github.com/opensearch-project/sql/pull/21))
* Build SQL/PPL against OpenSearch 1.0.0-alpha2 ([#22](https://github.com/opensearch-project/sql/pull/22))
* Build SQL/PPL against OpenSearch 1.0.0-beta1 ([#23](https://github.com/opensearch-project/sql/pull/23))
* Bump Workbench Version to Beta1 for OpenSearch Release ([#24](https://github.com/opensearch-project/sql/pull/24))

### Opensearch Notebooks Dashboards Plugin
* Migrate Notebooks frontend and backend plugin to OpenSearch ([#3](https://github.com/opensearch-project/dashboards-notebooks/pull/3))
* Change dashboards nav and pkgbuild.gradle to use OpenSearch ([#5](https://github.com/opensearch-project/dashboards-notebooks/pull/5))
* Add license header to all files ([#6](https://github.com/opensearch-project/dashboards-notebooks/pull/6))
* Change version to 1.0.0, change api to _opensearch ([#7](https://github.com/opensearch-project/dashboards-notebooks/pull/7))
* Migrate to OpenSearch Alpha2 ([#11](https://github.com/opensearch-project/dashboards-notebooks/pull/11))
* Update to Beta1 for OpenSearch Release ([#14](https://github.com/opensearch-project/dashboards-notebooks/pull/14))

### Opensearch Reports Dashboards Plugin
* Migrate reporting frontend plugin to OpenSearch Dashboards ([#4](https://github.com/opensearch-project/dashboards-reports/pull/4))
* [migration] Rename elasticsearch to opensearch for reports-scheduler ([#5](https://github.com/opensearch-project/dashboards-reports/pull/5))
* Change dashboards nav to use OpenSearch ([#6](https://github.com/opensearch-project/dashboards-reports/pull/6))
* Add license headers for OpenSearch ([#8](https://github.com/opensearch-project/dashboards-reports/pull/8))
* dashboards-reports version reset ([#23](https://github.com/opensearch-project/dashboards-reports/pull/23)) 
* [Migration] Reports-scheduler renaming, version reset, fix CI ([#22](https://github.com/opensearch-project/dashboards-reports/pull/22)) 
* [Migration] Build reporting against OpenSearch 1.0.0-alpha2 ([#25](https://github.com/opensearch-project/dashboards-reports/pull/25))
* Update opensearch version to 1.0.0 beta1 ([#26](https://github.com/opensearch-project/dashboards-reports/pull/26))

### Opensearch Trace Analytics
* Migrate trace analytics to OpenSearch Dashboards ([#1](https://github.com/opensearch-project/trace-analytics/pull/1))
* Change nav bar to use OpenSearch ([#2](https://github.com/opensearch-project/trace-analytics/pull/2))
* Add license headers for OpenSearch ([#3](https://github.com/opensearch-project/trace-analytics/pull/3))
* Change plugin versions to 1.0.0 ([#4](https://github.com/opensearch-project/trace-analytics/pull/4))
* Rebase commits from opendistro repo ([#5](https://github.com/opensearch-project/trace-analytics/pull/5))
* Bump Version to Beta1 for OpenSearch Release ([#7](https://github.com/opensearch-project/trace-analytics/pull/7))

### Opensearch Dashboards Visualizations
* Migrate gantt chart to OpenSearch Dashboards ([#1](https://github.com/opensearch-project/dashboards-visualizations/pull/1))
* Add license headers for OpenSearch ([#2](https://github.com/opensearch-project/dashboards-visualizations/pull/2))
* Change plugin versions to 1.0.0 ([#3](https://github.com/opensearch-project/dashboards-visualizations/pull/3))
* Bump version to beta1 for OpenSearch release ([#5](https://github.com/opensearch-project/dashboards-visualizations/pull/5))

## FEATURES

### Opensearch Cli
* Allow user to provide certificate path ([#6](https://github.com/opensearch-project/opensearch-cli/pull/6))


## ENHANCEMENTS

### Opensearch Index Management
* migrate plugin to be compatible with OpenSearch ([#1](https://github.com/opensearch-project/index-management/pull/1))
* rename plugin ([#5](https://github.com/opensearch-project/index-management/pull/5))

### Opensearch Alerting
* Update plugin install name ([#9](https://github.com/opensearch-project/alerting/pull/9))

### Opensearch Security
* Check and create multi-tenant index with alias for Update and Delete requests. Try to find a name for the multi-tenant index if index/alias with ".kibana_..._#" already exists ([#1058](https://github.com/opensearch-project/security/pull/1058))

### Opensearch Anomaly Detection Dashboards
* Migrate plugin to be compatible with OpenSearch Dashboards ([#1](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1))

### Opensearch Security Dashboards Plugin
* Save tenant selection by default and remove the checkbox ([#725](https://github.com/opensearch-project/security-dashboards-plugin/pull/725))
* Update list of permissions available in UI ([#740](https://github.com/opensearch-project/security-dashboards-plugin/pull/740))
* name change to opensearch dashboard ([#743](https://github.com/opensearch-project/security-dashboards-plugin/pull/743))


## BUG FIXES

### Opensearch Security
* [Fix][Usage][Hasher] wrong file reference hash.sh ([#1093](https://github.com/opensearch-project/security/pull/1093))


### Opensearch Security Dashboards Plugin
* Revert "Add opendistro/ism and rollup actions" ([#714](https://github.com/opensearch-project/security-dashboards-plugin/pull/714))
* Making sure SAML cookie uses saml session timeout value if it is available (([#715](https://github.com/opensearch-project/security-dashboards-plugin/pull/715))
* Making sure SAML cookie uses saml session timeout value if it is available ([#717](https://github.com/opensearch-project/security-dashboards-plugin/pull/717))
* Cherry-pick fix of saving tenant option from main to 7.9.1 branch ([#716](https://github.com/opensearch-project/security-dashboards-plugin/pull/716))
* Fix github integration test for 1.13.0.1 ([#723](https://github.com/opensearch-project/security-dashboards-plugin/pull/723))
* Updated logic for splitting SAML JWT token ([#730](https://github.com/opensearch-project/security-dashboards-plugin/pull/730))
* Updated logic for splitting SAML JWT token ([#731](https://github.com/opensearch-project/security-dashboards-plugin/pull/731))
* Fix ci and change artifact name ([#745](https://github.com/opensearch-project/security-dashboards-plugin/pull/745))
* fix text and remove svg content ([#751](https://github.com/opensearch-project/security-dashboards-plugin/pull/751))
* fix readme badge and audit log text ([#753](https://github.com/opensearch-project/security-dashboards-plugin/pull/753))

### Opensearch Alerting
* Update jackson CVE-2020-28491 ([#8](https://github.com/opensearch-project/alerting/pull/8))

## INFRASTRUCTURE

### Opensearch Index Management
* update github workflows ([#5](https://github.com/opensearch-project/index-management/pull/5))

### Opensearch Alerting
* Fix integ tests so they execute successfully in the test workflow ([#7](https://github.com/opensearch-project/alerting/pull/7))
* Fix Test Workflow ([#6](https://github.com/opensearch-project/alerting/pull/6))

### OpenSearch Common-utils
* Updated templates from .github ([#7](https://github.com/opensearch-project/common-utils/pull/7))
* Publish to maven local and add CI ([#8](https://github.com/opensearch-project/common-utils/pull/8))
* Update test workflow for alpha1 ([#9](https://github.com/opensearch-project/common-utils/pull/9))
* Update test workflow and publish beta1 ([#14](https://github.com/opensearch-project/common-utils/pull/14))

### Opensearch Asynchronous Search
* Adds templates for PR, bug report and feature request ([#5](https://github.com/opensearch-project/asynchronous-search/pull/5))
* Changes to use OpenSearch 1.0.0-alpha1 ([#6](https://github.com/opensearch-project/asynchronous-search/pull/6))

### Opensearch Alerting Dashboards
* Fix Unit tests and Cypress test workflows ([#4](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/4))
* Update github workflows for alpha2 ([#6](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/6))

### Opensearch Index Management Dashboards Plugin
* Updates versions and fixes the unit test workflow ([#7](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/7))
* Fix cypress workflow ([#8](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/8))

### Opensearch Anomaly Detection Dashboards
* Reset plugin version to 1.0.0.0, fix UT workflow ([#9](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/9))
* Rename plugin helpers file to fix zip build ([#12](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/12))

### Opensearch Knn
* Update upstream ([#1](https://github.com/opensearch-project/k-NN/pull/1))
* update CI to build on PRs ([#5](https://github.com/opensearch-project/k-NN/pull/1))
* Run build ([#8](https://github.com/opensearch-project/k-NN/pull/8))
* Update plugin name ([#9](https://github.com/opensearch-project/k-NN/pull/9))


### Opensearch Performance Analyzer
* OpenSearch fork changes ([#1](https://github.com/opensearch-project/performance-analyzer/pull/1))
* OpenSearch fork changes ([#3](https://github.com/opensearch-project/performance-analyzer-rca/pull/3))
* Modify opensearch version and fix buiild CI ([#4](https://github.com/opensearch-project/performance-analyzer/pull/4))
* Add missing metricsdb* files and enable spotless ([#5](https://github.com/opensearch-project/performance-analyzer-rca/pull/5))
* Update version to 1.x ([#6](https://github.com/opensearch-project/performance-analyzer/pull/6))
* Update version to 1.0 beta ([#6](https://github.com/opensearch-project/performance-analyzer-rca/pull/6))
* Update plugin name and add release notes ([#7](https://github.com/opensearch-project/performance-analyzer/pull/7))
* Fix Integration test and update README ([#7](https://github.com/opensearch-project/performance-analyzer-rca/pull/7))


### Opensearch Perftop
* OpenSearch fork changes ([#1](https://github.com/opensearch-project/perftop/pull/1))
* Add perfTop github CI on main branch ([#3](https://github.com/opensearch-project/perftop/pull/3))
* Update workflow and change opensearch version ([#4](https://github.com/opensearch-project/perftop/pull/4))
* Update plugin name and add release notes ([#5](https://github.com/opensearch-project/perftop/pull/5))


### Opensearch Sql
* Fix ODBC build failures ([#13](https://github.com/opensearch-project/sql/pull/13))

### Opensearch Job Scheduler Plugin
* Build and publish to maven local, enable CI ([#8](https://github.com/opensearch-project/job-scheduler/pull/8))
* Reset version to 1.0. ([#9](https://github.com/opensearch-project/job-scheduler/pull/9))
* Build against OpenSearch 1.0.0-alpha1. ([#11](https://github.com/opensearch-project/job-scheduler/pull/11))
* Rename plugin ([#14](https://github.com/opensearch-project/job-scheduler/pull/14))
* Run integration tests in CI + alpha2 ([#12](https://github.com/opensearch-project/job-scheduler/pull/12))
* consume opensearch 1.0.0-beta1 ([#18](https://github.com/opensearch-project/job-scheduler/pull/18))


### Opensearch Anomaly Detection
* Removing few lingering Elasticsearch strings in the repo ([#6](https://github.com/opensearch-project/anomaly-detection/pull/6))
* Updating the license and docs ([#7](https://github.com/opensearch-project/anomaly-detection/pull/7))
* Add SPDX license header to all files ([#10](https://github.com/opensearch-project/anomaly-detection/pull/10))
* Updating the Notice.txt to relfect the right software being used ([#11](https://github.com/opensearch-project/anomaly-detection/pull/11))
* Updated copyright and external links. ([#12](https://github.com/opensearch-project/anomaly-detection/pull/12))


## DOCUMENTATION

### Opensearch Index Management
* update NOTICE, README, LICENSE, CONTRIBUTING files; add MAINTAINERS file; update issue and PR template files ([#1](https://github.com/opensearch-project/index-management/pull/1))
* add SPDX license header for gradle files ([#2](https://github.com/opensearch-project/index-management/pull/2))
* add SPDX license header to all files ([#3](https://github.com/opensearch-project/index-management/pull/3))
* update MAINTAINERS file ([#5](https://github.com/opensearch-project/index-management/pull/5))
* add release notes for 1.0.0.0-beta1 release ([#6](https://github.com/opensearch-project/index-management/pull/6))

### Opensearch Anomaly Detection Dashboards
* Update base documentation files; add issues & PR templates ([#5](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/5))
* Add DCO info in CONTRIBUTING.md, remove admins from MAINTAINERS.md ([#6](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/6))
* Add SPDX license header to all files ([#7](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/7))
* Update NOTICE to reflect the direct software being used ([#8](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/8))

### Opensearch Index Management Dashboards Plugin
* Adds new license header ([#6](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/6))

### OpenSearch Common-utils
* Update licenses ([#3](https://github.com/opensearch-project/common-utils/pull/3))
* Add new license header ([#5](https://github.com/opensearch-project/common-utils/pull/5))
* Update spotless license file ([#11](https://github.com/opensearch-project/common-utils/pull/11))
* Add release notes and script to generate release notes ([#16](https://github.com/opensearch-project/common-utils/pull/16))

### Opensearch Asynchronous Search
* Update licenses ([#4](https://github.com/opensearch-project/asynchronous-search/pull/4))

### Opensearch Alerting
* Update licenses ([#5](https://github.com/opensearch-project/alerting/pull/5))
* Update documentation to remove more ES references and update licenses  ([#4](https://github.com/opensearch-project/alerting/pull/4))

### Opensearch Alerting Dashboards
* Update license headers ([#3](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/3))

### Opensearch Knn
* Standardize files with OpenSearch files contents ([#3](https://github.com/opensearch-project/k-NN/pull/3))
* Add SPDX-License to header ([#4](https://github.com/opensearch-project/k-NN/pull/4))
* Update README.md ([#7](https://github.com/opensearch-project/k-NN/pull/7))


### Opensearch Cli
* Standardize files with OpenSearch files contents ([#11](https://github.com/opensearch-project/opensearch-cli/pull/11))
* Fix typo ([#12](https://github.com/opensearch-project/opensearch-cli/pull/12))
* Add SPDX-License to all files ([#13](https://github.com/opensearch-project/opensearch-cli/pull/13))


### Opensearch Performance Analyzer
* Add SPDX license identifier ([#3](https://github.com/opensearch-project/performance-analyzer/pull/3))
* Add SPDX license identifier ([#4](https://github.com/opensearch-project/performance-analyzer-rca/pull/4))


### Opensearch Perftop
* Add SPDX license identifier ([#2](https://github.com/opensearch-project/perftop/pull/2))


### Opensearch Job Scheduler Plugin
* Update licenses ([#3](https://github.com/opensearch-project/job-scheduler/pull/3))
* Go Public ([#2](https://github.com/opensearch-project/job-scheduler/pull/2))
* Add new license header ([#6](https://github.com/opensearch-project/job-scheduler/pull/6))
* update release note for 1.0.0.0-beta1 ([#17](https://github.com/opensearch-project/job-scheduler/pull/17))

## MAINTENANCE

### Opensearch Index Management Dashboards Plugin
* Bump plugin version to 1.0.0.0-beta1 ([#9](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/9))

### Opensearch Anomaly Detection
* Migrating plugin to work with OpenSearch ([#1](https://github.com/opensearch-project/anomaly-detection/pull/1))
* Rename plugin to opensearch-anomaly-detection; bump plugin to 1.0.0-alpha2 ([#28](https://github.com/opensearch-project/anomaly-detection/pull/28))
* Bump plugin + dependencies to version 1.0.0.0-beta1 ([#32](https://github.com/opensearch-project/anomaly-detection/pull/32))

### Opensearch Anomaly Detection Dashboards
* Bump plugin version to 1.0.0.0-beta1 ([#14](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/14))

### Opensearch Alerting Dashboards
* Bump plugin version to 1.0.0.0-beta1 ([#7](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/7))

### Opensearch Security
* Redact BCrypt security config internal hashes from audit logs ([#756](https://github.com/opensearch-project/security/pull/756))
* Update docs on snapshot restore settings ([#814](https://github.com/opensearch-project/security/pull/814))
* Optimize debug log enable check ([#895](https://github.com/opensearch-project/security/pull/895))
* Correcting setupSslOnlyMode to use AbstractSecurityUnitTest.hasCustomTransportSettings() ([#1057](https://github.com/opensearch-project/security/pull/1057))
* Remove code setting the value for cluster.routing.allocation.disk.threshold_enabled ([#1067](https://github.com/opensearch-project/security/pull/1067))
* Rename for OpenSearch ([#1126](https://github.com/opensearch-project/security/pull/1126))
* Fix CI ([#1131](https://github.com/opensearch-project/security/pull/1131))
* Consume OpenSearch 1.0.0-alpha1 ([#1132](https://github.com/opensearch-project/security/pull/1132))
* Change name and version of plugin ([#1133](https://github.com/opensearch-project/security/pull/1133))
* Build with OpenSearch 1.0.0-alpha2 ([#1140](https://github.com/opensearch-project/security/pull/1140))
* Bump plugin version to beta1 ([#1141](https://github.com/opensearch-project/security/pull/1141))
* Build security plugin with OpenSearch 1.0.0-beta1 ([#1143](https://github.com/opensearch-project/security/pull/1143))
* Change opensearch version to use ([#1146](https://github.com/opensearch-project/security/pull/1146))
* Fix echo messages and anchor links ([#1147](https://github.com/opensearch-project/security/pull/1147))
* Update static roles for compatibility for new indices used in OpenSearch Dashboards ([#1148](https://github.com/opensearch-project/security/pull/1148))
* Update release note for OpenSearch Security Plugin `1.0.0.0-beta1`([#1152](https://github.com/opensearch-project/security/pull/1152))


### Opensearch Security Dashboards Plugin
* Update Contributing doc and add PR template ([#724](https://github.com/opensearch-project/security-dashboards-plugin/pull/724))
* change version back to beta1 ([#748](https://github.com/opensearch-project/security-dashboards-plugin/pull/748))
* Fix tests and document cleanup ([#754](https://github.com/opensearch-project/security-dashboards-plugin/pull/754))
* Update 1.0.0.0-beta1 release notes ([#755](https://github.com/opensearch-project/security-dashboards-plugin/pull/755))

### Opensearch Job Scheduler Plugin
* Migrate to OpenSearch ([#1](https://github.com/opensearch-project/job-scheduler/pull/1))


## REFACTORING

### Opensearch Index Management Dashboards Plugin
* Migrates plugin to OpenSearch Dashboards ([#1](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1))
* Cleans up a few more references ([#5](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/5))
* Update plugin id to indexManagementDashboards ([#10](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/10))

### Opensearch Alerting
* Change Kibana UserAgent to OpenSearchDashboards ([#3](https://github.com/opensearch-project/alerting/pull/3))
* Migrate Alerting to OpenSearch ([#1](https://github.com/opensearch-project/alerting/pull/1))
* Update version to alpha2 ([#10](https://github.com/opensearch-project/alerting/pull/10))
* Update version to 1.0.0.0-beta1 ([#11](https://github.com/opensearch-project/alerting/pull/11))

### OpenSearch Common-utils
* Renaming lingering strings to OpenSearch ([#2](https://github.com/opensearch-project/common-utils/pull/2))
* Update version to 1.0.0.0-alpha2 ([#15](https://github.com/opensearch-project/common-utils/pull/15))
* Update version to 1.0.0.0-beta1 ([#17](https://github.com/opensearch-project/common-utils/pull/17))

### Opensearch Alerting Dashboards
* Migrate Alerting to OpenSearch-Dashboards ([#1](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1))
* Update plugin name and url ([#2](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/2))
* Update plugin naming ([#5](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/5))

### Opensearch Asynchronous Search
* Update version to 1.0.0.0-beta1 ([#8](https://github.com/opensearch-project/asynchronous-search/pull/8))

### Opensearch Cli
* Opensearch cli rename ([#2](https://github.com/opensearch-project/opensearch-cli/pull/2))
* Update test badge repo link ([#3](https://github.com/opensearch-project/opensearch-cli/pull/3))
* Rename core to platform ([#4](https://github.com/opensearch-project/opensearch-cli/pull/4))


