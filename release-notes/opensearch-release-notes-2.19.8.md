# OpenSearch 2.19.8 and OpenSearch Dashboards 2.19.7 Release Notes

## Release Details
[OpenSearch 2.19.8](https://opensearch.org/artifacts/by-version/#release-2-19-8) includes the following bug fix and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.8.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.7.md).

## BUG FIXES

### OpenSearch
* Bound min_hash filter parameters to prevent OOM ([#23374](https://github.com/opensearch-project/OpenSearch/pull/23374))
* Block ptrace and process memory access syscalls in the system call filter ([#23494](https://github.com/opensearch-project/OpenSearch/pull/23494))


### OpenSearch k-NN
* Align field visibility across native k-NN search, exact scoring, and explanations to use the wrapped reader's field view ([#3660](https://github.com/opensearch-project/k-NN/pull/3660))

### OpenSearch Security
* Block DLS information leakage via global, multi_terms, and nested aggregations with `min_doc_count: 0` ([#6672](https://github.com/opensearch-project/security/pull/6672))
* Honor field-level security visibility in vector APIs and doc-values metadata ([#6723](https://github.com/opensearch-project/security/pull/6723))
* Reject reserved internal identity prefixes in proxy authenticators ([#6670](https://github.com/opensearch-project/security/pull/6670))

### SQL
* Add configurable match limit for PPL parse regex to prevent catastrophic backtracking ([#5922](https://github.com/opensearch-project/sql/pull/5922))


## MAINTENANCE

### OpenSearch
* Update Netty to 4.1.141.Final ([#23490](https://github.com/opensearch-project/OpenSearch/pull/23490)), ([#23667](https://github.com/opensearch-project/OpenSearch/pull/23667))
* Update OpenTelemetry to 1.67.0 ([#23363](https://github.com/opensearch-project/OpenSearch/pull/23363))
* Update bundled JDK to 21.0.13.1+2 ([#23408](https://github.com/opensearch-project/OpenSearch/pull/23408)), ([#23686](https://github.com/opensearch-project/OpenSearch/pull/23686))
* Bump Jackson to 2.18.12 and zstd-jni to 1.5.7-25, addressing multiple CVEs ([#23629](https://github.com/opensearch-project/OpenSearch/pull/23629))

### OpenSearch Anomaly Detection
* Bump urllib3 version to 2.7.0 in dataGeneration ([#1794](https://github.com/opensearch-project/anomaly-detection/pull/1794))

### OpenSearch Custom Codecs
* Update zstd-jni to 1.5.7-25 to align with core ([#393](https://github.com/opensearch-project/custom-codecs/pull/393))

### OpenSearch k-NN
* Upgrade JaCoCo to 0.8.16 and ASM to 9.11.1 to address vulnerable coverage dependencies ([#3670](https://github.com/opensearch-project/k-NN/pull/3670))
* Bump Guava to 33.7.2-jre and failureaccess to 1.0.3 to address reported CVEs ([#3698](https://github.com/opensearch-project/k-NN/pull/3698))

### SQL
* Bump Guava from 32.1.3-jre to 33.7.2-jre to address CVE-2026-102554 ([#5919](https://github.com/opensearch-project/sql/pull/5919))
