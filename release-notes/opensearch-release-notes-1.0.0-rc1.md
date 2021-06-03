# Open Distro for Elasticsearch 1.13.2 Release Notes

## Release Highlights

## Release Details

You can also track upcoming features in Open Distro for Elasticsearch by watching the code repositories or checking the [project website](https://opendistro.github.io/for-elasticsearch/features/comingsoon.html).

## BREAKING CHANGES

## FEATURES

## ENHANCEMENTS

### Opensearch Performance Analyzer
* Add CONFIG_DIR_NOT_FOUND in StatExceptionCode ([#11](https://github.com/opensearch-project/performance-analyzer-rca/pull/11))


### Opensearch Perftop
* Add env.js to store global property ([#10](https://github.com/opensearch-project/perftop/pull/10))


### Opensearch Security
* Allow attempt to load security config in case of plugin restart even if security index already exists ([#1154](https://github.com/opensearch-project/security/pull/1154))
* Allowing granular access for data-stream related transport actions ([#1170](https://github.com/opensearch-project/security/pull/1170))


### Opensearch Security Dashboards Plugin
* add svg content [#766](https://github.com/opensearch-project/security-dashboards-plugin/pull/766)
* Changes regarding the anonymous auth flow [#768](https://github.com/opensearch-project/security-dashboards-plugin/pull/768)


### Opensearch Sql
* Support querying a data stream ([#56](https://github.com/opensearch-project/sql/pull/56))


## BUG FIXES

### Opensearch Performance Analyzer
* Create conf directory if not exist to avoid NoSuchFile exceptions ([#9](https://github.com/opensearch-project/performance-analyzer/pull/9))
* Update docker artifact link ([#9](https://github.com/opensearch-project/performance-analyzer-rca/pull/9))
* Modify JVM gen tuning policy and update the Unit test ([#12](https://github.com/opensearch-project/performance-analyzer-rca/pull/12))


### Opensearch Security
* Delay the security index initial bootstrap when the index is red ([#1153](https://github.com/opensearch-project/security/pull/1153))
* Remove redundant isEmpty check and incorrect string equals operator ([#1181](https://github.com/opensearch-project/security/pull/1181))


### Opensearch Security Dashboards Plugin
* Fixing JSON parsing in SAML for strings that contain '' character [#749](https://github.com/opensearch-project/security-dashboards-plugin/pull/749)
* Fix login redirect [#777](https://github.com/opensearch-project/security-dashboards-plugin/pull/777)


### Opensearch Trace Analytics
* Pick latest commits from opendistro trace analytics ([#13](https://github.com/opensearch-project/trace-analytics/pull/13))


## INFRASTRUCTURE

### Opensearch Performance Analyzer
* Upgrade Jackson version to 2.11.4 ([#13](https://github.com/opensearch-project/performance-analyzer/pull/13))
* Upgrade Jackson version to 2.11.4 ([#15](https://github.com/opensearch-project/performance-analyzer-rca/pull/15))
* Update version to rc1 ([#16](https://github.com/opensearch-project/performance-analyzer/pull/16))
* Update to rc1 version and opendistro links ([#17](https://github.com/opensearch-project/performance-analyzer-rca/pull/17))


### Opensearch Perftop
* Update version to rc1 ([#10](https://github.com/opensearch-project/perftop/pull/10))


## DOCUMENTATION

### Opensearch Performance Analyzer
* Update rest endpoint names in README ([#15](https://github.com/opensearch-project/performance-analyzer/pull/15))


### Opensearch Perftop
* Update issue template with multiple labels([#7](https://github.com/opensearch-project/perftop/pull/7))
* Update OpenSearch documents link ([#9](https://github.com/opensearch-project/perftop/pull/9))
* Update REST endpoint in document ([#10](https://github.com/opensearch-project/perftop/pull/10))


### Opensearch Sql
* Migrate SQL/PPL, JDBC, ODBC docs to OpenSearch ([#68](https://github.com/opensearch-project/sql/pull/68))


## MAINTENANCE

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
* move issue templates to ISSUE_TEMPLATE [#758](https://github.com/opensearch-project/security-dashboards-plugin/pull/758)
* Update issue template with multiple labels [#756](https://github.com/opensearch-project/security-dashboards-plugin/pull/756)
* Naming convention change in repo [#764](https://github.com/opensearch-project/security-dashboards-plugin/pull/764)
* Point document links to opensearch.org [#763](https://github.com/opensearch-project/security-dashboards-plugin/pull/763)
* Create release notes for rc-1 and Bump version to 1.0.0.0-rc1 [#771](https://github.com/opensearch-project/security-dashboards-plugin/pull/771)
* Point OpenSearch Dashboards to to new back end APIs [#770](https://github.com/opensearch-project/security-dashboards-plugin/pull/770)
* Change the titles of release notes [#772](https://github.com/opensearch-project/security-dashboards-plugin/pull/772)


## REFACTORING

