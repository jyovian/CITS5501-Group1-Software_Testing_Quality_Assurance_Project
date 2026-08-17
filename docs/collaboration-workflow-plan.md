# Collaboration & Workflow Plan

## 1. Team communication and responsibilities

- Microsoft Teams is the group's primary communication channel for announcements, questions, meeting notes, and decisions.
- The group will check progress each week, normally during or around the Tuesday 11:00 lab. Additional online discussions will be arranged when a deadline or blocking issue requires them.
- Work will be divided into GitHub Issues. Each issue must have a clearly identified owner, scope, and expected completion date.
- The issue owner is responsible for reporting blockers early. Ownership does not remove shared responsibility: important report sections, code, tests, and presentation material will be checked by at least one other member.
- Decisions that affect the whole project, including tools, interfaces, and changes to scope, will be recorded in Teams, GitHub Issues, or pull requests so that all members can review them.

## 2. Accountability and progress tracking

- GitHub Projects will be used to track work using task states such as `Todo`, `In progress`, `In review`, and `Done`.
- Each task will be represented by a GitHub Issue and linked to the corresponding branch or pull request where applicable.
- Progress and overdue work will be reviewed during the weekly check-in.
- A task is only considered complete when it meets the agreed requirement, includes appropriate testing or supporting evidence, and has passed review.

## 3. Version control strategy

- Project documents and code will be maintained in the group's private GitHub repository.
- The `main` branch will contain reviewed work only and will remain protected from accidental direct changes.
- Each change will be developed on a short-lived branch with a descriptive name, such as `username-short-task-description`.
- Branches should remain focused on one task so that their changes are easy to review.
- Commit messages should be brief, use the imperative form, and describe the purpose of the change, for example `Add scraper timeout tests`.

## 4. Review and merging

- Changes will be submitted through pull requests rather than committed directly to `main`.
- At least one group member other than the author should review and approve a pull request before it is merged.
- Reviewers will check the relevant specification, correctness, clarity, tests, and documentation rather than only checking whether the code runs.
- Requested changes should be addressed before merging. Authors should not merge work with unresolved substantive review comments.
- The group will avoid leaving major merges until the submission day. A final cross-check against the project brief and marking requirements will be completed before submission.

## 5. Resource risk management

- Members should notify the group as early as possible if illness, other commitments, or technical problems may delay an assigned task.
- Work will be kept in the shared repository and decisions will be documented so that another member can continue a task if its owner becomes unavailable.
- Large tasks will be divided into smaller issues to reduce dependence on one person.
- If a task is blocked or its owner is unavailable, the group will reassess priorities during the next check-in and reassign essential work where necessary.
- Non-essential features may be reduced or postponed if required to protect the correctness and timely completion of core requirements.

## 6. Updating this plan

This plan may be updated through a pull request when the group agrees that its working practices need to change. Important changes should be communicated to all members before approval.
