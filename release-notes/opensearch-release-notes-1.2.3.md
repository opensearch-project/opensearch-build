# OpenSearch 1.2.3 Release Notes

## Release Highlights

This patch releases updates the version of Log4j used in OpenSearch to Log4j 2.17.0 as recommended by the advisory in [CVE-2021-45105](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45105).

### OpenSearch

* Fix repository-azure plugin hanging, regression introduced in 1.2.0 ([#1734](https://github.com/opensearch-project/OpenSearch/issues/1734))
* Increment version to 1.2.3 and upgrade log4j to 2.17.0 ([#1771](https://github.com/opensearch-project/OpenSearch/pull/1771))


### OpenSearch Security

* Bump log4j-core from 2.16.0 to 2.17.0 ([#1535](https://github.com/opensearch-project/security/pull/1535))

### OpenSearch SQL

* Bump log4j from 2.16.0 to 2.17.0  ([#345](https://github.com/opensearch-project/sql/pull/345))


### OpenSearch Performance Analyzer

* Upgrade log4j version from 2.16.0 to 2.17.0 ([#109](https://github.com/opensearch-project/performance-analyzer/pull/109))
* Upgrade log4j version from 2.16.0 to 2.17.0 ([#105](https://github.com/opensearch-project/performance-analyzer-rca/pull/105))
