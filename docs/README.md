### How is the Wiki Updated?
This repository's [Github Wiki](https://github.com/opensearch-project/opensearch-build/wiki) utilizes the [github-wiki-action](https://github.com/Andrew-Chen-Wang/github-wiki-action) action via [publish-wiki.yml](../.github/workflows/publish-wiki.yml) workflow. This workflow mirrors the [docs](https://github.com/opensearch-project/opensearch-build/tree/main/docs) folder within opensearch-build onto the Wiki.

With this workflow, the documentation within this repository can be organized within the Wiki tab, while maintaining the ability for contributors to submit reviewable documentation updates in the form of pull requests.

### Submit a change to the Wiki
To submit a documentation update, update the markdown files within the [docs](https://github.com/opensearch-project/opensearch-build/tree/main/docs) folder accordingly, or create new files using the naming convention specified by the [workflow](https://github.com/Andrew-Chen-Wang/github-wiki-action) .

To test your changes, you can fork this repository. Committing and pushing changes to the docs folder of your fork's main branch will run the workflow and update the fork's Wiki page.

Finally, create a pull request containing the changes. Adding a link to your fork's Wiki page within the pull request will help reviewers understand your changes.
