# OpenSearch and OpenSearch Dashboards 2.19.7 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.19.7 includes the following enhancements, bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.7.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.7.md).

## Enhancements

### OpenSearch Security

* Scale legacy alias resolution with bounded indices-lookup access for improved performance on clusters with many aliases ([#6320](https://github.com/opensearch-project/security/pull/6320))

## BUG FIXES

### OpenSearch Alerting

* Fix unbounded memory growth of findingsToTriggeredQueries in doc-level monitor fan-out action ([#2244](https://github.com/opensearch-project/alerting/pull/2244))

### OpenSearch Alerting Dashboards Plugin

* Fix missing import in TriggerNotifications.js that caused add trigger functionality to fail for composite monitors ([#1357](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1357))

### OpenSearch Dashboards Reporting

* Fix dependency CVEs for json-2-csv, dompurify, brace-expansion, js-yaml, and baseline-browser-mapping ([#816](https://github.com/opensearch-project/dashboards-reporting/pull/816))
* Fix critical handlebars and high-severity extract-zip CVEs by relocking handlebars to 4.7.10 and removing unused cypress dependency ([#822](https://github.com/opensearch-project/dashboards-reporting/pull/822))

### OpenSearch Job Scheduler

* Fix job metadata sweep query to sort by `_seq_no` instead of `_id` ([#912](https://github.com/opensearch-project/job-scheduler/pull/912))

### OpenSearch Query Insights Dashboards

* Fix Group By selector on Configuration page always showing None after refresh ([#408](https://github.com/opensearch-project/query-insights-dashboards/pull/408))

### OpenSearch Security

* Fix handling of unsupported HTTP content encodings such as zstd to pass through unmodified ([#6629](https://github.com/opensearch-project/security/pull/6629))
* Fix parent-child query detection across classloaders ([#6478](https://github.com/opensearch-project/security/pull/6478))
* Return the matcher itself when concat collapses to one, preventing inter-node request failures with duplicate `nodes_dn` entries ([#6606](https://github.com/opensearch-project/security/pull/6606))

### OpenSearch Security Analytics

* Fix authorization bypass in stashContext() by adding pre-flight index permission checks and blocking cross-index terms lookup queries ([#1768](https://github.com/opensearch-project/security-analytics/pull/1768))

## INFRASTRUCTURE

### OpenSearch Common Utils

* Bump 1password/load-secrets-action to v5.0.1 ([#996](https://github.com/opensearch-project/common-utils/pull/996))

### OpenSearch Custom Codecs

* Bump `1password/load-secrets-action` to v5.0.1 ([#370](https://github.com/opensearch-project/custom-codecs/pull/370))

### OpenSearch Dashboards Query Workbench

* Unblock CI by pinning all GitHub Actions to SHAs and fixing accumulated breakages on the 2.19 branch ([#597](https://github.com/opensearch-project/dashboards-query-workbench/pull/597))

### OpenSearch Index Management

* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#1745](https://github.com/opensearch-project/index-management/pull/1745))

### OpenSearch Job Scheduler

* Guard `eclipse()` to spotless tasks and pin P2 mirror version ([#990](https://github.com/opensearch-project/job-scheduler/pull/990))

### OpenSearch ML Commons

* Replace retired OpenAI and Bedrock models in integration tests to fix CI failures ([#5126](https://github.com/opensearch-project/ml-commons/pull/5126))

### OpenSearch Observability

* Bump `1password/load-secrets-action` to v5.0.1 ([#2023](https://github.com/opensearch-project/observability/pull/2023))

### OpenSearch OpenSearch Remote Metadata Sdk

* Register placeholder spotlessCheck task on JDK < 17 to fix JDK 11 CI builds ([#464](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/464))

### OpenSearch OpenSearch System Templates

* Guard eclipse() to spotless tasks and keep P2 mirror on pinned version ([#168](https://github.com/opensearch-project/opensearch-system-templates/pull/168))

### OpenSearch Performance Analyzer

* Bump `1password/load-secrets-action` to v5.0.1 ([#974](https://github.com/opensearch-project/performance-analyzer/pull/974))

### OpenSearch Query Insights

* Use Eclipse P2 mirror to avoid download.eclipse.org outages ([#667](https://github.com/opensearch-project/query-insights/pull/667))
* Guard eclipse() to spotless tasks and keep P2 mirror on pinned version ([#679](https://github.com/opensearch-project/query-insights/pull/679))

### OpenSearch Security

* Guard Eclipse JDT formatter provisioning to spotless tasks and keep P2 mirror on pinned version ([#6462](https://github.com/opensearch-project/security/pull/6462))
* Only provision Eclipse JDT formatter when running a spotless task ([#6453](https://github.com/opensearch-project/security/pull/6453))

### OpenSearch Security Analytics

* Only use alerting SNAPSHOTS in SNAPSHOT builds, otherwise use release artifacts ([#1841](https://github.com/opensearch-project/security-analytics/pull/1841))

### OpenSearch Skills

* Bump 1password/load-secrets-action to v5.0.1 ([#787](https://github.com/opensearch-project/skills/pull/787))

## MAINTENANCE

### OpenSearch Dashboards Assistant

* Bump brace-expansion to 1.1.18 to address CVE-2026-69152 ([#742](https://github.com/opensearch-project/dashboards-assistant/pull/742))
* Bump js-yaml to 3.15.0 to address CVE-2026-59869 ([#744](https://github.com/opensearch-project/dashboards-assistant/pull/744))

### OpenSearch Dashboards Observability

* Bump fast-uri to ^3.1.7 to remediate host-confusion and SSRF vulnerabilities (CVE-2026-75931, CVE-2026-75899, CVE-2026-75975, CVE-2026-76172) ([#2874](https://github.com/opensearch-project/dashboards-observability/pull/2874))
* Bump js-yaml, brace-expansion, nanoid, form-data, tmp, and dompurify to remediate multiple high and medium severity CVEs ([#2916](https://github.com/opensearch-project/dashboards-observability/pull/2916))

### OpenSearch Dashboards Query Workbench

* Bump brace-expansion to 1.1.17 to address CVE-2026-14257 ([#608](https://github.com/opensearch-project/dashboards-query-workbench/pull/608))
* Bump form-data to 4.0.6 to address CVE-2026-12143 ([#609](https://github.com/opensearch-project/dashboards-query-workbench/pull/609))
* Bump qs to 6.16.0 to address CVE-2026-82562 and CVE-2026-82417 ([#596](https://github.com/opensearch-project/dashboards-query-workbench/pull/596))

### OpenSearch Flow Framework

* Bump Jackson force directives to 2.18.9 to align with OpenSearch core ([#1506](https://github.com/opensearch-project/flow-framework/pull/1506))

### OpenSearch Index Management

* Bump 1password/load-secrets-action to v5.0.1 ([#1724](https://github.com/opensearch-project/index-management/pull/1724))

### OpenSearch ML Commons

* Bump 1password/load-secrets-action to v5.0.1 ([#4984](https://github.com/opensearch-project/ml-commons/pull/4984))
* Bump bc-fips, httpcore5, and httpclient5 to address multiple CVEs ([#5115](https://github.com/opensearch-project/ml-commons/pull/5115))
* Run snapshot publish workflow on Java 21 to fix broken Maven publishing ([#5129](https://github.com/opensearch-project/ml-commons/pull/5129))

### OpenSearch OpenSearch System Templates

* Bump 1password/load-secrets-action to v5.0.1 ([#159](https://github.com/opensearch-project/opensearch-system-templates/pull/159))

### OpenSearch Query Insights

* Bump 1password/load-secrets-action to v5.0.1 ([#668](https://github.com/opensearch-project/query-insights/pull/668))

### OpenSearch Security Analytics

* Add Eclipse P2 mirror to avoid download.eclipse.org outages ([#1801](https://github.com/opensearch-project/security-analytics/pull/1801))
* Guard eclipse() to Spotless tasks and keep P2 mirror on pinned version ([#1809](https://github.com/opensearch-project/security-analytics/pull/1809))
* Bump 1password/load-secrets-action to v5.0.1 ([#1795](https://github.com/opensearch-project/security-analytics/pull/1795))

### OpenSearch Security Dashboards Plugin

* Bump transitive security dependencies (brace-expansion, ip-address, qs) ([#2556](https://github.com/opensearch-project/security-dashboards-plugin/pull/2556))

### SQL

* Remove setuptools pin from doctest requirements to address CVE-2026-59890 ([#5843](https://github.com/opensearch-project/sql/pull/5843))
