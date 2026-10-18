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


### 2.1 Expected scraper behaviour

Across all scenarios, a reasonable scraper should never silently report success, contain failures so that one bad link does not stop the others, and in the case of an error, report clearly what went wrong. In several cases the correct response is simply to report the failure and stop rather than recover. 

* Scenario 1: If the scraper finds no links, or none that match its expected pattern, it should report that the page structure may have changed. It should not download anything or report success, and it should exit with a non-zero status. A silent "0 documents, done" is the worst outcome, because it looks like a pass.
* Scenario 2: The scraper should detect that the page is incomplete (for example, no closing `</html>`, or a body shorter than `Content-Length`). It should warn that results may be incomplete, and must not request a half-written URL. Links from the complete part of the page may be used, but the run should not be reported as fully successful.
* Scenario 3: Every request needs a timeout. A slow link that eventually responds within the timeout is fine. A link that exceeds it should be recorded as failed after a limited number of retries, and the scraper should carry on with the remaining documents. If the index page itself never responds, the scraper should give up after the timeout and report a clear error.
* Scenario 4: A 4xx means the request is at fault, so the scraper should not retry it (the exception is 429, where it should respect `Retry-After`). A 5xx may be transient, so a small, capped number of retries is reasonable. After that, the document is recorded as failed with its status code. If the index page returns a 4xx or 5xx, the scraper should abort with a clear message.
* Scenario 5: An HTTP 200 is not enough. The scraper should check the declared content type and the file signature (`%PDF` for PDFs, `PK` for `.docx`), and ideally that the file can actually be opened. Anything that fails these checks should be reported as failed ("not a valid PDF") and not counted as a success.

### 2.2 Test cases

All tests are run against a saved HTML page or a local test server (not the live site), so the responses are exactly controlled. Timeout values below are placeholders for whatever the scraper is configured with.
 
| ID | Scenario | Arrange | Act | Assert |
|---|---|---|---|---|
| T001 | 1 – Structure change | Saved index page where the document links are no longer `<a>` tags (e.g. documents listed as plain text or rendered by JavaScript). | Run the scraper against it. | Reports "no document links found / structure may have changed"; makes no download requests; exits non-zero; does not print a success summary. |
| T002 | 1 – Structure change | Index page with `<a>` tags, but every link is a handler URL such as `/download.aspx?id=12` with no file extension. | Run the scraper against it. | Same as T001: zero matches is flagged as a possible structure change, not treated as "nothing to do". |
| T003 | 2 – Truncated HTML | Server sends an index page cut off mid-tag (e.g. ending in `<a href="/policy/x.p`) with no `</html>`. | Run the scraper against it. | Warns the page appears truncated; does not request the partial URL; run is not reported as fully successful. |
| T004 | 3 – Timeout (short, one link) | Local server where one document link waits longer than the timeout before responding. Other links respond normally. | Run the scraper with a short timeout (e.g. 2 s). | That link is recorded as failed (timeout) after at most the allowed retries; the remaining documents still download; total time stays bounded (about timeout × attempts). |
| T005 | 3 – Timeout (long, index) | Local server that accepts the connection to the index page but never sends a response. | Run the scraper with the same timeout. | Scraper gives up after the timeout and prints a clear error; no download attempts; exits non-zero; does not hang. |
| T006 | 4 – 4xx | Local server returns 404 for one document link; other links are normal. | Run the scraper. | The 404 is recorded as failed with status 404 and is **not retried** (server log shows one request for that URL); other documents succeed. |
| T007 | 4 – 5xx | Local server returns 503 for one document link every time. | Run the scraper. | Scraper retries no more than the configured cap, then records the document as failed with status 503; total requests stay within the 20-request limit. |
| T008 | 4 – Index error | Local server returns 500 (and, in a second run, 403) for the index page. | Run the scraper. | Aborts with a clear message including the status code; makes no document requests; exits non-zero. |
| T009 | 5 – HTML instead of PDF | Local server returns 200 for a `.pdf` link, with `Content-Type: text/html` and an HTML body. | Run the scraper. | Document is reported as failed (e.g. "not a valid PDF"); first bytes are not `%PDF`; the run is not counted as a successful download. |
| T010 | 5 – Corrupt PDF | Local server returns 200 with `Content-Type: application/pdf` for a file that starts with `%PDF-1.6` but is truncated or filled with garbage after the header. | Run the scraper. | Document is reported as failed because the file cannot be opened (e.g. `pypdf` raises an error or `%%EOF` is missing); not counted as a success. |



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
