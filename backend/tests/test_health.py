import unittest

from backend.app.main import health
from rules.engine.evaluator import evaluate_building


class EvaluatorSmokeTest(unittest.TestCase):
    def test_health_endpoint_returns_ok(self) -> None:
        self.assertEqual(health(), {"status": "ok"})

    def test_missing_fields_returns_unknown(self) -> None:
        result = evaluate_building({"primary_use": "residential"})
        self.assertEqual(result.status, "unknown_insufficient_data")
        self.assertGreater(len(result.violations), 0)


if __name__ == "__main__":
    unittest.main()
