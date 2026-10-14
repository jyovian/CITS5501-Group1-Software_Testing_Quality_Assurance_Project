# Task 3b - fake server error example

This example checks how a scraper handles a server-side error. It starts a
small policy website on the local computer. The index page links to
`unavailable.pdf`, but the fake server returns `503 Service Unavailable` when
that link is requested. No request is sent to the real UWA policy website.

Run the demonstration from the repository root:

```bash
python3 task3b/fault_simulation_example.py
```

Expected output (the port number will be different):

```text
Request: http://127.0.0.1:12345/policy/unavailable.pdf
Success: False
Result: HTTP 503: Service Unavailable
```

The important result is that the error is caught and reported. The program
does not stop with an unhandled exception.

Run the automated test with:

```bash
python3 -m unittest discover -s task3b -p "test_*.py"
```

The example only uses modules from the Python standard library, so no extra
packages are needed.

## Use it with the prototype scraper

Keep the fake site running in one terminal:

```bash
python3 task3b/fault_simulation_example.py --serve
```

Its index is available at `http://127.0.0.1:8000/policy/`. The Task 1 Python
starter accepts a different start URL, so the completed prototype can be run
against this address in another terminal. Press `Ctrl+C` in the first terminal
when testing is finished.
