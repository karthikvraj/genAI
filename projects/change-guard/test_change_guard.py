"""Behavioral checks for decisions and graph edge cases."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("change_guard", HERE / "change_guard.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ChangeGuardTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((HERE / "example.json").read_text())

    def test_wide_impact_is_review_not_automatic_approval(self):
        report = module.evaluate(self.data)
        self.assertEqual(report["decision"], "REVIEW")
        self.assertEqual([x["id"] for x in report["affected_services"]],
                         ["dns", "api", "analytics", "inference"])
        self.assertEqual(report["criticality_exposure"], 0.889)

    def test_untested_rollback_blocks(self):
        self.data["change"]["rollback_tested"] = False
        self.assertEqual(module.evaluate(self.data)["decision"], "BLOCK")

    def test_isolated_change_can_be_ready(self):
        self.data["change"]["target"] = "offline-training"
        self.assertEqual(module.evaluate(self.data)["decision"], "READY_FOR_HUMAN_APPROVAL")

    def test_cycle_does_not_loop_and_hash_is_stable(self):
        self.data["services"][0]["depends_on"] = ["inference"]
        result = module.evaluate(self.data)
        self.assertEqual(len(result["affected_services"]), 4)
        reordered = copy.deepcopy(self.data)
        reordered["change"] = dict(reversed(list(reordered["change"].items())))
        self.assertEqual(result["input_sha256"], module.evaluate(reordered)["input_sha256"])

    def test_bad_reference_rejected(self):
        self.data["services"][1]["depends_on"] = ["missing"]
        with self.assertRaises(module.ValidationError):
            module.evaluate(self.data)


if __name__ == "__main__":
    unittest.main()
