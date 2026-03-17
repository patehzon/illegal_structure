import unittest

from rules.engine.evaluator import evaluate_building


class EvaluatorTest(unittest.TestCase):
    def test_missing_fields_returns_unknown_with_missing_evidence(self) -> None:
        result = evaluate_building({"primary_use": "residential"})

        self.assertEqual(result.status, "unknown_insufficient_data")
        self.assertEqual(sorted(result.missing_evidence), ["height_m", "zone_code"])
        self.assertEqual(result.violations[0].rule_code, "DATA_MINIMUM_REQUIRED")

    def test_height_violation_returns_illegal(self) -> None:
        result = evaluate_building(
            {
                "building_id": "PARIS-DEMO-HEIGHT",
                "height_m": 22,
                "primary_use": "residential",
                "zone_code": "R1",
            }
        )

        self.assertEqual(result.status, "illegal_today")
        self.assertEqual(result.violations[0].rule_code, "HEIGHT_MAX_BY_ZONE")
        self.assertGreaterEqual(result.confidence, 0.9)

    def test_use_violation_returns_illegal(self) -> None:
        result = evaluate_building(
            {
                "building_id": "PARIS-DEMO-USE",
                "height_m": 17,
                "primary_use": "industrial",
                "zone_code": "C1",
            }
        )

        self.assertEqual(result.status, "illegal_today")
        self.assertEqual(result.violations[0].rule_code, "LAND_USE_COMPATIBILITY")

    def test_heritage_flag_keeps_result_unknown_until_manual_review(self) -> None:
        result = evaluate_building(
            {
                "building_id": "PARIS-DEMO-HERITAGE",
                "height_m": 17,
                "primary_use": "residential",
                "zone_code": "R1",
                "heritage_protected": True,
            }
        )

        self.assertEqual(result.status, "unknown_insufficient_data")
        self.assertIn("heritage_override_review", result.missing_evidence)
        self.assertEqual(result.violations[0].rule_code, "HERITAGE_OVERRIDE")

    def test_compliant_building_returns_legal(self) -> None:
        result = evaluate_building(
            {
                "building_id": "PARIS-DEMO-LEGAL",
                "height_m": 17,
                "primary_use": "mixed_use",
                "zone_code": "C1",
                "heritage_protected": False,
            }
        )

        self.assertEqual(result.status, "legal_today")
        self.assertEqual(result.rule_version, "2026-baseline")
        self.assertEqual(result.missing_evidence, [])
        self.assertEqual(result.violations, [])


if __name__ == "__main__":
    unittest.main()
