#### Components Release Notes Check 

Pulls the latest CommitID based on user passed argument `--date` and checks if the release notes exists or not. Outputs a formated markdown table as follows.

*Usage*
```
./release_notes.sh check manifests/3.0.0/opensearch-3.0.0.yml --date 2022-07-26
```

*Sample Output*
```
# OpenSearch CommitID(after 2022-07-26) & Release Notes info
|    Repo    |Branch|CommitID|Commit Date|Release Notes|
|------------|------|--------|-----------|-------------|
|OpenSearch  |main  |7dad063 |2022-08-10 |NO           |
|common-utils|main  |b82ef4a |2022-08-09 |NO           |
```

The workflow uses the following arguments:
* `--date`: To check if commit exists after a specific date (in format yyyy-mm-dd, example 2022-07-26).


The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --date             | Shows commit after a specific date.                                     |
| --save             | Saves the table output to table.md.                                     |
| -v, --verbose      | Show more verbose output.                                               |