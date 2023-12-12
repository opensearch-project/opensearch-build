# OpenSearch and OpenSearch Dashboards 1.3.14 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.14](https://opensearch.org/versions/opensearch-1-3-14.html) includes the following bug fixes, enhancements and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.14.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.14.md).

<h2>ENHANCEMENTS</h2>

<h3>OpenSearch Security</h3>

<ul>
<li>Add early rejection from RestHandler for unauthorized requests (<a href="https://github.com/opensearch-project/security/pull/3675">#3675</a>)</li>
<li>Expanding Authentication with SecurityRequest Abstraction (<a href="https://github.com/opensearch-project/security/pull/3670">#3670</a>)</li>
<li>Adding minimum viable integration tests framework (<a href="https://github.com/opensearch-project/security/pull/3649">#3649</a>)</li>
<li>For read-only tenants filter with allow list (<a href="https://github.com/opensearch-project/security/commit/4e962f22a39b22ee4dd7619bfee72544aaae61b0">4e962f2</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>OpenSearch Security</h3>

<ul>
<li>Prevent OptionalDataException from User data structures (<a href="https://github.com/opensearch-project/security/pull/3725">#3725</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>OpenSearch Security</h3>

<ul>
<li>Update the version of <code>snappy-java</code> to 1.1.10.5 (<a href="https://github.com/opensearch-project/security/pull/3478">#3478</a>)</li>
<li>Update the version of <code>zookeeper</code> to 3.9.1, <code>xmlsec</code> to 2.3.4, and <code>jackson-databind</code> to 2.14.2 (<a href="https://github.com/opensearch-project/security/pull/3800">#3800</a>)</li>
<li>Adds OpenSearch trigger bot to discerning merger list to allow automatic merges (<a href="https://github.com/opensearch-project/security/pull/3474">#3474</a>)</li>
</ul>

<h3>OpenSearch Security Dashboards Plugin</h3>

<ul>
<li>Update <code>yarn.lock</code> file (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1669">#1669</a>)</li>
<li>Bump  <code>debug</code> to <code>4.3.4</code> and <code>browserify-sign</code> to <code>4.2.2</code> to address CVEs (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1674">#1674</a>)</li>
</ul>
