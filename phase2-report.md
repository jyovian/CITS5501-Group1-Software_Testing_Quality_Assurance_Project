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

### 4.1 Happy-path assumptions

We started by writing down what has to go right for a scraper to work on the
"normal" path. Most of these are things a team would never think to check,
because the real site happens to behave nicely:

- Policy links end in `.pdf` or `.docx`, in lowercase, with nothing after them.
- Links are either full URLs or simple relative paths.
- Each document is only linked once.
- The index page is valid UTF-8 HTML, and the links are already in the page
  source rather than added later by JavaScript.
- Asking for a document gets a `200 OK` straight away, with no redirects.
- The `Content-Type` header is correct, and a `.pdf` link really gives you a PDF.
- Files are a normal size and download completely.
- The server answers quickly.

### 4.2 Adversarial test ideas

Each idea below targets one of these assumptions. We would run all of them
against a local server or a saved HTML page, not the live site, since we can
control exactly what gets sent back.

| # | Assumption being challenged | Input / environment used | What counts as failure, and how it's detected |
|---|---|---|---|
| 1 | Links always end in a lowercase extension. | An index page with links like `Policy.PDF`, `leave.pdf?version=2` and `code.docx#section-3`. All of them point to real documents. | The scraper ignores some of them. We know which documents are in the fixture, so we just compare that list with what the scraper says it found. |
| 2 | Links are simple paths that are easy to join onto the site URL. | A page that uses a `<base href>` tag, links starting with `../`, and a filename with a space in it (`my%20policy.pdf`). | The scraper builds a wrong URL and gets a 404, or ends up on the wrong host. We'd log the final URLs the scraper requests and check them by hand against the expected ones. |
| 3 | If a link ends in `.pdf`, you get a PDF back. | A local server that answers a `.pdf` link with `200 OK` and an HTML "page not found" page. | The scraper says the download worked. This is easy to catch: the file starts with `<html` instead of `%PDF`, but the scraper still reports success. |
| 4 | The `Content-Type` header can be trusted. | Two responses: a real PDF sent as `application/octet-stream`, and an HTML page sent as `application/pdf`. | The scraper throws away the good PDF or keeps the HTML page. We check this by comparing what the scraper decided with the first few bytes of each file. |
| 5 | Documents are returned directly, without redirects. | Links that return `301` or `302`, including one that redirects to itself and one that redirects to a different website. | The scraper gets stuck in a loop, blows through its request limit, or downloads from somewhere it shouldn't. The local server's log shows how many requests were made and where they ended up. |
| 6 | Files are small enough to hold in memory and always arrive in full. | One link serving a very large file (around 2 GB), and another that promises 500 KB in `Content-Length` but cuts the connection after 1 KB. | The scraper hangs, crashes with a memory error, or reports the cut-off file as fine. We'd watch memory and run time, and compare the size the scraper reports with `Content-Length`. |
| 7 | Every link is a different document. | An index page with the same PDF linked several times, with different link text, a different letter case or a trailing `/`. | The scraper downloads the same file again and wastes its 3–5 document and 20-request limit. Repeated URLs show up in both the scraper output and the server log. |
| 8 | The page is UTF-8 and the links are in the HTML source. | A page saved in `windows-1252` with a filename like `política.pdf`, and a second page where the links are only added by JavaScript. | The scraper crashes on the encoding, mangles the filename, or finds no documents at all. Any of these shows up as an error or as an empty or wrong list of links. |
