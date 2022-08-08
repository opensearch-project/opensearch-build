#### Components Release Notes Check 

Pulls the latest CommitID based on user passed argument `--gitlogdate` and checks if the release notes exists or not. Outputs a formated markdown table and adds a comment to the github issue using passed arguments `--addcomment`, `--gitissuenumber` and `--gittoken`.
```
*Sample Output*
# OpenSearch CommitID(after 2022-07-26) & Release Notes info
|    Repo     |Branch|CommitID|Release Notes|
|-------------|------|--------|-------------|
|OpenSearch   |   2.2|4035bf7 |YES          |
|common-utils |2.x   |7d53102 |NO           |
|job-scheduler|   2.2|a501307 |YES          |
|security     |main  |f7b6fe5 |YES          |
|geospatial   |   2.2|a71475a |YES          |
|k-NN         |2.x   |53185a0 |YES          |
```

The workflow uses the following arguments:
* `--gitlogdate`: To check if commit exists after a specific date (in format yyyy-mm-dd, example 2022-07-26).
* `--addcomment` (Optional): True/False (Default is False).
* `--gitissuenumber` (Optional): Build repo GitHub issue number to add the generated tabel as comment.
* `--gittoken` (Optional): Token used to add the comment on the github issue.

To just output the information in tabel
```
./run_releasenotes_check.sh manifests/2.2.0/opensearch-2.2.0.yml --gitlogdate 2022-07-26 
```

To add the mardown tabel as comment:
```
./run_releasenotes_check.sh manifests/2.2.0/opensearch-2.2.0.yml --gitlogdate 2022-07-26 --addcomment --gitissuenumber 2345 --gittoken $GITHUB_TOKEN
```

