# ETL scaffold

This module will ingest and normalize all datasets needed to classify building legality in Paris.

## Planned datasets (initial)

- Building footprints / geometry sources
- Address and street number sources
- Parcel/cadastre references
- Zoning and regulatory layers
- Heritage/protection layers

## Pipeline stages

1. `extract`: pull source snapshots with source metadata.
2. `normalize`: convert to canonical schema and CRS.
3. `link`: deduplicate and join building/address/parcel relations.
4. `load`: write to PostGIS staging + curated tables.
5. `validate`: quality checks and anomaly reporting.

Use `etl/scripts/` for executable ingestion modules.
