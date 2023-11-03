<h1>OpenSearch and OpenSearch Dashboards 2.8.0 Release Notes</h1>
<h2>FEATURES</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>integrate security-analytics &amp; alerting for correlation engine. (<a href="https://github.com/opensearch-project/alerting/pull/878">#878</a>)</li>
<li>DocLevel Monitor - generate findings when 0 triggers. (<a href="https://github.com/opensearch-project/alerting/pull/856">#856</a>)</li>
<li>DocLevelMonitor Error Alert - rework. (<a href="https://github.com/opensearch-project/alerting/pull/892">#892</a>)</li>
<li>Update endtime for DocLevelMonitor Error State Alerts and move them to history index when monitor execution succeeds. (<a href="https://github.com/opensearch-project/alerting/pull/905">#905</a>)</li>
<li>log error messages and clean up monitor when indexing doc level queries or metadata creation fails. (<a href="https://github.com/opensearch-project/alerting/pull/900">#900</a>)</li>
<li>Adds transport layer actions for CRUD workflows. (<a href="https://github.com/opensearch-project/alerting/pull/934">#934</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Support notification integration with long running operations. (<a href="https://github.com/opensearch-project/index-management/pull/712">#712</a>, <a href="https://github.com/opensearch-project/index-management/pull/722">#722</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Identify extension Transport requests and permit handshake and extension registration actions (<a href="https://github.com/opensearch-project/security/pull/2599">#2599</a>)</li>
<li>Use ExtensionsManager.lookupExtensionSettingsById when verifying extension unique id (<a href="https://github.com/opensearch-project/security/pull/2749">#2749</a>)</li>
<li>Generate auth tokens for service accounts (<a href="https://github.com/opensearch-project/security/pull/2716">#2716</a>)</li>
<li>Security User Refactor (<a href="https://github.com/opensearch-project/security/pull/2594">#2594</a>)</li>
<li>Add score based password verification (<a href="https://github.com/opensearch-project/security/pull/2557">#2557</a>)</li>
<li>Usage of JWKS with JWT (w/o OpenID connect) (<a href="https://github.com/opensearch-project/security/pull/2808">#2808</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Support for pagination in v2 engine of SELECT * FROM &lt;table&gt; queries (<a href="https://github.com/opensearch-project/sql/pull/1666">#1666</a>)</li>
<li>Support Alternate Datetime Formats (<a href="https://github.com/opensearch-project/sql/pull/1664">#1664</a>)</li>
<li>Create new anonymizer for new engine (<a href="https://github.com/opensearch-project/sql/pull/1665">#1665</a>)</li>
<li>Add Support for Nested Function Use In WHERE Clause Predicate Expresion (<a href="https://github.com/opensearch-project/sql/pull/1657">#1657</a>)</li>
<li>Cross cluster search in PPL (<a href="https://github.com/opensearch-project/sql/pull/1512">#1512</a>)</li>
<li>Added COSH to V2 engine (<a href="https://github.com/opensearch-project/sql/pull/1428">#1428</a>)</li>
<li>REST API for GET,PUT and DELETE (<a href="https://github.com/opensearch-project/sql/pull/1482">#1482</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>integrate security-analytics &amp; alerting for correlation engine. (<a href="https://github.com/opensearch-project/common-utils/pull/412">#412</a>)</li>
<li>NoOpTrigger. (<a href="https://github.com/opensearch-project/common-utils/pull/420">#420</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>add correlation engine for security-analytics. (<a href="https://github.com/opensearch-project/security-analytics/pull/405">#405</a>)</li>
<li>SearchRule API - source filtering. (<a href="https://github.com/opensearch-project/security-analytics/pull/374">#374</a>)</li>
<li>Alias and dataStream end-to-end ITs. (<a href="https://github.com/opensearch-project/security-analytics/pull/373">#373</a>)</li>
<li>add rules to correlations for correlation engine. (<a href="https://github.com/opensearch-project/security-analytics/pull/423">#423</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Add a setting to enable/disable model url in register API (<a href="https://github.com/opensearch-project/ml-commons/pull/871">#871</a>)</li>
<li>Add a setting to enable/disable local upload while registering model (<a href="https://github.com/opensearch-project/ml-commons/pull/873">#873</a>)</li>
<li>Check hash value for the pretrained models (<a href="https://github.com/opensearch-project/ml-commons/pull/878">#878</a>)</li>
<li>Add pre-trained model list (<a href="https://github.com/opensearch-project/ml-commons/pull/883">#883</a>)</li>
<li>Add content hash value for the correlation model. (<a href="https://github.com/opensearch-project/ml-commons/pull/885">#885</a>)</li>
<li>Set default access_control_enabled setting to false (<a href="https://github.com/opensearch-project/ml-commons/pull/935">#935</a>)</li>
<li>Enable model access control in secure reset IT (<a href="https://github.com/opensearch-project/ml-commons/pull/940">#940</a>)</li>
<li>Add model group rest ITs (<a href="https://github.com/opensearch-project/ml-commons/pull/942">#942</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Add default roles for SQL plugin: PPL and cross-cluster search (<a href="https://github.com/opensearch-project/security/pull/2729">#2729</a>)</li>
<li>Update security-analytics roles to add correlation engine apis (<a href="https://github.com/opensearch-project/security/pull/2732">#2732</a>)</li>
<li>Changes in role.yml for long-running operation notification feature in Index-Management repo (<a href="https://github.com/opensearch-project/security/pull/2789">#2789</a>)</li>
<li>Rest admin permissions (<a href="https://github.com/opensearch-project/security/pull/2411">#2411</a>)</li>
<li>Separate config option to enable restapi: permissions (<a href="https://github.com/opensearch-project/security/pull/2605">#2605</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Minor clean up of datetime and other classes (<a href="https://github.com/opensearch-project/sql/pull/1310">#1310</a>)</li>
<li>Add integration JDBC tests for cursor/fetch_size feature (<a href="https://github.com/opensearch-project/sql/pull/1315">#1315</a>)</li>
<li>Refactoring datasource changes to a new module. (<a href="https://github.com/opensearch-project/sql/pull/1504">#1504</a>)</li>
</ul>

<h3>Opensearch Cross Cluster Replication</h3>

<ul>
<li>Support CCR for k-NN enabled indices (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/760">#760</a>)</li>
</ul>

<h3>Opensearch Knn</h3>

<ul>
<li>Bulk allocate objects for nmslib index creation to avoid malloc fragmentation (<a href="https://github.com/opensearch-project/k-NN/pull/773">#773</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Fix getAlerts API for standard Alerting monitors. (<a href="https://github.com/opensearch-project/alerting/issues/870">#870</a>)</li>
<li>Fixed a bug that prevented alerts from being generated for doc level monitors that use wildcard characters in index names. (<a href="https://github.com/opensearch-project/alerting/issues/894">#894</a>)</li>
<li>revert to deleting monitor metadata after deleting doc level queries to fix delete monitor regression. (<a href="https://github.com/opensearch-project/alerting/issues/931">#931</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>fix guava jar hell issue (<a href="https://github.com/opensearch-project/observability/pull/1536">#1536</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Fix class not found exception when deserialize model (<a href="https://github.com/opensearch-project/ml-commons/pull/899">#899</a>)</li>
<li>Fix publish shadow publication dependency issue (<a href="https://github.com/opensearch-project/ml-commons/pull/919">#919</a>)</li>
<li>Fix model group index not existing model version query issue and SecureMLRestIT failure ITs (<a href="https://github.com/opensearch-project/ml-commons/pull/933">#933</a>)</li>
<li>Fix model access mode upper case bug (<a href="https://github.com/opensearch-project/ml-commons/pull/937">#937</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Remove recursion call when checking permission on indices. (<a href="https://github.com/opensearch-project/index-management/pull/779">#779</a>)</li>
<li>Added trimming of nanos part of &quot;epoch_millis&quot; timestamp when date_histogram type used is date_nanos. (<a href="https://github.com/opensearch-project/index-management/pull/772">#772</a>)</li>
<li>Added proper resolving of sourceIndex inside RollupInterceptor, it's required for QueryStringQuery parsing. (<a href="https://github.com/opensearch-project/index-management/pull/773">#773</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Fix ShardStateCollector which was impacted by <a href="https://github.com/opensearch-project/OpenSearch/pull/7301">core refactoring</a> <a href="https://github.com/opensearch-project/performance-analyzer/pull/445">445</a></li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li><code>deserializeSafeFromHeader</code> uses <code>context.getHeader(headerName)</code> instead of <code>context.getHeaders()</code> (<a href="https://github.com/opensearch-project/security/pull/2768">#2768</a>)</li>
<li>Fix multitency config update (<a href="https://github.com/opensearch-project/security/pull/2758">#2758</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Fixing bug where Nested functions used in WHERE, GROUP BY, HAVING, and ORDER BY clauses don't fallback to legacy engine. (<a href="https://github.com/opensearch-project/sql/pull/1549">#1549</a>)</li>
</ul>

<h3>Opensearch Cross Cluster Replication</h3>

<ul>
<li>Handle serialization issues with UpdateReplicationStateDetailsRequest (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/866">#866</a>)</li>
<li>Two followers using same remote alias can result in replication being auto-paused (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/833">#833</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Update json version to 20230227 (<a href="https://github.com/opensearch-project/reporting/pull/692">#692</a>)</li>
<li>Update Gradle Wrapper to 7.6.1 (<a href="https://github.com/opensearch-project/reporting/pull/695">#695</a>)</li>
<li>Removing guava dependency to fix jarhell (<a href="https://github.com/opensearch-project/reporting/pull/709">#709</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Findings index mappings fix. (<a href="https://github.com/opensearch-project/security-analytics/pull/409">#409</a>)</li>
<li>fix for input validation of correlation rule names. (<a href="https://github.com/opensearch-project/security-analytics/pull/428">#428</a>)</li>
<li>fix for failure in syslogs mappings view api. (<a href="https://github.com/opensearch-project/security-analytics/pull/435">#435</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Modify the default values in the bindle file to make them consistent with the values in code (<a href="https://github.com/opensearch-project/notifications/pull/672">#672</a>)</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>Opensearch Observability</h3>

<ul>
<li>Update Gradle Wrapper to 7.6.1 (<a href="https://github.com/opensearch-project/observability/pull/1512">#1512</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Bump gradle version to 8.1.1 (<a href="https://github.com/opensearch-project/neural-search/pull/169">#169</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Upgrade gradle to 7.6.1, upgrade gradle test-retry plugin to 1.5.2. (<a href="https://github.com/opensearch-project/performance-analyzer/pull/438">#438</a>)</li>
<li>Introduce protobuf and guava dependency from core versions file <a href="https://github.com/opensearch-project/performance-analyzer/pull/437">#437</a></li>
<li>Update dependency org.xerial:sqlite-jdbc to v3.41.2.2 <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/375">#375</a></li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Partial Cherry-pick of #886 from anomaly-detection and Additional Adjustments. (<a href="https://github.com/opensearch-project/anomaly-detection/pull/914">#914</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Make jacoco report to be generated faster in local (<a href="https://github.com/opensearch-project/geospatial/pull/267">#267</a>)</li>
<li>Exclude lombok generated code from jacoco coverage report (<a href="https://github.com/opensearch-project/geospatial/pull/268">#268</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Switch publish maven branches to list. (<a href="https://github.com/opensearch-project/common-utils/pull/423">#423</a>)</li>
</ul>

<h3>Opensearch Knn</h3>

<ul>
<li>Bump requests version from 2.26.0 to 2.31.0 (<a href="https://github.com/opensearch-project/k-NN/pull/913">#913</a>)</li>
<li>Disable index refresh for system indices (<a href="https://github.com/opensearch-project/k-NN/pull/915">#773</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Upgrade gradle version to 8.1.1 (<a href="https://github.com/opensearch-project/notifications/pull/663">#663</a>)</li>
<li>Fix gradle run failed on windows platform and fix weak password test failure (<a href="https://github.com/opensearch-project/notifications/pull/684">#684</a>)</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Added 2.8 release notes. (<a href="https://github.com/opensearch-project/alerting/pull/939">#939</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<h3>Documentation</h3>

<h3>Opensearch Index Management</h3>

<ul>
<li>Added 2.8 release notes. (<a href="https://github.com/opensearch-project/index-management/pull/794">#794</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Add Nested Documentation for 2.7 Related Features (<a href="https://github.com/opensearch-project/sql/pull/1620">#1620</a>)</li>
<li>Update usage example doc for PPL cross-cluster search (<a href="https://github.com/opensearch-project/sql/pull/1610">#1610</a>)</li>
<li>Documentation and other papercuts for datasource api launch (<a href="https://github.com/opensearch-project/sql/pull/1530">#1530</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Added 2.8 release notes. (<a href="https://github.com/opensearch-project/common-utils/pull/441">#441</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Added 2.8.0 release notes. (<a href="https://github.com/opensearch-project/security-analytics/pull/444">#444</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Add 2.8.0 release notes (<a href="https://github.com/opensearch-project/notifications/pull/682">#682</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Baseline codeowners and maintainers. (<a href="https://github.com/opensearch-project/alerting/pull/818">#818</a>)</li>
<li>upgrade gradle to 8.1.1. (<a href="https://github.com/opensearch-project/alerting/pull/893">#893</a>)</li>
<li>Update codeowners and maintainers. (<a href="https://github.com/opensearch-project/alerting/pull/899">#899</a>)</li>
<li>Updating the CODEOWNERS file with the right format. (<a href="https://github.com/opensearch-project/alerting/pull/911">#911</a>)</li>
<li>Compile fix - Strings package change. (<a href="https://github.com/opensearch-project/alerting/pull/924">#924</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Increment version to 2.8.0-SNAPSHOT (<a href="https://github.com/opensearch-project/observability/pull/1505">#1505</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Increment version to 2.8.0-SNAPSHOT (<a href="https://github.com/opensearch-project/ml-commons/pull/896">#896</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Upgrade to gradle 8.1.1. (<a href="https://github.com/opensearch-project/index-management/pull/777">#777</a>)</li>
<li>Bump version to 2.8. (<a href="https://github.com/opensearch-project/index-management/pull/759">#759</a>)</li>
</ul>

<h3>Opensearch.job Scheduler</h3>

<ul>
<li>Consuming breaking changes from moving ExtensionActionRequest (<a href="https://github.com/opensearch-project/job-scheduler/pull/381">#381</a>)</li>
<li>Fix the Maven publish (<a href="https://github.com/opensearch-project/job-scheduler/pull/379">#379</a>)</li>
<li>Fixes issue with publishing Job Scheduler artifacts to correct maven coordinates (<a href="https://github.com/opensearch-project/job-scheduler/pull/377">#377</a>)</li>
<li>Bumping JS main BWC test version for sample extension plugin to 2.8 (<a href="https://github.com/opensearch-project/job-scheduler/pull/371">#371</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update RestController constructor for tests <a href="https://github.com/opensearch-project/performance-analyzer/pull/440">#440</a></li>
<li>Dependencies change in favor of Commons repo <a href="https://github.com/opensearch-project/performance-analyzer/pull/448">#448</a></li>
<li>WriterMetrics and config files dependency redirection <a href="https://github.com/opensearch-project/performance-analyzer/pull/450">#450</a></li>
<li>Refactor code related to Commons change, fixing unit tests <a href="https://github.com/opensearch-project/performance-analyzer/pull/451">#451</a></li>
<li>Remove remaining dependencies from PA-RCA due to commons repo <a href="https://github.com/opensearch-project/performance-analyzer/pull/453">#453</a></li>
<li>Fix BWC Integration tests <a href="https://github.com/opensearch-project/performance-analyzer/pull/413">#413</a></li>
<li>Fix SHA update for PA-Commons repo in build.gradle  <a href="https://github.com/opensearch-project/performance-analyzer/pull/454">#454</a></li>
<li>Refactor Service/Stat Metrics <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/376">#376</a></li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Update to Gradle 8.1.1 (<a href="https://github.com/opensearch-project/security/pull/2738">#2738</a>)</li>
<li>Upgrade spring-core from 5.3.26 to 5.3.27 (<a href="https://github.com/opensearch-project/security/pull/2717">#2717</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Fix IT - address breaking changes from upstream. (<a href="https://github.com/opensearch-project/sql/pull/1659">#1659</a>)</li>
<li>Increment version to 2.8.0-SNAPSHOT (<a href="https://github.com/opensearch-project/sql/pull/1552">#1552</a>)</li>
<li>Backport maintainer list update to <code>2.x</code>. (<a href="https://github.com/opensearch-project/sql/pull/1650">#1650</a>)</li>
<li>Backport jackson and gradle update from #1580 to 2.x (<a href="https://github.com/opensearch-project/sql/pull/1596">#1596</a>)</li>
<li>adding reflections as a dependency (<a href="https://github.com/opensearch-project/sql/pull/1596">#1559</a>)</li>
<li>Bump org.json dependency version (<a href="https://github.com/opensearch-project/sql/pull/1586">#1586</a>)</li>
<li>Integ Test Fix (<a href="https://github.com/opensearch-project/sql/pull/1541">#1541</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Increment version to 2.8.0-SNAPSHOT (<a href="https://github.com/opensearch-project/reporting/pull/688">#688</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Change package for Strings.hasText (<a href="https://github.com/opensearch-project/geospatial/pull/314">#314</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>upgrade gradle to 8.1.1. (<a href="https://github.com/opensearch-project/common-utils/pull/418">#418</a>)</li>
<li>Sync up MAINTAINERS to CODEOWNERS. (<a href="https://github.com/opensearch-project/common-utils/pull/427">#427</a>)</li>
<li>Fix build errors after refactoring of Strings class in core. (<a href="https://github.com/opensearch-project/common-utils/pull/432">#432</a>)</li>
<li>updating maintainers and codeowners. (<a href="https://github.com/opensearch-project/common-utils/pull/438">#438</a>)</li>
<li>fix codeowners file format. (<a href="https://github.com/opensearch-project/common-utils/pull/440">#440</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Updating maintainers file (<a href="https://github.com/opensearch-project/asynchronous-search/pull/275">275</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fixed compile issues related to latest OS core repo changes. (<a href="https://github.com/opensearch-project/security-analytics/pull/412">#412</a>)</li>
<li>Moved CODEOWNERS files to align with org requirements. (<a href="https://github.com/opensearch-project/security-analytics/pull/418">#418</a>)</li>
<li>Update CODEOWNERS. (<a href="https://github.com/opensearch-project/security-analytics/pull/434">#434</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>[AUTO] Increment version to 2.8.0-SNAPSHOT (<a href="https://github.com/opensearch-project/notifications/pull/657">#657</a>)</li>
</ul>

<h2>REFACTORING</h2>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Change mem_size_estimation to memory_size_estimation (<a href="https://github.com/opensearch-project/ml-commons/pull/868">#868</a>)</li>
</ul>

<h2>EXPERIMENTAL</h2>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Model access control. (<a href="https://github.com/opensearch-project/ml-commons/pull/928">#928</a>)</li>
</ul>

<h2>ADDED [NEW CATEGORY]</h2>
<h3>Opensearch.job Scheduler</h3>
<ul>
<li>Add auto-release github workflow (<a href="https://github.com/opensearch-project/job-scheduler/pull/385">#385</a>)</li>
</ul>

