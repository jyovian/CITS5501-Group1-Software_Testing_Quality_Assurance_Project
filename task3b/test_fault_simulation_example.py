"""Automated checks for the Task 3b fault-simulation example."""

import unittest
from http.server import ThreadingHTTPServer
from threading import Thread

from fault_simulation_example import FakePolicyHandler, fetch_policy, run_demo


class FaultSimulationExampleTest(unittest.TestCase):
    """Check that the fake site behaves as expected and the error is reported."""

    def test_fake_index_links_to_unavailable_pdf(self):
        """The fake index page loads and links to the unavailable PDF."""

        server = ThreadingHTTPServer(("127.0.0.1", 0), FakePolicyHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            url = f"http://127.0.0.1:{server.server_port}/policy/"
            success, result = fetch_policy(url)
            self.assertTrue(success)
            self.assertIn(b"unavailable.pdf", result)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_scraper_reports_fake_server_error(self):
        """Requesting the PDF reports an HTTP 503 failure instead of crashing."""

        success, result = run_demo()

        self.assertFalse(success)
        self.assertIn("HTTP 503", result)


if __name__ == "__main__":
    unittest.main()
