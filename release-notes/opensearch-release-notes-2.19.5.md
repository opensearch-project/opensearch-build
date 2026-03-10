# OpenSearch and OpenSearch Dashboards 2.19.5 Release Notes


## BUG FIXES


### OpenSearch Security


* [2.19] Fix issue serializing user to threadcontext when userRequestedTenant is null ([#5925](https://github.com/opensearch-project/security/pull/5925))
* Fix ConcurrentModificationException for SecurityRoles for 2.x ([#5860](https://github.com/opensearch-project/security/pull/5860))


### OpenSearch Security Analytics


* Fix bug when deleting detector with 0 rules. ([#1648](https://github.com/opensearch-project/security-analytics/pull/1648))


## INFRASTRUCTURE


### OpenSearch Common Utils


* Adjust shadowJar name. ([#909](https://github.com/opensearch-project/common-utils/pull/909))


### OpenSearch Custom Codecs


* Fix Github Actions MacOS checks ([#298](https://github.com/opensearch-project/custom-codecs/pull/298))


### OpenSearch Job Scheduler


* [2.19] Change com.github.johnrengelman.shadow to com.gradleup.shadow ([#888](https://github.com/opensearch-project/job-scheduler/pull/888))


### OpenSearch Security


* [Backport 2.19] Enable mend remediate to create PRs ([#5784](https://github.com/opensearch-project/security/pull/5784))


## MAINTENANCE


### OpenSearch Common Utils


* [Backport 2.19] Bump logback from 1.5.19 to 1.5.32 ([#905](https://github.com/opensearch-project/common-utils/pull/905))


### OpenSearch Security


* [2.19] Bump commons-text to 1.15.0 and log4j-core to 2.25.3 ([#5974](https://github.com/opensearch-project/security/pull/5974))
* [Backport 2.19] Bump org.lz4:lz4-java from 1.8.0 to 1.10.1 ([#5970](https://github.com/opensearch-project/security/pull/5970))


### OpenSearch Skills


* [AUTO] Increment version to 2.19.5-SNAPSHOT ([#684](https://github.com/opensearch-project/skills/pull/684))


## REFACTORING


### OpenSearch Security


* Use RestRequestFilter.getFilteredRequest to declare sensitive API params ([#5710](https://github.com/opensearch-project/security/pull/5710))


