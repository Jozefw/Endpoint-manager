
"""
test_fleet.py

Purpose:
    Test endpoint compliance decisions and inventory validation.

Run from the project folder:
    python3 -m unittest -v

All tests use simulated data. No physical devices or external services
are required.
"""

import unittest

# Import the evaluator without running the fleet report.
from fleet import evaluate_device


class TestEndpointCompliance(unittest.TestCase):
    """Verify policy decisions and safe handling of invalid inventory."""

    def setUp(self):
        """Create a fresh policy and device for every test."""

        # This policy permits macOS and Windows with minimum versions.
        self.policy = {
            "allowed_operating_systems": ["macOS", "Windows"],
            "minimum_os_versions": {
                "macOS": 14,
                "Windows": 10,
            },
            "require_encryption": True,
            "require_screen_lock": True,
        }

        # This sample device passes all requirements by default.
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
        """An unapproved OS should be marked high risk."""
        self.device["os"] = "Linux"

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Unsupported operating system", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")

    def test_os_version_too_old(self):
        """An OS below the configured minimum should fail."""
        self.device["os_version"] = 13

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("OS version too old", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")

    def test_multiple_issues(self):
        """Multiple security failures should all be reported."""
        self.device["encryption"] = False
        self.device["screen_lock"] = False

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Encryption disabled", result["issues"])
        self.assertIn("Screen lock disabled", result["issues"])
        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_missing_required_field(self):
        """Missing inventory fields should not cause a crash."""
        del self.device["encryption"]

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn(
            "Missing required field: encryption",
            result["issues"],
        )
        self.assertEqual(result["risk_level"], "HIGH")

    def test_invalid_os_version_type(self):
        """A text OS version should be rejected safely."""
        self.device["os_version"] = "fifteen"

        result = evaluate_device(self.device, self.policy)

        self.assertEqual(result["status"], "NON-COMPLIANT")
        self.assertIn("Invalid OS version value", result["issues"])
        self.assertEqual(result["risk_level"], "HIGH")


# Allow this file to run directly as well as through unittest discovery.
if __name__ == "__main__":
    unittest.main(verbosity=2)
