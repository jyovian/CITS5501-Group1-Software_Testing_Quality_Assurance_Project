# Task 3b - fake server error example

This example checks how a scraper handles a server-side error. It starts a
small HTTP server on the local computer and makes the server return `503
Service Unavailable` for a policy page. No request is sent to the real UWA
policy website.

Run the demonstration from the repository root:

```bash
python3 task3b/fault_simulation_example.py
```

Expected output (the port number will be different):

```text
Request: http://127.0.0.1:12345/policy/example.html
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
