# Task 1 - Minimal prototype scraper

`prototype.py` fetches the UWA policy index page, finds links that look like
policy documents (`.pdf`, `.doc`, `.docx`, `.rtf`), downloads up to 5 of them
and prints metadata for each one. Downloaded files are not saved to disk.

## Requirements

- Python 3.10 or later
- No extra packages. The prototype only uses the Python standard library, so
  there is nothing to install or compile.

## Running it

From the repository root:

```bash
python3 task1/prototype.py
```

This uses the live index page
`https://uwa-policy.cits5501.arranstewart.io/policy/`.

Optional arguments:

```bash
python3 task1/prototype.py [START_URL] [--max-docs N] [--max-requests N]
```

- `START_URL` - a different index page, e.g. a local test server such as
  `http://127.0.0.1:8000/policy/` (see `task3b/README.md`)
- `--max-docs` - how many documents to download (default 5)
- `--max-requests` - total HTTP request limit, including the index page and
  any retries (default 20)

## Example output

```text
Fetching index page: https://uwa-policy.cits5501.arranstewart.io/policy/
  HTTP 200, 584187 bytes
Found 213 distinct document links on the same site.

[OK] https://uwa-policy.cits5501.arranstewart.io/policy/-/media/project/uwa/uwa/policy-library/policy/code-of-conduct/up26-2-code-of-conduct.pdf
  status:       200
  content type: application/pdf
  size:         163909 bytes
  first bytes:  b'%PDF-1.6'

...

Downloaded 5 of 5 documents using 6 of 20 requests.
```

For each document the prototype prints the URL, HTTP status, declared
content type, downloaded size and the first 8 bytes. PDF files should start
with `%PDF` and `.docx` files with `PK`. Older `.doc` files start with
different bytes (`\xd0\xcf\x11\xe0`).
