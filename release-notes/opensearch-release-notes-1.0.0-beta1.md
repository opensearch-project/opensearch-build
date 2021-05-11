# OpenSearch and Dashboards 1.0.0-beta1 Release Notes

## Release Highlights

## Release Details

You can also track upcoming features in OpenSearch and Dashboards by watching the code repositories or checking the [project website](https://opensearch.org/blog/).

## BREAKING CHANGES

## FEATURES

### Opensearch Cli
* Allow user to provide certificate path ([#6](https://github.com/opensearch-project/opensearch-cli/pull/6))


## ENHANCEMENTS

### Opensearch Index Management
* migrate plugin to be compatible with OpenSearch [#1](https://github.com/opensearch-project/index-management/pull/1)
* rename plugin [#5](https://github.com/opensearch-project/index-management/pull/5)


### Opensearch Security
* Check and create multi-tenant index with alias for Update and Delete requests. Try to find a name for the multi-tenant index if index/alias with ".kibana_..._#" already exists ([#1058](https://github.com/opensearch-project/security/pull/1058))


### Opensearch Security Dashboards Plugin
* Save tenant selection by default and remove the checkbox [#725](https://github.com/opensearch-project/security-dashboards-plugin/pull/725)
* Update list of permissions available in UI [#740](https://github.com/opensearch-project/security-dashboards-plugin/pull/740)
* name change to opensearch dashboard [#743](https://github.com/opensearch-project/security-dashboards-plugin/pull/743)


## BUG FIXES

### Opensearch Security
* [Fix][Usage][Hasher] wrong file reference hash.sh ([#1093](https://github.com/opensearch-project/security/pull/1093))


### Opensearch Security Dashboards Plugin
* Revert "Add opendistro/ism and rollup actions" [#714](https://github.com/opensearch-project/security-dashboards-plugin/pull/714)
* Making sure SAML cookie uses saml session timeout value if it is available [#715](https://github.com/opensearch-project/security-dashboards-plugin/pull/715)
* Making sure SAML cookie uses saml session timeout value if it is available [#717](https://github.com/opensearch-project/security-dashboards-plugin/pull/717)
* Cherry-pick fix of saving tenant option from main to 7.9.1 branch [#716](https://github.com/opensearch-project/security-dashboards-plugin/pull/716)
* Fix github integration test for 1.13.0.1 [#723](https://github.com/opensearch-project/security-dashboards-plugin/pull/723)
* Updated logic for splitting SAML JWT token [#730](https://github.com/opensearch-project/security-dashboards-plugin/pull/730)
* Updated logic for splitting SAML JWT token [#731](https://github.com/opensearch-project/security-dashboards-plugin/pull/731)
* Fix ci and change artifact name [#745](https://github.com/opensearch-project/security-dashboards-plugin/pull/745)
* fix text and remove svg content [#751](https://github.com/opensearch-project/security-dashboards-plugin/pull/751)
* fix readme badge and audit log text [#753](https://github.com/opensearch-project/security-dashboards-plugin/pull/753)


## INFRASTRUCTURE

### Opensearch Index Management
* update github workflows [#5](https://github.com/opensearch-project/index-management/pull/5)


### Opensearch Index Management Dashboards Plugin
* Updates versions and fixes the unit test workflow ([#7](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/7))
* Fix cypress workflow ([#8](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/8))


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


## DOCUMENTATION

### Opensearch Index Management
* update NOTICE, README, LICENSE, CONTRIBUTING files; add MAINTAINERS file; update issue and PR template files [#1](https://github.com/opensearch-project/index-management/pull/1)
* add SPDX license header for gradle files [#2](https://github.com/opensearch-project/index-management/pull/2)
* add SPDX license header to all files [#3](https://github.com/opensearch-project/index-management/pull/3)
* update MAINTAINERS file [#5](https://github.com/opensearch-project/index-management/pull/5)
* add release notes for 1.0.0.0-beta1 release [#6](https://github.com/opensearch-project/index-management/pull/6)


### Opensearch Index Management Dashboards Plugin
* Adds new license header ([#6](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/6))


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


## MAINTENANCE

### Opensearch Index Management Dashboards Plugin
* Bump plugin version to 1.0.0.0-beta1 ([#9](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/9))


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
* Update Contributing doc and add PR template [#724](https://github.com/opensearch-project/security-dashboards-plugin/pull/724)
* change version back to beta1 [#748](https://github.com/opensearch-project/security-dashboards-plugin/pull/748)
* Fix tests and document cleanup [#754](https://github.com/opensearch-project/security-dashboards-plugin/pull/754)
* Update 1.0.0.0-beta1 release notes [#755](https://github.com/opensearch-project/security-dashboards-plugin/pull/755)


## REFACTORING

### Opensearch Index Management Dashboards Plugin
* Migrates plugin to OpenSearch Dashboards ([#1](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1))
* Cleans up a few more references ([#5](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/5))
* Update plugin id to indexManagementDashboards ([#10](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/10))


### Opensearch Cli
* Opensearch cli rename ([#2](https://github.com/opensearch-project/opensearch-cli/pull/2))
* Update test badge repo link ([#3](https://github.com/opensearch-project/opensearch-cli/pull/3))
* Rename core to platform ([#4](https://github.com/opensearch-project/opensearch-cli/pull/4))


