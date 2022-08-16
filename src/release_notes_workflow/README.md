#### Components Release Notes Check 

Pulls the latest code to check if the release notes exists and whether new commits have been made based on user passed argument `--date`. Outputs a formated markdown table as follows.

*Usage*
```
./release_notes.sh check manifests/3.0.0/opensearch-3.0.0.yml --date 2022-07-26
```

*Sample Output*
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
* `--output`: To dump the output into an `.md` file, example `--output table.md`).


The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --date             | Shows commit after a specific date.                                     |
| --output           | Saves the table output to user specified file.  		       	       |
| -v, --verbose      | Show more verbose output.                                               |
