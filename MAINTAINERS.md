- [Overview](#overview)
- [Current Maintainers](#current-maintainers)
- [Emeritus Maintainers](#Emeritus-maintainers)
- [Release Owner](#release-owner)
  - [Release Activities](#release-activities)
  - [Dealing with Ambiguity](#dealing-with-ambiguity)
  - [Managing Critical Issues](#managing-critical-issues)
    - [General Guidelines](#general-guidelines)
  - [Correcting Mistakes](#correcting-mistakes)
  - [Retrospectives](#retrospectives)

## Overview

This document contains a list of maintainers in this repo. See [opensearch-project/.github/RESPONSIBILITIES.md](https://github.com/opensearch-project/.github/blob/main/RESPONSIBILITIES.md#maintainer-responsibilities) that explains what the role of maintainer means, what maintainers do in this and other repos, and how they should be doing it. If you're interested in contributing, and becoming a maintainer, see [CONTRIBUTING](CONTRIBUTING.md).

## Current Maintainers

| Maintainer       | GitHub ID                                | Affiliation |
| ---------------- |------------------------------------------| ----------- |
| Peter Zhu        | [peterzhuamazon](https://github.com/peterzhuamazon) | Amazon      |
| Barani Bikshandi | [bbarani](https://github.com/bbarani)    | Amazon      |
| Sayali Gaikawad  | [gaiksaya](https://github.com/gaiksaya)  | Amazon      |
| Rishab Singh     | [rishabh6788](https://github.com/rishabh6788) | Amazon      |
| Zelin Hao        | [zelinh](https://github.com/zelinh)      | Amazon      |
| Jeff Lu | [jordarlu](https://github.com/jordarlu)  | Amazon      |
| Prudhvi Godithi | [prudhvigodithi](https://github.com/prudhvigodithi) | Amazon      |
| Divya Madala  | [Divyaasm](https://github.com/Divyaasm)  | Amazon      |
| Daniel (dB.) Doubrovkine  | [dblock](https://github.com/dblock)      | Amazon      |
| Tianle Huang | [tianleh](https://github.com/tianleh)    | Amazon      |

## Emeritus Maintainers

| Maintainer        | GitHub ID                                               | Affiliation |
| ----------------- | ------------------------------------------------------- | ----------- |
| Abhinav Gupta     | [abhinavGupta16](https://github.com/abhinavGupta16)     | Amazon      |
| Cameron Skinner   | [camerski](https://github.com/camerski)                 | Amazon      |
| Marc Handalian    | [mch2](https://github.com/mch2)                         | Amazon      |
| Peter Nied        | [peternied](https://github.com/peternied)               | Amazon      |

## Release Owner

The release owner is a temporary role for the duration of a given OpenSearch / OpenSearch Dashboards release.  This owner is tracked by the assignment of a release ticket an individual. The release owner oversees the release ticket, makes sure the activities are completed, and closed the release.  Release activities are documented in the release ticket, see the [template](./.github/ISSUE_TEMPLATE/release_template.md). The purpose of the release owner is to be responsible for following the release process.

### Release Activities

The release owner performs the activities described in the overall release ticket.  Other activities associated with the release are managed by the component release owners or are be delegation to the most appropriate area owner.  Keeping the release owner's activities well document and predicable ensures the release process avoids bottlenecks.

### Dealing with Ambiguity 

Tasks will become unclear to complete, the release owner’s role is to make sure that a path to resolution is found by involving those that are needed and communicating via the primary release issue and on the component release issues.

### Managing Critical Issues

Create a new issue in GitHub any time the release schedule is impacted.  For transparency GitHub has all the information pertaining to state of the release.

#### General Guidelines

- For issues impacting a single component, created an issue in the component’s GitHub repository, with the release version tag and referenced on the component's release issue.
- For issues impacting multiple components, create an issue in the root cause's GitHub repository, with the release version tag and referenced in the component's release issues.
- For issues impacting all / blocking any productivity, create an issue immediately in this repository, with the release version tag, and post a comment in the general release ticket.  Make a broad call to action for stakeholders to engage in the issue.  Closely monitor the issue until the release can resume as planned.

### Correcting Mistakes

Mistakes happen, correcting these transparently is paramount.  Use markdown strike-through when making edits to correct incorrect information instead of deleting. 

Some mistakes are larger, such as a process that was marked completed was done so incorrectly, these corrections need additional tracking as a campaign. Create an issue to drive the campaign with a list of components to track statuses such as notifications and confirmation of the correction.  This is important to confirm that the process was completed as expected, see an [example](https://github.com/opensearch-project/opensearch-build/issues/954).

### Retrospectives

The release process will be improved and invested in, running a retrospective and communicating an summary of its results is necessary to achieve this.  Retrospectives are encouraged at the component level in the component release issues template. 

Feedback comes from the retro issue created during the release and component level retrospectives.  A meeting could be run to capture additional feedback if desired.  This process is focused on recording what happened to make remedies.
 
After the retro items are in, a final summary is written as a comment on the retrospective issue.  The comment includes areas of consideration for the project alongside action items with owners to drive them, [example](https://github.com/opensearch-project/opensearch-build/issues/880) summary.
