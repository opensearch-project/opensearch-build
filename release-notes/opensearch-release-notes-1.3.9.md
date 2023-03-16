# OpenSearch and OpenSearch Dashboards 1.3.9 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.9](https://opensearch.org/versions/opensearch-1-3-9.html) includes the following bug fixes, infrastructure, enhancements and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.9.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.9.md).

## ENHANCEMENTS

### OpenSearch Security Dashboards Plugin
* Windows CI support for 1.3 branch ([#1321](https://github.com/opensearch-project/security-dashboards-plugin/pull/1321))

### OpenSearch Security
* Flatten response times ([#2471](https://github.com/opensearch-project/security/pull/2471))
* Add auto github release workflow ([#2450](https://github.com/opensearch-project/security/pull/2450))
* Adding index template permissions to kibana_server role ([2503](https://github.com/opensearch-project/security/pull/2503))
* Clock skew tolerance for oidc token validation ([2482](https://github.com/opensearch-project/security/pull/2482))

### OpenSearch k-NN
* Change initial size of DocIdSetBuilder ([#502](https://github.com/opensearch-project/k-NN/pull/502))

## BUG FIXES

### OpenSearch Security Dashboards Plugin
* Replace legacy template with index template ([#1359](https://github.com/opensearch-project/security-dashboards-plugin/pull/1359))

## INFRASTRUCTURE

### OpenSearch k-NN
* Increment version to 1.3.9 ([#749](https://github.com/opensearch-project/k-NN/pull/749))

## MAINTENANCE

### OpenSearch Security Dashboards Plugin
* Add auto-release workflow ([#1339](https://github.com/opensearch-project/security-dashboards-plugin/pull/1339))

### OpenSearch Security
* Update kafka client to 3.4.0 ([#2484](https://github.com/opensearch-project/security/pull/2484))
* Fix the format of the codeowners file ([#2469](https://github.com/opensearch-project/security/pull/2469))
