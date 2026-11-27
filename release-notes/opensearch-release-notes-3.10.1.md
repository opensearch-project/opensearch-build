# OpenSearch 3.10.1 and OpenSearch Dashboards 3.10.0 Release Notes

## Release Details
[OpenSearch and OpenSearch Dashboards 3.10.1](https://opensearch.org/artifacts/by-version/#release-3-10-1) includes the following bug fix and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.10.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.10.0.md).


## BUG FIXES

### OpenSearch
* Fix scripted source reads failing on compound segments due to Java agent denying file open ([#23692](https://github.com/opensearch-project/OpenSearch/pull/23692))


## MAINTENANCE


### OpenSearch
* Update Reactor Netty to 1.3.9 and Project Reactor to 3.8.9 ([#23689](https://github.com/opensearch-project/OpenSearch/pull/23689))
* Update bundled JDK to 25.0.5.1+2 for all distributions ([#23684](https://github.com/opensearch-project/OpenSearch/pull/23684)), ([#23732](https://github.com/opensearch-project/OpenSearch/pull/23732))


### OpenSearch ML Commons
* Update ml-commons to use teams-based maintainers access ([#5237](https://github.com/opensearch-project/ml-commons/pull/5237))
