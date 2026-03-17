# Data sources (to validate and operationalize)

This file tracks candidate data providers and ingestion readiness.

## Candidate source families

- Building geometry inventories
- Address databases (street number precision required)
- Parcel/cadastre data
- Zoning/planning maps and text regulations
- Heritage/protection layers

## For each source, record

- Owner/publisher
- License and redistribution rights
- Spatial coverage and update frequency
- Required transformations
- Quality caveats

## MVP staging provenance fields

The current ETL skeleton writes the following provenance fields per staged
building record:

- `dataset_name`
- `source_name`
- `source_url`
- `source_record_id`
- `license`
- `extraction_date`
- `pipeline_run_id`
- `generated_at`

These fields are the minimum required to keep legality outputs reproducible and
to support later lineage joins from evaluation snapshots back to staged source
records.
