"""
test_fleet.py

Purpose:
    Verify that our simulated endpoint compliance rules work correctly.

Why this matters:
    Automated tests help catch mistakes when we change our policy or
    add features. They let us verify behavior without using real devices.

How to run:
    python3 -m unittest -v
"""

import unittest


# Import the policy-evaluation function from fleet.py.
# NOTE: Our current fleet.py does not expose this function yet.
# We will refactor fleet.py in the next step so these tests can
# call the compliance logic directly without running the whole report.
from fleet import evaluate_device


class TestEndpointCompliance(unittest.TestCase):
    """Tests for individual endpoint compliance decisions."""

    def setUp(self):
        """
        Create a standard simulated device and policy for each test.

        Each test gets its own copy so changes in one test do not
        accidentally affect another test.
        """
        self.policy = {
            "allowed_operating_systems": ["macOS", "Windows"],
            "minimum_os_versions": {
                "macOS": 14,
                "Windows": 10,
            },
            "require_encryption": True,
            "require_screen_lock": True,
        }

        self.device = {
            "id": "TEST-001",
            "owner": "Test User",
            "os": "macOS",
            "os_version": 15,
            "encryption": True,
            "screen_lock": True,
        }

    def test_fully_compliant_device(self):
        """A device meeting every policy requirement should pass."""
        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "COMPLIANT")
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["risk_level"], "LOW")

    def test_encryption_disabled(self):
        """A device without required encryption should fail."""
        self.device["encryption"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Encryption disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_screen_lock_disabled(self):
        """A device without the required screen lock should fail."""
        self.device["screen_lock"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Screen lock disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_unsupported_operating_system(self):
        """An OS not allowed by policy should receive high risk."""
        self.device["os"] = "Linux"

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn(
            "Unsupported operating system",
            result["issues"],
        )
        self.assertEqual(result["risk_level"], "HIGH")

    def test_os_version_too_old(self):
        """An OS below its configured minimum should fail."""
        self.device["os_version"] = 13

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("OS version too old", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")

    def test_multiple_issues(self):
        """A device can have multiple failures at the same time."""
        self.device["encryption"] = False
        self.device["screen_lock"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Encryption disabled", result["issues"])
        self.assertIn("Screen lock disabled", result["issues"])


# Run the tests when this file is executed directly.
# The command `python3 -m unittest -v` also discovers these tests.
if __name__ == "__main__":
    unittest.main(verbosity=2)
    