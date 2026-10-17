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

### 3.1 Test oracle

For testing, we can use saved HTML pages and sample policy files as fixtures. For example, a saved HTML page can contain a fixed set of PDF, DOCX and RTF links. Because we already know which links are inside the page, we can check whether the scraper finds the correct ones.

We can also keep some valid sample files and some broken or corrupted files. This can help us check whether the scraper can tell the difference between a successful download and an invalid file. These fixtures are more reliable than always using the live website because the files will not change between test runs. A small local server can also be used when we need to test HTTP behaviour.

### 3.2 Rate limiting

We tested the live policy website using `curl` in Windows PowerShell. We sent 10 requests with a one-second delay between each request. Requests 1–6 returned HTTP 200. Requests 7 and 8 returned HTTP 429 (Too Many Requests), and requests 9 and 10 returned HTTP 200 again.

From this test, the website seems to use temporary rate limiting when several requests are sent in a short time. Because of this, our automated tests should not keep sending requests to the real website. We can instead use saved HTML files, sample policy files, mocked responses, or a local server. This also makes the tests easier to repeat without putting extra load on the real site.

### 3.3 Simulating failures

Test doubles can be useful for failures that are hard to create on the real website. Because our prototype imports `urlopen` directly from `urllib.request`, we should patch the name where it is used, such as `prototype.urlopen`, rather than patching `urllib.request.urlopen`. Using `unittest.mock.patch` (or pytest's monkeypatching) lets us replace it with a fake that raises `TimeoutError` or `URLError` to simulate a timeout or connection failure.

The fake can also return controlled, incomplete bytes to simulate an interrupted download. For slow responses or a connection that closes before the promised data arrives, a small local `http.server` is more suitable: it can delay its response or send only part of the content. This is the approach used by the failure demonstration in §3.4.

Using these methods is safer than trying to create the same problems on the real website. It also means we can repeat the same failure many times and know what result we should expect.

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
