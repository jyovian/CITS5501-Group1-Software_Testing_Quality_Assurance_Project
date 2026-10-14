"""Small fault-simulation example for Task 3b.

The local server acts like the policy website, but deliberately returns an
HTTP 500 response.  This lets us check error handling without sending test
requests to the real website.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


class FakePolicyHandler(BaseHTTPRequestHandler):
    """Return a server error for the policy page used by the demo."""

    def do_GET(self):
        if self.path == "/policy/example.html":
            body = b"Temporary server problem"
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, "Not found")

    def log_message(self, format, *args):
        """Keep the demonstration output short and readable."""


def fetch_policy(url, timeout=2):
    """Fetch one policy page and return a result that the caller can inspect."""

    try:
        with urlopen(url, timeout=timeout) as response:
            return True, response.read()
    except HTTPError as error:
        message = f"HTTP {error.code}: {error.reason}"
        error.close()
        return False, message
    except URLError as error:
        return False, f"Network error: {error.reason}"


def run_demo():
    """Start the fake server, make one request, and then stop the server."""

    server = ThreadingHTTPServer(("127.0.0.1", 0), FakePolicyHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{server.server_port}/policy/example.html"
    try:
        success, result = fetch_policy(url)
        print(f"Request: {url}")
        print(f"Success: {success}")
        print(f"Result: {result}")
        return success, result
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    run_demo()
