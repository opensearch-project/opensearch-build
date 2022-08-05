<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

- [Maintainers](#maintainers)
- [Release Owner](#release-owner)
  - [Release Activities](#release-activities)
  - [Dealing with Ambiguity](#dealing-with-ambiguity)
  - [Managing Critical Issues](#managing-critical-issues)
    - [General Guidelines](#general-guidelines)
  - [Correcting Mistakes](#correcting-mistakes)
  - [Retrospectives](#retrospectives)
- [ZenHub Process Workflow](#zenhub-process-workflow)
  - [What is ZenHub?](#what-is-zenhub)
  - [Setting up ZenHub](#setting-up-zenhub)
  - [Sprint Board](#sprint-board)
    - [Pipelines](#pipelines)
  - [Creating Issues](#creating-issues)
  - [Managing issues/stories](#managing-issuesstories)
    - [Spillovers](#spillovers)
  - [Epics](#epics)
  - [Recurring Team Meetings](#recurring-team-meetings)
  - [On-Call](#on-call)

## Maintainers

| Maintainer       | GitHub ID                                           | Affiliation |
| ---------------- | --------------------------------------------------- | ----------- |
| Peter Zhu        | [peterzhuamazon](https://github.com/peterzhuamazon) | Amazon      |
| Barani Bikshandi | [bbarani](https://github.com/bbarani)               | Amazon      |
| Sayali Gaikawad  | [gaiksaya](https://github.com/gaiksaya)             | Amazon      |
| Rishab Singh     | [rishabh6788](https://github.com/rishabh6788)       | Amazon      |
| Zelin Hao        | [zelinh](https://github.com/zelinh)                 | Amazon      |
| Prudhvi Godithi  | [prudhvigodithi](https://github.com/prudhvigodithi) | Amazon       | 


[This document](https://github.com/opensearch-project/.github/blob/main/MAINTAINERS.md) explains what maintainers do in this repo, and how they should be doing it. If you're interested in contributing, see [CONTRIBUTING](CONTRIBUTING.md).

## Release Owner
The release owner is a temporary role for the duration of a given OpenSearch / OpenSearch Dashboards release.  This owner is tracked by the assignment of a release ticket an individual.  The release owner oversees the release ticket, makes sure the activities are completed, and closed the release.  Release activities are documented in the release ticket, see the [template](./.github/ISSUE_TEMPLATE/release_template.md). The purpose of the release owner is to be responsible for following the release process.

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

## ZenHub Process Workflow
We follow agile methodologies for our development and release process. We use GitHub issues with annotations via ZenHub to manage and track our stories and issues to effectively manage them over the sprint.

### What is [ZenHub](https://www.zenhub.com/)?

ZenHub is an agile project management and product roadmaps solution, natively integrated into GitHub. It is free to use for opensource repository and comes with a paid membership to manage private repositories. 
We currently use ZenHub only with our public and opensource repositories.

### Setting up ZenHub

ZenHub can be easily added as an [extension]((https://www.zenhub.com/extension)) to chrome and firefox which can be downloaded for free from the ZenHub website. 
Alternatively, we can use a the ZenHub [webapp link](https://app.zenhub.com/workspaces/engineering-effectiveness-614cf4272a385f0015d2b48f/board?repos=357723952,406037663) to view the board.

### Sprint Board
Once the ZenHub extension is installed, ZenHub board can be accessed using the ZenHub tab on GitHub.

![img.png](zenhub_tab_image.png)

If you are using the webapp - here is the [link](https://app.zenhub.com/workspaces/engineering-effectiveness-614cf4272a385f0015d2b48f/board?repos=357723952,406037663)

#### Pipelines

1. **New Issues -** Issues to be reviewed and estimated before being added to the Product Backlog.
2. **Icebox -** Low priority Issues that do not need to be addressed in the near future**.**
3. **Product Backlog -** Upcoming Issues that have been reviewed, estimated, and prioritized top-to-bottom.
4. **Sprint Backlog -** Issues ready to be worked on in the sprint, prioritized top-to-bottom.
5. **In Progress -** Issues currently being worked on by the team.
6. **Review/QA -** Issues open to the team for review and testing. Code complete, pending feedback.
7. **Done -** Issues tested and ready to be deployed to production. Verify the acceptance criteria and close the issue.
8. **Closed -** Issues that are deployed to production and closed

Description for each pipeline can also be found on the sprint board by clicking on the 3 dots next to the pipleine name.

### Creating Issues

Follow the steps below to create issues on ZenHub workflow -

1. Create the issue for the desired repository following the required guidelines for mandatory and optional fields on GitHub.
2. Add an acceptance criteria for the issue
3. Add relevant tags to the issue. This would help us to track and filter issues.
4. Select the correct pipeline for the issue (defaults to New Issues )
5. Mark the issue for a sprint (if known)

### Managing issues/stories

1. Everyone working on a task should ensure the following -
    1. Have an issue associated with it to record the work
    2. The issue should be assigned
    3. The issue should have an estimate set
    4. The issue should have the correct pipeline
2. Pull requests raised should be assigned and linked to their issues. There should not be a PR without an issue.
3. If you are working on an issue that belongs to a private repository, create an issue in the opensearch-build repository with only public details to track your work.

#### Spillovers

Spillover issues that were a part of the sprint but were not completed are a good indicator for improvement areas.

These issues will automatically be moved to the next sprint. There are 3 possible cases in this scenario :

1. **Issue is still in sprint backlog -** This is an indication that we need to look again at our sprint planning to help plan better for the sprint. 
2. **Issue is in progress -** This means that we need to create smaller issues such that these can be completed in a sprint. 
3. **Issue is in Review -** These issues should be closed at a priority in the upcoming sprint.

### Epics

An epic is *a large body of work that can be broken down into a number of smaller stories*, or sometimes called “[META] Issues”. Epics often encompass multiple teams, on multiple projects, and can even be tracked on multiple boards. Epics are almost always delivered over a set of sprints.

ZenHub provides an elegant way to incorporate epics reducing a lot of manual work compared to meta issues and easy viewing. Click [here](https://help.zenhub.com/support/solutions/articles/43000010341-an-intro-to-zenhub-epics) for more details.

### Recurring Team Meetings

- **Standup -** Daily standups can easily be managed using the sprint board. The moderator should select the filter for the current sprint and change filter for assignees as we move forward with the standup. 
This would ensure that all the tasks the an individual is working on is correctly represented on the sprint board.<br>

  Everyone should spend approximately 1 minute to discuss the work without interruption, answering questions like - What did I do yesterday? What is the plan for today? What help I might need from others? After everyone turns, we can discuss go-backs if any. The Moderator keeps track of the time.


- **Grooming -** All team members come together to add items to the Product Backlog.  These issues/stories should have been reviewed, estimated, and prioritized top-to-bottom.


- **Planning -** We go over the product backlog to see what all do we need to complete for the current sprint.


- **Retrospective -** This meeting is held at the end of a sprint used to discuss what went well during the previous sprint cycle and what can be improved for the next sprint.

### On-Call
Since on-call is a weekly rotation, we do not create an issue for on-call. However, if on-call requires you to work on a bug, please make sure that we have issue associated with the task for tracking.

