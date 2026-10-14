import unittest

from fault_simulation_example import run_demo


class FaultSimulationExampleTest(unittest.TestCase):
    def test_scraper_reports_fake_server_error(self):
        success, result = run_demo()

        self.assertFalse(success)
        self.assertIn("HTTP 500", result)


if __name__ == "__main__":
    unittest.main()
