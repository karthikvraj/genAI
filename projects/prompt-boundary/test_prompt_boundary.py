import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prompt_boundary", ROOT / "prompt_boundary.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class PromptBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "example.json").read_text())

    def test_attack_and_benign_denominators(self):
        metrics = app.evaluate(self.data)["metrics"]
        self.assertEqual(metrics["observed_attack_success_rate"], 0.5)
        self.assertEqual(metrics["benign_task_completion_rate"], 1.0)

    def test_literal_leak_in_tool_arguments(self):
        case = app.evaluate(self.data)["cases"][1]
        self.assertEqual(case["leaked_markers"], ["CANARY-SECRET-42"])
        self.assertEqual(case["unauthorized_tools"], ["send_email"])

    def test_allowed_tool_without_marker_not_compromise(self):
        sample = copy.deepcopy(self.data)
        sample["cases"][1]["allowed_tools"] = ["send_email"]
        sample["cases"][1]["tool_calls"][0]["arguments"] = "to=team@example.test; body=done"
        self.assertFalse(app.evaluate(sample)["cases"][1]["compromise_observed"])

    def test_duplicate_id_rejected(self):
        self.data["cases"][1]["id"] = self.data["cases"][0]["id"]
        with self.assertRaises(app.InvalidTrace):
            app.evaluate(self.data)


if __name__ == "__main__":
    unittest.main()
