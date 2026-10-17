"""Minimal prototype policy-document scraper (CITS5501 Phase 2, Task 1).

Summary
-------
This program does four things:

1. Downloads the policy index page (by default the live UWA policy site).
2. Looks through every link on that page and keeps the ones that look like
   policy documents: links on the same website whose file name ends in
   .pdf, .doc, .docx or .rtf.
3. Downloads the first few of those documents (5 by default), never making
   more than 20 HTTP requests in total.
4. Prints details about each download: the URL, HTTP status code, content
   type, size, and the first few bytes of the file.

Files are not saved to disk. Only the Python standard library is used, so
there is nothing to install. See README.md for how to run it.
"""

import argparse
import time
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

# The page we start from if no other URL is given on the command line.
DEFAULT_START_URL = "https://uwa-policy.cits5501.arranstewart.io/policy/"

# A link counts as a policy document if its path ends in one of these.
DOCUMENT_EXTENSIONS = (".pdf", ".doc", ".docx", ".rtf")

# Sent with every request so the server can see who is making them.
USER_AGENT = "CITS5501-Group1-prototype/0.1 (student project)"

# How many bytes from the start of each file to print.
# PDFs start with "%PDF" and .docx files start with "PK".
NUM_PREVIEW_BYTES = 8

# How long to wait after a 429 if Retry-After is missing or not a plain number
# of seconds (it may also be a date), and the longest we are willing to wait.
DEFAULT_RETRY_WAIT = 10
MAX_RETRY_WAIT = 60


class LinkCollector(HTMLParser):
    """Collects the href value of every <a> tag in a page."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    # HTMLParser calls this method for every opening tag it finds in the page.
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # We only care about links, i.e. <a href="..."> tags.
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.hrefs.append(value)


class BudgetExhausted(Exception):
    """Raised when the request limit is reached before a request can be made."""


def retry_wait_seconds(retry_after: str | None) -> int:
    """Returns how many seconds to wait, given a Retry-After header value.

    Only the "number of seconds" form is understood. If the header is missing,
    negative, or in the HTTP-date form, DEFAULT_RETRY_WAIT is used instead.
    The result is capped at MAX_RETRY_WAIT.
    """
    try:
        wait = int(retry_after) if retry_after is not None else DEFAULT_RETRY_WAIT
    except ValueError:
        wait = DEFAULT_RETRY_WAIT
    if wait < 0:
        wait = DEFAULT_RETRY_WAIT
    return min(wait, MAX_RETRY_WAIT)


class RequestBudget:
    """Counts HTTP requests and refuses to go over a fixed limit."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.used = 0

    def remaining(self) -> int:
        return self.limit - self.used

    def fetch(self, url: str) -> tuple[int, str, bytes]:
        """GET a URL. Returns (status, content type, body).

        If the server says we are rate limited (HTTP 429), wait for the
        number of seconds in its Retry-After header and try again. Every
        attempt counts against the budget; raises BudgetExhausted when it
        runs out.
        """
        while True:
            # Stop if we have already used up all our allowed requests.
            if self.remaining() <= 0:
                raise BudgetExhausted("request budget used up")
            self.used += 1

            request = Request(url, headers={"User-Agent": USER_AGENT})
            try:
                # Successful response (2xx): read the whole body into memory.
                with urlopen(request) as response:
                    return response.status, response.headers.get("Content-Type", ""), response.read()
            except HTTPError as error:
                # urlopen raises HTTPError for 4xx/5xx status codes.
                if error.code == 429:
                    # "Too Many Requests": wait as long as the server asks, then retry.
                    wait = retry_wait_seconds(error.headers.get("Retry-After"))
                    print(f"  (rate limited, waiting {wait}s)")
                    time.sleep(wait)
                    continue
                # Any other error status: return it so it can be printed as a failure.
                return error.code, error.headers.get("Content-Type", ""), error.read()


def find_document_links(index_url: str, html: str) -> list[str]:
    """Returns distinct, absolute document URLs on the same host as the index page."""
    # Pull every <a href> out of the page.
    collector = LinkCollector()
    collector.feed(html)

    index_host = urlparse(index_url).netloc
    documents: list[str] = []
    for href in collector.hrefs:
        # Turn relative links like "/policy/x.pdf" into full URLs.
        url = urljoin(index_url, href)
        parsed = urlparse(url)

        # Skip links to other websites.
        if parsed.netloc != index_host:
            continue

        # Skip links that don't end in a document extension (web pages, images, etc.).
        # Only the path is checked, so "x.pdf?v=2" still counts as a PDF.
        if not parsed.path.lower().endswith(DOCUMENT_EXTENSIONS):
            continue

        # Skip duplicates, but keep the order links appear in on the page.
        if url not in documents:
            documents.append(url)
    return documents


def main() -> None:
    # Read the optional command-line arguments (see README.md).
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start_url", nargs="?", default=DEFAULT_START_URL, help="policy index page URL")
    parser.add_argument("--max-docs", type=int, default=5, help="number of documents to download (default 5)")
    parser.add_argument("--max-requests", type=int, default=20, help="total HTTP request limit (default 20)")
    args = parser.parse_args()

    # Every request below, including the index page, goes through this budget.
    budget = RequestBudget(args.max_requests)

    # Step 1: download the index page.
    print(f"Fetching index page: {args.start_url}")
    try:
        status, _, body = budget.fetch(args.start_url)
    except BudgetExhausted:
        print("Request limit reached before the index page loaded; giving up.")
        return
    print(f"  HTTP {status}, {len(body)} bytes")
    if status != 200:
        print("Could not fetch the index page; giving up.")
        return

    # Step 2: find the links that look like policy documents.
    links = find_document_links(args.start_url, body.decode("utf-8", errors="replace"))
    print(f"Found {len(links)} distinct document links on the same site.\n")

    # Steps 3 and 4: download the first few documents and print details for each.
    successes = 0
    for url in links[: args.max_docs]:
        if budget.remaining() <= 0:
            print("Request limit reached; giving up.")
            break

        try:
            status, content_type, data = budget.fetch(url)
        except BudgetExhausted:
            print("Request limit reached; giving up.")
            break

        # A download counts as successful if the server returned 200 OK.
        ok = status == 200
        successes += ok

        print(f"[{'OK' if ok else 'FAILED'}] {url}")
        print(f"  status:       {status}")
        print(f"  content type: {content_type or '(none)'}")
        print(f"  size:         {len(data)} bytes")
        print(f"  first bytes:  {data[:NUM_PREVIEW_BYTES]!r}\n")

    # Final summary line.
    print(f"Downloaded {successes} of {min(len(links), args.max_docs)} documents "
          f"using {budget.used} of {budget.limit} requests.")


# Only run main() when this file is run directly, not when it is imported.
if __name__ == "__main__":
    main()
