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

<!-- Owner: ______
     Write ONLY inside this section. Delete these comments when done. -->

<!-- 5–8 ideas for breaking another team's scraper. -->

| # | Assumption being challenged | Input / environment used | What counts as failure, and how it's detected |
|---|---|---|---|
| 1 | | | |
