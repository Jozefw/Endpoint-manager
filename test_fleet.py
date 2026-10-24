
"""
test_fleet.py

Purpose:
    Automatically verify endpoint compliance decisions and inventory
    data validation.

Run the tests from the project folder with:
    python3 -m unittest -v

Why this matters:
    Automated tests help catch regressions when the compliance engine
    changes. These tests use fictional devices and require no physical
    computers or paid services.
"""

import unittest

# Import the function being tested.
# The main report will not run during this import because fleet.py
# protects its main() call with an if __name__ == "__main__" check.
from fleet import evaluate_device


class TestEndpointCompliance(unittest.TestCase):
    """Tests for compliance decisions and invalid inventory data."""

    def setUp(self):
        """
        Prepare a fresh policy and sample device for every test.

        Each test gets its own copy so a change in one test cannot
        accidentally affect another test.
        """

        # Define the security requirements used by the test cases.
        self.policy = {
            "allowed_operating_systems": ["macOS", "Windows"],
            "minimum_os_versions": {
                "macOS": 14,
                "Windows": 10,
            },
            "require_encryption": True,
            "require_screen_lock": True,
        }

        # This device meets every policy requirement by default.
        # Individual tests change one or more values to test failures.
        self.device = {
            "id": "TEST-001",
            "owner": "Test User",
            "os": "macOS",
            "os_version": 15,
            "encryption": True,
            "screen_lock": True,
        }

    def test_fully_compliant_device(self):
        """A device meeting every requirement should pass."""
        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "COMPLIANT")
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["risk_level"], "LOW")

    def test_encryption_disabled(self):
        """Disabled required encryption should fail compliance."""
        self.device["encryption"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Encryption disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_screen_lock_disabled(self):
        """A disabled required screen lock should fail compliance."""
        self.device["screen_lock"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Screen lock disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_unsupported_operating_system(self):
        """An operating system outside the allowlist should be high risk."""
        self.device["os"] = "Linux"

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn(
            "Unsupported operating system",
            result["issues"],
        )
        self.assertEqual(result["risk_level"], "HIGH")

    def test_os_version_too_old(self):
        """An OS version below the configured minimum should fail."""
        self.device["os_version"] = 13

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("OS version too old", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")

    def test_multiple_issues(self):
        """The evaluator should report multiple security failures."""
        self.device["encryption"] = False
        self.device["screen_lock"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Encryption disabled", result["issues"])
        self.assertIn("Screen lock disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_missing_required_field(self):
        """Missing inventory information should be reported, not crash."""
        # Remove a field the evaluator needs to make a valid decision.
        del self.device["encryption"]

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn(
            "Missing required field: encryption",
            result["issues"],
        )
        self.assertEqual(result["risk_level"], "HIGH")

    def test_invalid_os_version_type(self):
        """A text OS version should be rejected as invalid inventory data."""
        # The version should be an integer, not a text string.
        self.device["os_version"] = "fifteen"

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Invalid OS version value", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")


# Allow this test file to run directly as well as through unittest.
if __name__ == "__main__":
    unittest.main(verbosity=2)
