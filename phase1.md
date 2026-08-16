# CITS5501 Project Phase 1 Report

**Group name:**

**Repository:** [CITS5501 Group 1 Repository](https://github.com/jyovian/CITS5501-Group1-Software_Testing_Quality_Assurance_Project)

**Group members:**

- Juan Yeremia Yovian - Student ID: 24911605 - Github: 
- Jinghan Wu - Student ID: 24289151 - Github: Jinghan00
-
-
-

## Planning and organization

**1. Where is your group's Collaboration & Workflow Plan maintained? Is it in the Git repository, or elsewhere?**

**2. What tool or approach are you using to track assigned tasks and completion? Why did you choose it? Has anyone in the group used it before?**

We are using GitHub Projects that links directly to our repository's Issues. This was chosen because it's a simple and convenient way of tracking our progress. No extra app or account or tool required. Everyone already has a GitHub account. It also links directly to commits/PRs. Some members of the group have used GitHub Projects before, while others are already familiar with basic GitHub functions.

---

## Language and tooling

**3. Which language has your group chosen? Have any members of the group not used it — and if so, how will they get familiar with it? What factors influenced your choice of implementation language? Rank the top three in order of importance. What advantages do you expect your chosen language to give your team? What disadvantages or risks do you expect? If you had to implement this project in the other language, what do you think would be most difficult? What might be easier?**

Our chosen language for this project is **Python**. We chose it mainly because web scraping can involve unexpected HTML and different document formats. Python allows us to develop and debug this type of software relatively quickly.

###### Top 3 factors:

1. **Library support**. Python has mature and well-documented libraries for many stages of this project, from fetching, HTML parsing, document extraction, etc. These help reduce the amount of custom code we will need to write and test.
2. **Team members' experience**. Every member of this group has experience with Python.
3. **Ease of debugging**. If the scraper fails because of unexpected or changing website behaviour, Python should allow us to identify and modify the affected code relatively quickly.

###### Advantages:

- Allows us to develop features relatively quickly.
- Strong library support for web scraping and document processing.

###### Disadvantages:

- Python's dynamic typing means that some type-related errors may only be detected at runtime.
- Using several third-party libraries may introduce dependency management issues.

###### If we had to use another language (Java)

It would probably be harder to deal with all the different ways things can go wrong when scraping (bad HTML, missing files, network errors, etc). Java would require us to handle these exceptions really explicitly, which can be good for safety but would slow us down a lot. Plus, Java introduces boilerplate code and complexity for those who aren't familiar with it. However, Java's static type system and compiler checks could make some errors easier to detect before the program is run.

**4. What build/dependency management tool will you use (e.g. uv or poetry for Python; Gradle or Maven for Java; something else)? Has anyone in the group used it before — or will this be the first time setting up a project with it?**

[Answer]

---

## Technical risks

**5. What parts of a web scraper do you expect could most easily fail, and how?**

The parts most likely to fail are the network requests, HTML parsing, and document downloading. Network requests may fail because of timeouts, server errors, or temporary connection problems. HTML parsing may fail if the website structure changes or if the page contains malformed HTML. Document downloads may also fail because of broken links, missing files, unexpected file types, or corrupted documents.

**6. Which external factors could make your software stop working after it has been completed?**

The software could stop working if the website changes its structure, URLs, or document formats. It could also be affected by new login requirements, stricter rate limits, or changes in the server. Updates to third-party libraries may also cause compatibility problems.

**7. Which components of your project do you think will be easiest to test? Which do you expect will be hardest?**

- The easiest components to test will probably be functions that process fixed inputs, such as URL handling, file type detection, text processing, and query logic. These can be tested using known inputs and expected outputs.

- The hardest components to test will be network requests and interactions with the real website. These depend on external factors such as connection problems, server errors, rate limits, and changes to the website. These behaviours are harder to reproduce consistently in tests.

**8. What assumptions is your software likely to make about the website it scrapes? How could those assumptions be violated?**

Our software will probably assume that the website structure stays mostly consistent, that document links work, and that file types can be identified correctly. These assumptions could fail if the website layout changes, links are broken, files have unexpected formats, or the server returns unusual responses.

---

## Team practices

**9. Suppose a serious bug is discovered two days before the deadline. How would your team investigate and respond?**

If a serious bug is found two days before the deadline, we would first reproduce it and identify the affected component. The issue would be given high priority and assigned to appropriate team members. If necessary, non-essential work would be paused. After fixing the bug, we would run the relevant tests and regression tests, review the change, and merge it only after confirming that the problem is resolved.

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
