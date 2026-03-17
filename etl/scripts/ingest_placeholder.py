"""Minimal ETL staging pipeline for the MVP demo inventory."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


DATASET_REGISTRY: dict[str, dict[str, Any]] = {
    "demo_paris_inventory": {
        "source_name": "Local MVP demo inventory",
        "source_url": "internal://illegal-structure/demo-paris-inventory",
        "license": "Internal demo data for scaffold validation",
        "records": [
            {
                "source_record_id": "demo-0001",
                "building_id": "PARIS-DEMO-0001",
                "address": "10 Rue de Rivoli",
                "arrondissement": 1,
                "height_m": 16.0,
                "primary_use": "residential",
                "zone_code": "R1",
                "heritage_protected": False,
            },
            {
                "source_record_id": "demo-0002",
                "building_id": "PARIS-DEMO-0002",
                "address": "12 Avenue de Clichy",
                "arrondissement": 17,
                "height_m": 22.0,
                "primary_use": "residential",
                "zone_code": "R1",
                "heritage_protected": False,
            },
            {
                "source_record_id": "demo-0003",
                "building_id": "PARIS-DEMO-0003",
                "address": "5 Rue du Chevaleret",
                "arrondissement": 13,
                "height_m": 20.0,
                "primary_use": "industrial",
                "zone_code": "C1",
                "heritage_protected": False,
            },
            {
                "source_record_id": "demo-0004",
                "building_id": "PARIS-DEMO-0004",
                "address": "3 Boulevard de Belleville",
                "arrondissement": 20,
                "height_m": None,
                "primary_use": "mixed_use",
                "zone_code": "C1",
                "heritage_protected": False,
            },
            {
                "source_record_id": "demo-0005",
                "building_id": "PARIS-DEMO-0005",
                "address": "8 Place des Vosges",
                "arrondissement": 4,
                "height_m": 17.5,
                "primary_use": "residential",
                "zone_code": "R1",
                "heritage_protected": True,
            },
        ],
    }
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_iso_date(value: str) -> str:
    date.fromisoformat(value)
    return value


def normalize_record(
    raw_record: dict[str, Any],
    *,
    dataset_name: str,
    source_name: str,
    source_url: str,
    license_name: str,
    extraction_date: str,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "building_id": raw_record["building_id"],
        "address": raw_record["address"],
        "arrondissement": raw_record["arrondissement"],
        "height_m": raw_record["height_m"],
        "primary_use": raw_record["primary_use"],
        "zone_code": raw_record["zone_code"],
        "heritage_protected": raw_record["heritage_protected"],
        "provenance": {
            "dataset_name": dataset_name,
            "source_name": source_name,
            "source_url": source_url,
            "source_record_id": raw_record["source_record_id"],
            "license": license_name,
            "extraction_date": extraction_date,
            "pipeline_run_id": run_id,
            "generated_at": generated_at,
            "record_hash_basis": {
                "building_id": raw_record["building_id"],
                "source_record_id": raw_record["source_record_id"],
            },
        },
    }


def run_pipeline(
    *,
    dataset: str,
    output_dir: Path,
    extraction_date: str,
    run_id: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    if dataset not in DATASET_REGISTRY:
        raise ValueError(f"Unsupported dataset '{dataset}'")

    extraction_date = _validate_iso_date(extraction_date)
    generated_at = generated_at or _utc_now_iso()
    dataset_spec = DATASET_REGISTRY[dataset]
    stage_dir = output_dir / dataset / extraction_date / run_id
    stage_dir.mkdir(parents=True, exist_ok=True)

    normalized_records = [
        normalize_record(
            raw_record,
            dataset_name=dataset,
            source_name=dataset_spec["source_name"],
            source_url=dataset_spec["source_url"],
            license_name=dataset_spec["license"],
            extraction_date=extraction_date,
            run_id=run_id,
            generated_at=generated_at,
        )
        for raw_record in dataset_spec["records"]
    ]

    records_path = stage_dir / "buildings.jsonl"
    records_path.write_text(
        "\n".join(json.dumps(record, sort_keys=True) for record in normalized_records) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "dataset": dataset,
        "record_count": len(normalized_records),
        "schema_version": "mvp-demo-v1",
        "stage_dir": str(stage_dir),
        "records_path": str(records_path),
        "source_name": dataset_spec["source_name"],
        "source_url": dataset_spec["source_url"],
        "license": dataset_spec["license"],
        "extraction_date": extraction_date,
        "pipeline_run_id": run_id,
        "generated_at": generated_at,
    }
    manifest_path = stage_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage a minimal Paris legality demo dataset.")
    parser.add_argument("--dataset", default="demo_paris_inventory")
    parser.add_argument("--output-dir", default="etl/staging")
    parser.add_argument("--extraction-date", default=date.today().isoformat())
    parser.add_argument("--run-id", default="local-demo")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    manifest = run_pipeline(
        dataset=args.dataset,
        output_dir=Path(args.output_dir),
        extraction_date=args.extraction_date,
        run_id=args.run_id,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
