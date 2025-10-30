# OpenSearch 3.3.2 and OpenSearch Dashboards 3.3.0 Release Notes

## Release Highlights
Includes maintenance changes and bug fixes for the OpenSearch core engine and ML Commons, Neural Search, Skills, k-NN and Security plugins.

## Release Details
[OpenSearch 3.3.2](https://opensearch.org/artifacts/by-version/#release-3-3-2) includes the following bug fix updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.3.2.md).


## FEATURES


### OpenSearch ML Commons


* Nova mme support ([#4368](https://github.com/opensearch-project/ml-commons/pull/4368))


## ENHANCEMENTS


### OpenSearch ML Commons


* Support MCP connector in agent update API ([#4352](https://github.com/opensearch-project/ml-commons/pull/4352))
* Add refresh policy; add checkpoint id field ([#4305](https://github.com/opensearch-project/ml-commons/pull/4305))


### OpenSearch Neural Search


* [Agentic Search] Add conversation search support with agentic search ([#1626](https://github.com/opensearch-project/neural-search/pull/1626))
* [Agentic Search] Extract JSON from Agent Response ([#1631](https://github.com/opensearch-project/neural-search/pull/1631))
* [Agentic Search] Extract agent summary based on models ([#1633](https://github.com/opensearch-project/neural-search/pull/1633))


## BUG FIXES


### OpenSearch Core Engine
* Fix issue with updating core with a patch number other than 0 ([#19377](https://github.com/opensearch-project/OpenSearch/pull/19377))
* Fix IndexOutOfBoundsException when running include/exclude on non-existent prefix in terms aggregations ([#19637](https://github.com/opensearch-project/OpenSearch/pull/19637))
* Add S3Repository.LEGACY_MD5_CHECKSUM_CALCULATION to list of repository-s3 settings ([#19789](https://github.com/opensearch-project/OpenSearch/pull/19789))



### OpenSearch k-NN


* Do not apply memory optimized search for old indices. ([#2918](https://github.com/opensearch-project/k-NN/pull/2918))


### OpenSearch ML Commons


* [Agentic Search] Add extract JSON processor in Query Planning Tool ([#4356](https://github.com/opensearch-project/ml-commons/pull/4356))
* Add name validation to index prefix ([#4332](https://github.com/opensearch-project/ml-commons/pull/4332))
* Fix CVE-2025-58057 ([#4338](https://github.com/opensearch-project/ml-commons/pull/4338))
* Fix unsupported operation exception in execute tool API ([#4325](https://github.com/opensearch-project/ml-commons/pull/4325))
* Fixing regex bypass issue ([#4336](https://github.com/opensearch-project/ml-commons/pull/4336))
* Fix when return\_history is true ([#4310](https://github.com/opensearch-project/ml-commons/pull/4310))
* Use filtered output in agent tool response streaming ([#4335](https://github.com/opensearch-project/ml-commons/pull/4335))
* Combine json chunks from requests ([#4317](https://github.com/opensearch-project/ml-commons/pull/4317))


### OpenSearch Remote Metadata SDK


* Upgrading netty codec version to match with OpenSearch Core Engine ([#273](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/273))


### OpenSearch Security


* Create a WildcardMatcher.NONE when creating a WildcardMatcher with an empty string ([#5694](https://github.com/opensearch-project/security/pull/5694))
* Add security provider earlier in bootstrap process ([#5749](https://github.com/opensearch-project/security/pull/5749))


### OpenSearch Skills


* Fix regex bypass issue ([#656](https://github.com/opensearch-project/skills/pull/656))


## MAINTENANCE


### OpenSearch Core Engine
* Bump ch.qos.logback modules from 1.5.18 to 1.5.20 in HDFS test fixture ([#19764](https://github.com/opensearch-project/OpenSearch/pull/19764))
* Bump org.bouncycastle:bc-fips from 2.1.1 to 2.1.2 ([#19817](https://github.com/opensearch-project/OpenSearch/pull/19817))

