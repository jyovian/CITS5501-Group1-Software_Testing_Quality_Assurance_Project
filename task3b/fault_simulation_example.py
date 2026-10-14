"""Small fault-simulation example for Task 3b.

The local server acts like the policy website, but deliberately returns an
HTTP 503 response.  This lets us check error handling without sending test
requests to the real website.
"""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


class FakePolicyHandler(BaseHTTPRequestHandler):
    """Serve a small policy index with one unavailable PDF link."""

    def do_GET(self):
        if self.path == "/policy/":
            body = (
                b"<!doctype html><html><body>"
                b'<a href="unavailable.pdf">Example policy</a>'
                b"</body></html>"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/policy/unavailable.pdf":
            body = b"Temporary server problem"
            self.send_response(503)
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

    url = f"http://127.0.0.1:{server.server_port}/policy/unavailable.pdf"
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


def serve(port):
    """Run the fake policy site until the user stops it."""

    server = ThreadingHTTPServer(("127.0.0.1", port), FakePolicyHandler)
    print(f"Fake policy index: http://127.0.0.1:{server.server_port}/policy/")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping fake server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Task 3b fake policy site.")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="keep the fake site running so another scraper can use it",
    )
    parser.add_argument("--port", type=int, default=8000, help="port for --serve")
    args = parser.parse_args()

    if args.serve:
        serve(args.port)
    else:
        run_demo()
