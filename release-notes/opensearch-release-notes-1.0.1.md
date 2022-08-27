# OpenSearch Distribution Version 1.0.1 Release Notes

## Release Details

OpenSearch Distribution Version 1.0.1 includes the following enhancements, bug fixes, documentation and maintenance updates.

## ENHANCEMENTS

### OpenSearch Release Engineering
* Optimize Docker images size, thanks @osddeitf ([#93](https://github.com/opensearch-project/opensearch-build/pull/93))

## BUG FIXES

### Opensearch Dashboards Notebooks
* Bump Version to 1.0.1.0 and Patch Notebooks Context Menu ([#64](https://github.com/opensearch-project/dashboards-notebooks/pull/64))


### Opensearch Dashboards Reports
* Bump version and add notebooks context menu fix for 1.0.1.0 patch ([#142](https://github.com/opensearch-project/dashboards-reports/pull/142))


### Opensearch Index Management
* Adds back opendistro policy_id setting to explain response ([#127](https://github.com/opensearch-project/index-management/pull/127))


### Opensearch Index Management Dashboards Plugin
* Address data stream API security breaking issue ([#69](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/69))


### Opensearch Performance Analyzer
* Create writer file only if metrics are present ([#23](https://github.com/opensearch-project/performance-analyzer-rca/pull/23))
* Fixing Event Log file cleanup issue ([#30](https://github.com/opensearch-project/performance-analyzer-rca/pull/30))
* Create writer file if metrics are available ([#31](https://github.com/opensearch-project/performance-analyzer/pull/31))
* Addressing the spotbug failure ([#31](https://github.com/opensearch-project/performance-analyzer-rca/pull/31))
* Fixing Event Log file cleanup issue ([#36](https://github.com/opensearch-project/performance-analyzer/pull/36))
* Handling purging of lingering files before scheduleExecutor start ([#37](https://github.com/opensearch-project/performance-analyzer/pull/37))
* Fix failing file handler test ([#38](https://github.com/opensearch-project/performance-analyzer/pull/38))
* Add privileges for removing files ([#45](https://github.com/opensearch-project/performance-analyzer-rca/pull/45))
* Fix build to succeed with opensearch_version provided ([#52](https://github.com/opensearch-project/performance-analyzer/pull/52))


### Opensearch Security
* Return HTTP 409 if get parallel put request ([#1158](https://github.com/opensearch-project/security/pull/1158))
* Add validation for null array DataType ([#1157](https://github.com/opensearch-project/security/pull/1157))
* Add support for ResolveIndexAction handling ([#1312](https://github.com/opensearch-project/security/pull/1312))
* Fix LDAP authentication when using StartTLS ([#1415](https://github.com/opensearch-project/security/pull/1415))
* Fix index permissions for negative lookahead and negated regex index patterns ([#1300](https://github.com/opensearch-project/security/pull/1300))


### Opensearch Security Dashboards Plugin
* Add resolve pemission to UI ([#803](https://github.com/opensearch-project/security-dashboards-plugin/pull/803))
* Add refresh page to account-app.tsx to solve the tenant display issue ([#811](https://github.com/opensearch-project/security-dashboards-plugin/pull/811))


## DOCUMENTATION

### Opensearch Dashboards Notebooks
* Add release notes for 1.0.1 release ([#65](https://github.com/opensearch-project/dashboards-notebooks/pull/65))


### Opensearch Dashboards Reports
* Add release notes for 1.0.1 release ([#143](https://github.com/opensearch-project/dashboards-reports/pull/143))


## MAINTENANCE

### Opensearch Performance Analyzer
* Add tests to check for writer file only if metrics are present ([#35](https://github.com/opensearch-project/performance-analyzer/pull/35))
* Fixing the linker error, updating from docs-beta to official document ([#32](https://github.com/opensearch-project/performance-analyzer/pull/32))
* Remove dependency on main branch when running spotless ([#47](https://github.com/opensearch-project/performance-analyzer/pull/47))
* Updates to gradle build file ([#48](https://github.com/opensearch-project/performance-analyzer/pull/48))
* Remove dependency on main branch when running spotless check ([#54](https://github.com/opensearch-project/performance-analyzer-rca/pull/54))
* Update the branch to 1.0.1 ([#58](https://github.com/opensearch-project/performance-analyzer/pull/58))
* Add release notes for 1.0.1 release ([#59](https://github.com/opensearch-project/performance-analyzer/pull/59))
* Update the branch to 1.0.1 ([#62](https://github.com/opensearch-project/performance-analyzer-rca/pull/62))


### Opensearch Security
* Fix maven build ${version} deprecation warning ([#1209](https://github.com/opensearch-project/security/pull/1209))
* Fix race condition on async test for PR #1158 ([#1331](https://github.com/opensearch-project/security/pull/1331))
* Build OpenSearch in CD workflow in order to build security plugin ([#1364](https://github.com/opensearch-project/security/pull/1364))
* Update checkNullElementsInArray() unit test to check both error message and error code instead of only checking the error code ([#1370](https://github.com/opensearch-project/security/pull/1370))
* Add themed logo to README ([#1333](https://github.com/opensearch-project/security/pull/1333))
* Checkout OpenSearch after Cache in CD ([#1410](https://github.com/opensearch-project/security/pull/1410))
* Address follow up comments for PR #1172 ([#1224](https://github.com/opensearch-project/security/pull/1224))
* Upgrade CXF to v3.4.4 ([#1412](https://github.com/opensearch-project/security/pull/1412))
* Bump version to 1.0.1.0 ([#1418](https://github.com/opensearch-project/security/pull/1418))


### Opensearch Security Dashboards Plugin
* Add Integtest.sh for OpenSearch integtest setups ([#783](https://github.com/opensearch-project/security-dashboards-plugin/pull/783))
* Bump plugin version to 1.0.1.0 ([#813](https://github.com/opensearch-project/security-dashboards-plugin/pull/813))

## NOTES
No changes were made to [OpenSearch](https://github.com/opensearch-project/OpenSearch/releases/tag/1.0.0) and [OpenSearch-Dashboards](https://github.com/opensearch-project/OpenSearch-Dashboards/releases/tag/1.0.0).


