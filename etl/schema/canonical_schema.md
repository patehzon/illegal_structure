# Canonical schema (draft)

## building
- `building_id` (string, primary key)
- `source_building_ids` (array<string>)
- `geometry` (polygon/multipolygon)
- `height_m` (float, nullable)
- `levels` (int, nullable)
- `primary_use` (enum)
- `construction_year` (int, nullable)

## address
- `address_id` (string)
- `building_id` (string, fk)
- `street_number` (string)
- `street_name` (string)
- `postcode` (string)
- `arrondissement` (int)

## parcel
- `parcel_id` (string)
- `building_id` (string, fk)
- `cadastral_ref` (string)

## provenance
- `record_id` (string)
- `dataset_name` (string)
- `dataset_version` (string)
- `extracted_at` (datetime)
- `license` (string)
- `confidence` (float)
