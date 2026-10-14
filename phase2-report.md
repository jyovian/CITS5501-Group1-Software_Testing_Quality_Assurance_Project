# CITS5501 Project Phase 2 Report

**Repository:** [CITS5501 Group 1 Repository](https://github.com/jyovian/CITS5501-Group1-Software_Testing_Quality_Assurance_Project)

**Group members:**

- Juan Yeremia Yovian - Student ID: 24911605 - Github: jyovian
- Jinghan Wu - Student ID: 24289151 - Github: Jinghan00
- Shee Wang - Student ID: 24368932 - Github: sheewang
- Gelani Nimit Sureshbhai - Student ID: 24765784 - Github: Fighterdx
- Laura Acosta Vargas - Student ID: 23802255 - Github: laura-camila-av

---

## 1. Task 1 – Prototype

<!-- Owner: ______
     Write ONLY inside this section. Delete these comments when done. -->

### 1.1 What the prototype does

<!-- What it does, step by step. How to run it can just point to the README. -->

### 1.2 Limitations

<!-- At least 2. -->

### 1.3 Assumptions

<!-- Number them from A007 onwards (Phase 1 used A001–A006).
     Format: **A007:** assumption. Why it's reasonable. -->

---

## 2. Task 2 – Test design

<!-- Owner: ______
     Write ONLY inside this section. Delete these comments when done. -->

### 2.1 Expected scraper behaviour

<!-- For each of the 5 scenarios, what should a reasonable scraper do?
     1. Site structure changes
     2. HTML is truncated
     3. Site or link times out (short or long)
     4. 4xx / 5xx status codes
     5. Link doesn't return a valid office/PDF file (e.g. HTML instead of PDF, corrupt PDF) -->

### 2.2 Test cases

<!-- 6–10 tests, at least 1 per scenario. -->

| ID | Scenario | Arrange | Act | Assert |
|---|---|---|---|---|
| T001 | | | | |

---

## 3. Task 3 – Fixtures and test doubles

<!-- Owners: ______ (3.1–3.3), Shee Wang (3.4)
     Write ONLY inside this section. Delete these comments when done. -->

### 3.1 Test oracle

<!-- What is our "source of truth" for whether the scraper works? (saved HTML, sample policy files, local server…) -->

### 3.2 Rate limiting

<!-- Does the live site limit lots of requests? What did you observe?
     If it does, how would we run our tests without the live site? -->

### 3.3 Simulating failures

<!-- Can test doubles simulate timeouts, interrupted downloads, connection failures, slow responses?
     Which Python tools would we use? -->

### 3.4 Failure demonstration

The artifact for this task is `task3b/fault_simulation_example.py`. It runs a
small policy site on the local computer. The index page contains a link called
`unavailable.pdf`, but the server returns `503 Service Unavailable` when the
scraper follows that link. This gives us a repeatable way to check whether the
scraper reports a failed download instead of treating the response as a valid
PDF. The script also has a short demonstration mode, and the automated checks
are in `task3b/test_fault_simulation_example.py`.

Reproducing the same problem on the live policy site would be difficult because
we cannot make that server return a 503 response when we need it. Trying to
overload or interfere with the live site would also be inappropriate. The local
server gives the same response on every run and does not send test traffic to
the real site.

**A3-001:** An HTTP 503 response is treated as a failed download and not as
valid policy content.

---

## 4. Task 4 – Adversarial inputs

<!-- Owner: ______
     Write ONLY inside this section. Delete these comments when done. -->

<!-- 5–8 ideas for breaking another team's scraper. -->

| # | Assumption being challenged | Input / environment used | What counts as failure, and how it's detected |
|---|---|---|---|
| 1 | | | |
