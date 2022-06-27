- [Managing OpenSearch Components](#managing-opensearch-components)
  - [Install GH](#install-gh)
  - [Install Meta](#install-meta)
  - [Check Out Components](#check-out-components)
  - [Get Repo Info](#get-repo-info)
  - [Add a New Component](#add-a-new-component)
  - [Create or Update Release Labels](#create-or-update-release-labels)
  - [Create a Release Issue](#create-a-release-issue)
  - [Check for Release Tags](#check-for-release-tags)
  - [Check for Versions and Releases](#check-for-versions-and-releases)

## Managing OpenSearch Components

We use [meta](https://github.com/mateodelnorte/meta) to manage OpenSearch and OpenSearch Dashboards components as a set.

### Install GH

Install and configure GitHub CLI from [cli.github.com/manual/installation](https://cli.github.com/manual/installation). Authenticate with `gh auth login` and ensure that it works, e.g. `gh issue list`.

### Install Meta

```sh
npm install -g meta
```

### Check Out Components

```sh
meta git update
```

Use `meta git pull` to subsequently pull the latest revisions.

### Get Repo Info

```sh
meta gh issue list
```

### Add a New Component

```sh
meta project import new-component git@github.com:opensearch-project/new-component.git
```

### Create or Update Release Labels

Install [ghi](https://github.com/stephencelis/ghi), e.g. `brew install ghi`.

```
meta exec "ghi label 'v1.2.0' -c '#b94c47'"
```

Alternate option if you are having issues with `ghi`:

```
meta exec "gh label create v2.2.0 -c '#537DB0'"
```

When creating a version label for the ongoing release, always create the next version's label as well.

### Create a Release Issue

We create release issues in all component repos that link back to a parent release issue in this repository. 

1. Locate the parent release issue, e.g. [opensearch-build#567](https://github.com/opensearch-project/opensearch-build/issues/567) for version 1.2.
2. Clone the [release template](templates/releases/release_template.md) into a new `release-X.Y.Z.md`, e.g. [release-1.2.0.md](templates/releases/release-1.2.0.md). Update all `REPLACE` tags with actual versions and dates and commit and PR the file.
3. From [components](components), run `meta exec "gh issue create --label v1.2.0 --title 'Release version 1.2' --body-file ../../templates/releases/release-1.2.0.md"`.

### Check for Release Tags

Check whether a tag for version `1.1.0` exists.

```
meta exec "git ls-remote | grep -E 'refs/tags/1.1.0$'"
```

The command will fail and show in red for every repository without a tag.

### Check for Versions and Releases

Check whether a version or a release exists.

```
meta exec "gh release list | grep -E '(1.1.0.*)$'"
```
