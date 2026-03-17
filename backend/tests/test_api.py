import unittest

from backend.app.compat import HTTPException
from backend.app.main import get_building, get_stats, list_buildings


class ApiTest(unittest.TestCase):
    def test_list_buildings_returns_evaluated_summaries(self) -> None:
        payload = list_buildings()

        self.assertEqual(len(payload), 5)
        self.assertEqual(payload[0].building_id, "PARIS-DEMO-0001")
        self.assertEqual(str(payload[0].status), "legal_today")
        self.assertGreater(payload[0].confidence, 0.9)
        self.assertEqual(str(payload[1].status), "illegal_today")

    def test_list_buildings_supports_arrondissement_filter(self) -> None:
        payload = list_buildings(min_arr=17, max_arr=20)

        self.assertEqual([building.building_id for building in payload], ["PARIS-DEMO-0002", "PARIS-DEMO-0004"])

    def test_get_building_returns_explainable_evaluation(self) -> None:
        payload = get_building("PARIS-DEMO-0002")

        self.assertEqual(str(payload.status), "illegal_today")
        self.assertEqual(payload.rule_version, "2026-baseline")
        self.assertGreaterEqual(len(payload.violations), 1)
        self.assertGreaterEqual(len(payload.explanations), 3)
        self.assertEqual(payload.violations[0].severity, "high")

    def test_get_building_returns_404_for_unknown_id(self) -> None:
        with self.assertRaises(HTTPException) as context:
            get_building("UNKNOWN")

        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Unknown building_id", context.exception.detail)

    def test_stats_aggregate_current_demo_inventory(self) -> None:
        payload = get_stats()
        self.assertEqual(
            payload.model_dump(),
            {
                "total_buildings": 5,
                "legal_today": 1,
                "illegal_today": 2,
                "unknown_insufficient_data": 2,
                "non_conforming_tolerated": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
