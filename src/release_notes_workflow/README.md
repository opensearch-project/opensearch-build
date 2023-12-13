- [Consolidated Release Notes Automation](#consolidated-release-notes-automation)
  - [Components Release Notes Check](#components-release-notes-check)
  - [Consolidated Release Notes](#consolidated-release-notes)

## Consolidated Release Notes

### Components Release Notes Check 

Pulls the latest code to check if the release notes exists and whether new commits have been made based on user passed argument `--date`. Outputs a formated markdown table as follows.

#### Usage
```
./release_notes.sh check manifests/3.0.0/opensearch-3.0.0.yml --date 2022-07-26
```

#### Sample Output
```
#  OpenSearch CommitID(after 2022-07-26) & Release Notes info
|          Repo           |   Branch   |CommitID|Commit Date|Release Notes|
|-------------------------|------------|--------|-----------|-------------|
|OpenSearch               |tags/2.2.0  |b1017fa |2022-08-08 |True         |
|common-utils             |tags/2.2.0.0|7d53102 |2022-08-04 |False        |
|job-scheduler            |tags/2.2.0.0|a501307 |2022-08-02 |True         |
|ml-commons               |tags/2.2.0.0|a7d2695 |2022-08-08 |True         |
|performance-analyzer     |tags/2.2.0.0|3a75d7d |2022-08-08 |True         |
|security                 |tags/2.2.0.0|8e9e583 |2022-08-08 |True         |
|geospatial               |tags/2.2.0.0|a71475a |2022-08-04 |True         |
|k-NN                     |tags/2.2.0.0|53185a0 |2022-08-04 |True         |
|cross-cluster-replication|tags/2.2.0.0|14d871a |2022-08-05 |False        |
```

The workflow uses the following arguments:
* `--date`: To check if commit exists after a specific date (in format yyyy-mm-dd, example 2022-07-26).
* `--output`: To dump the output into an `.md` file, example `--output table.md`.


The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --date             | Shows commit after a specific date.                                     |
| --output           | Saves the table output to user specified file.  		       	       |
| -v, --verbose      | Show more verbose output.                                               |

### Consolidated Release Notes

This workflow generates a consolidated release notes for all the components. 
It utilizes the output from the preceding step to compile these consolidated release notes. If the preceding step hasn't been executed, it will automatically run that step first before generating the consolidated release notes. 

#### Usage
```
./release_notes.sh compile manifests/3.0.0/opensearch-3.0.0.yml --date 2022-07-26
```

#### Sample Output
Two output files are generated:
- Markdown table containing links to individual components' release notes for quick reference (Example: `release_notes_table-2.10.0.md`)
- Consolidated release notes for all the components (Example: `release_notes-2.10.0.md`)

<details> 
<summary>Markdown table with links</summary>

#  OpenSearch CommitID(after 2022-07-26) & Release Notes info
|          Repo           |    Branch     |CommitID|Commit Date|Release Notes Exists|                                                                                URL                                                                                 |
|-------------------------|---------------|--------|-----------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|alerting                 |[tags/2.10.0.0]|dc1b9bf |2023-09-18 |True                |https://raw.githubusercontent.com/opensearch-project/alerting/2.10.0.0/release-notes/opensearch-alerting.release-notes-2.10.0.0.md                                  |
|anomaly-detection        |[tags/2.10.0.0]|bc4d8b1 |2023-09-08 |True                |https://raw.githubusercontent.com/opensearch-project/anomaly-detection/2.10.0.0/release-notes/opensearch-anomaly-detection.release-notes-2.10.0.0.md                |
|asynchronous-search      |[tags/2.10.0.0]|a312d9a |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/asynchronous-search/2.10.0.0/release-notes/opensearch-asynchronous-search.release-notes-2.10.0.0.md            |
|common-utils             |[tags/2.10.0.0]|0352c2f |2023-09-08 |True                |https://raw.githubusercontent.com/opensearch-project/common-utils/2.10.0.0/release-notes/opensearch-common-utils.release-notes-2.10.0.0.md                          |
|cross-cluster-replication|[tags/2.10.0.0]|dee2f60 |2023-09-08 |True                |https://raw.githubusercontent.com/opensearch-project/cross-cluster-replication/2.10.0.0/release-notes/opensearch-cross-cluster-replication.release-notes-2.10.0.0.md|
|custom-codecs            |[tags/2.10.0.0]|3437b43 |2023-09-15 |True                |https://raw.githubusercontent.com/opensearch-project/custom-codecs/2.10.0.0/release-notes/opensearch-custom-codecs.release-notes-2.10.0.0.md                        |
|geospatial               |[tags/2.10.0.0]|a3da222 |2023-09-12 |True                |https://raw.githubusercontent.com/opensearch-project/geospatial/2.10.0.0/release-notes/opensearch-geospatial.release-notes-2.10.0.0.md                              |
|index-management         |[tags/2.10.0.0]|062badd |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/index-management/2.10.0.0/release-notes/opensearch-index-management.release-notes-2.10.0.0.md                  |
|job-scheduler            |[tags/2.10.0.0]|e9d3637 |2023-09-12 |True                |https://raw.githubusercontent.com/opensearch-project/job-scheduler/2.10.0.0/release-notes/opensearch.job-scheduler.release-notes-2.10.0.0.md                        |
|k-NN                     |[tags/2.10.0.0]|e437016 |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/k-NN/2.10.0.0/release-notes/opensearch-knn.release-notes-2.10.0.0.md                                           |
|ml-commons               |[tags/2.10.0.0]|521214b |2023-09-13 |True                |https://raw.githubusercontent.com/opensearch-project/ml-commons/2.10.0.0/release-notes/opensearch-ml-common.release-notes-2.10.0.0.md                               |
|neural-search            |[tags/2.10.0.0]|9476d43 |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/neural-search/2.10.0.0/release-notes/opensearch-neural-search.release-notes-2.10.0.0.md                        |
|notifications            |[tags/2.10.0.0]|0a9dfb0 |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/notifications/2.10.0.0/release-notes/opensearch-notifications.release-notes-2.10.0.0.md                        |
|opensearch-observability |[tags/2.10.0.0]|d2c087c |2023-09-13 |True                |https://raw.githubusercontent.com/opensearch-project/observability/2.10.0.0/release-notes/opensearch-observability.release-notes-2.10.0.0.md                        |
|opensearch-reports       |[tags/2.10.0.0]|3095e3c |2023-09-13 |True                |https://raw.githubusercontent.com/opensearch-project/reporting/2.10.0.0/release-notes/opensearch-reporting.release-notes-2.10.0.0.md                                |
|performance-analyzer     |[tags/2.10.0.0]|3ee56fc |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/performance-analyzer/2.10.0.0/release-notes/opensearch-performance-analyzer.release-notes-2.10.0.0.md          |
|security                 |[tags/2.10.0.0]|6daa697 |2023-09-12 |True                |https://raw.githubusercontent.com/opensearch-project/security/2.10.0.0/release-notes/opensearch-security.release-notes-2.10.0.0.md                                  |
|security-analytics       |[tags/2.10.0.0]|e005b5a |2023-09-19 |True                |https://raw.githubusercontent.com/opensearch-project/security-analytics/2.10.0.0/release-notes/opensearch-security-analytics.release-notes-2.10.0.0.md              |
|sql                      |[tags/2.10.0.0]|ef18b38 |2023-09-07 |True                |https://raw.githubusercontent.com/opensearch-project/sql/2.10.0.0/release-notes/opensearch-sql.release-notes-2.10.0.0.md                                            |

</details>

---

The workflow uses the following arguments:
* `--date`: To check if commit exists after a specific date (in format yyyy-mm-dd, example 2022-07-26). This is optional if the previous step is already run.
* `--output`: To dump the consolidated release notes into an `.md` file, example `--output table.md`.


The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --date             | Shows commit after a specific date.                                     |
| --output           | Saves the release notes to user specified file.  		       	       |
| -v, --verbose      | Show more verbose output.                                               |
