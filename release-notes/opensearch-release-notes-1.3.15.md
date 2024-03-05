# OpenSearch and OpenSearch Dashboards 1.3.15 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.15](https://opensearch.org/versions/opensearch-1-3-15.html) includes the following bug fixes, enhancements and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.15.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.15.md).

<h2>SECURITY FIXES</h2>

<h3>OpenSearch Cross Cluster Replication</h3>

<ul>
<li>Changed version of ipaddress library to 5.4.1 for OS 1.3 (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/1339">#1339</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>OpenSearch SQL</h3>

<ul>
<li>Bump json and wiremock version to fix CVEs (<a href="https://github.com/opensearch-project/sql/pull/2533">#2533</a>)</li>
</ul>

<h3>OpenSearch Dashboards Reporting</h3>

<ul>
<li>Bump dependencies to fix cve (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/320">#320</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>OpenSearch Alerting</h3>

<ul>
<li>Adjusted dependency versions to address CVEs (<a href="https://github.com/opensearch-project/alerting/pull/1447">#1447</a>)</li>
</ul>

<h3>OpenSearch Common Utils</h3>

<ul>
<li>Forced ktlint to use logback-core:1.2.13, and logback-classic:1.2.13 to address CVE (<a href="https://github.com/opensearch-project/common-utils/pull/602">#602</a>)</li>
</ul>

<h3>OpenSearch Alerting Dashboards Plugin</h3>

<ul>
<li>Fixed bunch of CVEs by updating package versions and bumped plugin version (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/893">#893</a>)</li>
</ul>
