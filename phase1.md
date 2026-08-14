# CITS5501 Project Phase 1 Report

**Group name:**

**Repository:** [link to private GitHub/GitLab/Bitbucket repo]

**Group members:**

- Juan Yeremia Yovian (24911605)
-

## Planning and organization

**1. Where is your group's Collaboration & Workflow Plan maintained? Is it in the Git repository, or elsewhere?**

**2. What tool or approach are you using to track assigned tasks and completion? Why did you choose it? Has anyone in the group used it before?**

We are using GitHub Projects that links directly to our repository's Issues. This was chosen because it's the most efficient way of tracking our progress. No extra app or account or tool required. Everyone already has a GitHub account. It also links directly to commits/PRs.

---

## Language and tooling

**3. Which language has your group chosen? Have any members of the group not used it — and if so, how will they get familiar with it? What factors influenced your choice of implementation language? Rank the top three in order of importance. What advantages do you expect your chosen language to give your team? What disadvantages or risks do you expect? If you had to implement this project in the other language, what do you think would be most difficult? What might be easier?**

Our chosen language for this project is **Python**. We picked it mainly because scraping websites means dealing with messy, unpredictable HTML. Python is easier to write quickly and fix quickly when that happens.

###### Top 3 factors:

1. **Mature ecosystem**. Python has mature and well-documented libraries for every stage of this project, from fetching, HTML parsing, document extraction, etc). These help reduce the amount of custom code we will need to write and test.
2. **Team familiarity**. Every member of this group has experience with Python,
3. **Faster to write and debug**. When the scraper breaks, which it will because websites change, we can fix it quickly without fighting the compiler.

###### Advantages:

- Quicker to get something working
- Easier to test since Python's dynamic typing doesn't go against us when handling messy scraped data

###### Disadvantages:

- Python doesn't catch type errors until runtime

###### If we had to use another language (Java)

It would probably be harder to deal with all the different ways thigns can go wrong when scarping

**4. What build/dependency management tool will you use (e.g. uv or poetry for Python; Gradle or Maven for Java; something else)? Has anyone in the group used it before — or will this be the first time setting up a project with it?**

[Answer]

---

## Technical risks

**5. What parts of a web scraper do you expect could most easily fail, and how?**

[Answer]

**6. Which external factors could make your software stop working after it has been completed?**

[Answer]

**7. Which components of your project do you think will be easiest to test? Which do you expect will be hardest?**

[Answer]

**8. What assumptions is your software likely to make about the website it scrapes? How could those assumptions be violated?**

[Answer]

---

## Team practices

**9. Suppose a serious bug is discovered two days before the deadline. How would your team investigate and respond?**

[Answer]

**10. What will convince your team that a feature is "finished"?**

[Answer]

**11. If two group members disagree about whether software is "working correctly", how will you resolve that disagreement?**

[Answer]

---

## Code quality

**12. [Python groups] Will you use a type checker (e.g. mypy or pyright), and if so, will it run in CI or just periodically/manually? Has anyone used one before? Do you plan to use a linter (e.g. pylint, black)?**
**[Java groups] Is your team familiar with any static analysis/linting tools (e.g. Checkstyle, SpotBugs, PMD)? Do you plan to use any?**

[Answer]

**13. Suppose a group member's contribution doesn't pass your linting or type checking checks. What will be the consequences? Will merges be blocked if these checks fail, or will the checks be advisory only?**

[Answer]

---

## Testing framework

**14. What test framework will you use (e.g. pytest for Python; JUnit 5 for Java; something else)? Has the group used it before, or only heard of it?**

[Answer]

---

## CI / automation

**15. Will you set up continuous integration (e.g. GitHub Actions) to run your test suite automatically, or run tests manually before submission? Have any members of your group used continuous integration before?**

[Answer]

---

## Testing mindset

**16. Suppose your scraper is finished and submitted. Now imagine another student is trying to break your software (get it to exhibit failures or unexpected behaviour). What might they try first?**

[Answer]

**17. How will you know that your software is producing the correct output, rather than merely some output?**

[Answer]

**18. What evidence would increase your confidence that your software is reliable?**

[Answer]

**19. At this stage of the project, what do you think will be the biggest challenge in producing reliable software?**

[Answer]

---

## Process and standards

**20. What will be your code review process — does someone other than the author review changes before merging, or is this informal?**

[Answer]

---

## Assumptions

List any assumptions made while completing this report, numbered (A001, A002, ...), with justification.

- **A001:** [Assumption] — [Reasoning]
