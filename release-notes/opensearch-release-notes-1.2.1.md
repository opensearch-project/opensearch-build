# OpenSearch 1.2.1 Release Notes

## Release Highlights

This patch releases updates the version of Log4j used in OpenSearch to Log4j 2.15.0 as recommended by the advisory in [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). Additionally, this patch release includes an update to Linux version used in the Docker distributions as recommended by [CVE-2021-43527](https://alas.aws.amazon.com/AL2/ALAS-2021-1722.html).

### OpenSearch
* Upgrade to log4j 2.15.0 ([#1698](https://github.com/opensearch-project/OpenSearch/pull/1698))

### OpenSearch Security
* Bumping log4j to 2.15.0 ([#1520](https://github.com/opensearch-project/security/pull/1520))
