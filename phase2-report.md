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

### 1.1 What the prototype does

The prototype is `task1/prototype.py`. It is written in Python and uses only
the standard library. Instructions for running it are in `task1/README.md`.
This is how it works:

1. It downloads the index page at
   `https://uwa-policy.cits5501.arranstewart.io/policy/`. A different start
   URL can be given on the command line, so it can also be run against a
   local test server.
2. It reads every `<a href>` on the page, turns relative links into full
   URLs, and checks and keeps a link only if:

   - it is on the same host as the index page and
   - its path ends in `.pdf`, `.doc`, `.docx` or `.rtf`.

   Duplicates are removed. It does not follow any other links, so there is no recursive crawling.
3. It downloads the first 5 links found (this can be changed with
   `--max-docs`). Every request, including the index page, counts towards a
   limit of 20 (`--max-requests`), and the prototype stops when the limit is
   reached, printing a message and the summary line instead of crashing. If
   the server responds with `429 Too Many Requests`, it waits for the number
   of seconds given in the `Retry-After` header (at most 60) and tries again.
   If that header is missing or uses the date form, it waits 10 seconds.
   Downloaded files are kept in memory only and are not saved.
4. For each document it prints whether the download succeeded (HTTP 200),
   the URL, the HTTP status, the declared `Content-Type`, the size in bytes
   and the first 8 bytes of the file. It finishes with a summary line.

On the live site, the prototype downloaded 5 of 5 documents using 6
requests. All five returned status 200 with content type `application/pdf`,
and every file started with `%PDF-1.6`.

```
Fetching index page: https://uwa-policy.cits5501.arranstewart.io/policy/
  HTTP 200, 584187 bytes
Found 213 distinct document links on the same site.

[OK] https://uwa-policy.cits5501.arranstewart.io/policy/-/media/project/uwa/uwa/policy-library/policy/code-of-conduct/integrity/policy-framework/policy-governance-framework.pdf
  status:       200
  content type: application/pdf
  size:         301201 bytes
  first bytes:  b'%PDF-1.6'

[OK] https://uwa-policy.cits5501.arranstewart.io/policy/-/media/project/uwa/uwa/policy-library/policy/code-of-conduct/up26-2-code-of-conduct.pdf
  status:       200
  content type: application/pdf
  size:         163909 bytes
  first bytes:  b'%PDF-1.6'

[OK] https://uwa-policy.cits5501.arranstewart.io/policy/-/media/project/uwa/uwa/policy-library/policy/code-of-conduct/up26-2-code-of-conduct---annexure-a.pdf
  status:       200
  content type: application/pdf
  size:         217240 bytes
  first bytes:  b'%PDF-1.6'

...

Downloaded 5 of 5 documents using 6 of 20 requests.
```

### 1.2 Limitations

##### Documents are identified by file extension

A policy document served from a URL without one of the four extensions (for
example `/download?id=123`) would be missed. However, a link ending
in `.pdf` that actually returns an HTML error page would still be selected.

##### "Success" only means HTTP 200

The prototype prints the content type and first bytes, but it does not check
them. A corrupt PDF, or an HTML page returned with status 200, is still
reported as `OK`, so a person has to read the output to notice the problem.

##### No timeouts or error handling

Requests have no timeout, so a server that stops responding would make the
prototype hang. A dropped connection or DNS failure stops the program with an
unhandled exception. The spec says the prototype does not need to be robust,
so this was left out on purpose.

##### The sample is not representative

The prototype always downloads the first 5 links in page order. On the live site these
are all PDFs from the same section, so `.doc`, `.docx` and `.rtf` downloads
are never tried in a default run.

##### Same-host links only

Links to other hosts are skipped. This also skips `Fitness-to-Study.doc`,
which is linked on `www.uwa.edu.au` rather than on the policy site itself.

### 1.3 Assumptions

- A001: All policy documents are linked directly from the index page.
- A002: Links ending in `.pdf`, `.doc`, `.docx` or `.rtf` are policy
  documents. `.pptx` files are out of scope (Phase 1, A006).
- A003: Only links on the same host as the index page are part of the site.
- A004: An HTTP 200 response means the download succeeded.
- A005: The index page is UTF-8, as the server declares.
- A006: Waiting for the `Retry-After` time after a 429 response is enough to
  stay within the rate limit.

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

### 3.1 Test oracle

For testing, we can use saved HTML pages and sample policy files as fixtures. For example, a saved HTML page can contain a fixed set of PDF, DOCX and RTF links. Because we already know which links are inside the page, we can check whether the scraper finds the correct ones.

We can also keep some valid sample files and some broken or corrupted files. This can help us check whether the scraper can tell the difference between a successful download and an invalid file. These fixtures are more reliable than always using the live website because the files will not change between test runs. A small local server can also be used when we need to test HTTP behaviour.

### 3.2 Rate limiting

We tested the live policy website using `curl` in Windows PowerShell. We sent 10 requests with a one-second delay between each request. Requests 1–6 returned HTTP 200. Requests 7 and 8 returned HTTP 429 (Too Many Requests), and requests 9 and 10 returned HTTP 200 again.

From this test, the website seems to use temporary rate limiting when several requests are sent in a short time. Because of this, our automated tests should not keep sending requests to the real website. We can instead use saved HTML files, sample policy files, mocked responses, or a local server. This also makes the tests easier to repeat without putting extra load on the real site.

### 3.3 Simulating failures

Test doubles can be used to simulate failures that are difficult to reproduce on the real website. Since our prototype uses `urllib`, we can use `unittest.mock.patch` to replace `urlopen` with a fake function.

For example, the fake `urlopen` can raise a `TimeoutError` or `URLError` to test how the scraper handles timeouts and connection failures. Because the prototype imports `urlopen` directly, it should be patched where it is used, such as `prototype.urlopen`, rather than patching `urllib.request.urlopen`.

For slow responses or interrupted downloads, a local `http.server` can be used to control how the server responds. The server can deliberately delay its response or stop sending data before the download is complete. Section 3.4 provides a similar local-server example for a `503 Service Unavailable` response.

Using these methods is safer and more repeatable than trying to create the same failures on the real policy website.

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

### 4.1 Happy-path assumptions

We started by writing down what has to go right for a scraper to work on the
"normal" path. Most of these are things a team would never think to check,
because the real site happens to behave nicely:

- Policy links end in `.pdf` or `.docx`, in lowercase, with nothing after them.
- Every document link has a file extension in it at all.
- Links are either full URLs or simple relative paths.
- Each document can only be reached from one URL.
- The index page is valid UTF-8 HTML, and the links are already in the page
  source rather than added later by JavaScript.
- Asking for a document gets a `200 OK` straight away, with no redirects.
- The `Content-Type` header is correct.
- Files are a normal size and download completely.
- The server answers quickly.

### 4.2 Adversarial test ideas

Each idea below targets one of these assumptions. We would run all of them
against a local server or a saved HTML page, not the live site, since we can
control exactly what gets sent back.

| # | Assumption being challenged | Input / environment used | What counts as failure, and how it's detected |
|---|---|---|---|
| 1 | Links always end in a lowercase extension. | An index page with links like `Policy.PDF`, `leave.pdf?version=2` and `code.docx#section-3`. All of them point to real documents. | The scraper ignores some of them. We know which documents are in the fixture, so we just compare that list with what the scraper says it found. |
| 2 | Links are simple paths that are easy to join onto the site URL. | A page that uses a `<base href>` tag, links starting with `../`, and a filename with a space in it (`my%20policy.pdf`). | The scraper builds a wrong URL and gets a 404, or ends up on the wrong host. The local server logs every path it is asked for, and the test compares that log with a list of the paths we expect. |
| 3 | You can tell a link is a document just from its URL. | A link like `/policy/download?id=42` with no extension. The server returns a valid PDF with `Content-Disposition: attachment; filename="leave.pdf"`. | The scraper never finds this document because its extension filter skips the link. We compare the documents the scraper found with the list in the fixture, and this one is missing. |
| 4 | The `Content-Type` header can be trusted. | A valid PDF and a valid `.docx`, both sent with a generic `Content-Type: application/octet-stream` instead of `application/pdf` or the Word type. | The scraper rejects good documents just because of the header. Both files start with the right bytes (`%PDF` and `PK`), so we check that the scraper still reports them as successful downloads. |
| 5 | Documents are returned directly, without redirects. | Links that return `301` or `302`, including one that redirects to itself and one that redirects to a different website. | The scraper gets stuck in a loop, blows through its request limit, or downloads from somewhere it shouldn't. The local server's log shows how many requests were made and where they ended up. |
| 6 | Files are small enough to hold in memory and always arrive in full. | One link serving a very large file (around 2 GB), and another that promises 500 KB in `Content-Length` but cuts the connection after 1 KB. | The scraper hangs, crashes with a memory error, or reports the cut-off file as fine. We'd watch memory and run time, and compare the size the scraper reports with `Content-Length`. |
| 7 | Every link is a different document. | An index page linking to three different URLs (e.g. `/policy/leave.pdf`, `/policy/archive/leave.pdf` and `/policy/leave.pdf?download=1`) that all serve byte-identical copies of the same PDF. The expected result is that this content is counted once. | The same content is downloaded more than once, which wastes the scraper's 3–5 document and 20-request limit. We take a SHA-256 hash of each downloaded file; two downloads with the same hash means the scraper has failed. |
| 8 | The page is UTF-8 and the links are in the HTML source. | A page saved in `windows-1252` with a filename like `política.pdf`, and a second page where the links are only added by JavaScript. | The scraper crashes on the encoding, mangles the filename, or finds no documents at all. Any of these shows up as an error or as an empty or wrong list of links. |
