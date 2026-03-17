import json
import tempfile
import unittest
from pathlib import Path

from etl.scripts.ingest_placeholder import run_pipeline


class EtlPipelineTest(unittest.TestCase):
    def test_run_pipeline_writes_manifest_and_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest = run_pipeline(
                dataset="demo_paris_inventory",
                output_dir=Path(tmp_dir),
                extraction_date="2026-03-01",
                run_id="test-run",
                generated_at="2026-03-17T12:00:00Z",
            )

            stage_dir = Path(manifest["stage_dir"])
            manifest_path = stage_dir / "manifest.json"
            records_path = stage_dir / "buildings.jsonl"

            self.assertTrue(manifest_path.exists())
            self.assertTrue(records_path.exists())
            self.assertEqual(manifest["record_count"], 5)

            persisted_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(persisted_manifest["pipeline_run_id"], "test-run")
            self.assertEqual(persisted_manifest["extraction_date"], "2026-03-01")

            first_record = json.loads(records_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(first_record["building_id"], "PARIS-DEMO-0001")
            self.assertEqual(first_record["provenance"]["source_record_id"], "demo-0001")
            self.assertEqual(first_record["provenance"]["pipeline_run_id"], "test-run")

    def test_run_pipeline_rejects_unknown_datasets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(ValueError):
                run_pipeline(
                    dataset="missing_dataset",
                    output_dir=Path(tmp_dir),
                    extraction_date="2026-03-01",
                    run_id="test-run",
                    generated_at="2026-03-17T12:00:00Z",
                )


if __name__ == "__main__":
    unittest.main()
