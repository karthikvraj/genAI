import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rollout_lab", ROOT / "rollout_lab.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class RolloutLabTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "example.json").read_text())

    def test_regression_recommends_rollback(self):
        report = app.evaluate(self.data)
        self.assertEqual(report["decision"], "ROLLBACK_RECOMMENDED")
        self.assertEqual(report["windows"][1]["findings"], ["ERROR_REGRESSION_CONFIDENT"])

    def test_clean_windows_candidate(self):
        self.data["windows"][1]["canary"]["errors"] = 7
        self.data["windows"][1]["canary"]["latency_ms"] = [92, 96, 100, 105, 120]
        self.assertEqual(app.evaluate(self.data)["decision"], "PROMOTION_CANDIDATE")

    def test_small_sample_holds(self):
        self.data["windows"][0]["canary"]["requests"] = 50
        self.assertEqual(app.evaluate(self.data)["windows"][0]["status"], "HOLD")

    def test_latency_guardrail_reviews(self):
        self.data["windows"][1]["canary"]["errors"] = 7
        self.assertEqual(app.evaluate(self.data)["decision"], "REVIEW")

    def test_invalid_counts_rejected(self):
        self.data["windows"][0]["canary"]["errors"] = 1001
        with self.assertRaises(app.InvalidWindow):
            app.evaluate(self.data)

    def test_key_order_does_not_change_fingerprint(self):
        changed = copy.deepcopy(self.data)
        changed["policy"] = dict(reversed(list(changed["policy"].items())))
        self.assertEqual(app.evaluate(self.data)["input_sha256"], app.evaluate(changed)["input_sha256"])

    def test_one_latency_outlier_does_not_trip_the_p95_guardrail(self):
        data = json.loads((ROOT / "noisy-sample.json").read_text())
        report = app.evaluate(data)
        noisy_window = report["windows"][1]
        self.assertEqual(report["decision"], "PROMOTION_CANDIDATE")
        self.assertEqual(noisy_window["status"], "CLEAN")
        latencies = data["windows"][1]["canary"]["latency_ms"]
        self.assertEqual(len(latencies), 20)
        self.assertEqual(max(latencies), 300)
        self.assertLess(
            noisy_window["p95_latency_ratio"],
            data["policy"]["max_p95_ratio"],
        )


if __name__ == "__main__":
    unittest.main()
