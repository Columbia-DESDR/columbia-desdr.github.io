# CHIRPS Pipeline Guide

This document walks through how to use `chirps_pipeline.py` to extract CHIRPS rainfall data for any country or region and produce the two CSV files the Sliders dashboard needs: `chirps_raw.csv` and `admin_raw.csv`.

There are two ways to provide admin boundaries: **GEE boundaries** (no local files needed) or a **local shapefile**. Both are demonstrated below with real, tested examples.

---

## Prerequisites

### 1. Install Python dependencies

```bash
pip3 install earthengine-api pandas geopandas fiona requests
```

### 2. Authenticate with Google Earth Engine (one-time)

```bash
python3 -c "import ee; ee.Authenticate()"
```

This opens a browser window. Sign in with your Google account and authorize access. On success it prints `Successfully saved authorization token.`

### 3. Register your GCP project for Earth Engine (one-time)

1. Go to: `https://console.cloud.google.com/earth-engine/configuration?project=YOUR_PROJECT_ID`
2. Register for noncommercial/research use.
3. Go to: `https://console.developers.google.com/apis/api/earthengine.googleapis.com/overview?project=YOUR_PROJECT_ID`
4. Click **Enable** to turn on the Earth Engine API.
5. Update the project ID in `initialize_earth_engine()` in `chirps_pipeline.py` (currently set to `desdr-testing-project`).

---

## Example 1: GEE Boundaries (no shapefile needed)

Use this when you don't have a local shapefile. The script pulls admin boundaries directly from GEE's FAO GAUL dataset.

### Config file: `examples/example1_gee_config.json`

```json
{
  "source": {
    "shapefile": null,
    "use_gee_boundaries": true,
    "country_name": "Kenya",
    "admin_level": 2
  },

  "filter": {
    "admin_field": "ADM2_NAME",
    "admin_names": ["Nairobi", "Mombasa"]
  },

  "date_range": {
    "start_date": "2023-01-01",
    "end_date": "2024-01-01"
  },

  "season": {
    "early_first": 9,
    "early_last": 17,
    "late_first": 28,
    "late_last": 36
  },

  "output_dir": "./examples/output_gee"
}
```

**What each field means:**

| Field | Value | Why |
|---|---|---|
| `use_gee_boundaries` | `true` | Pull boundaries from GEE instead of a local file |
| `country_name` | `"Kenya"` | Country to extract from the GAUL dataset |
| `admin_level` | `2` | District level (0=country, 1=province, 2=district) |
| `admin_field` | `"ADM2_NAME"` | Column name for district names in GAUL level 2 |
| `admin_names` | `["Nairobi", "Mombasa"]` | Only process these two districts |
| `start_date` / `end_date` | 2023 | One year of CHIRPS data |
| `early_first`..`late_last` | 9-17, 28-36 | Kenya's long rains (Mar-Jun) and short rains (Oct-Dec) |

### Run it

```bash
python3 chirps_pipeline.py --config examples/example1_gee_config.json
```

### Expected output

```
✓ Google Earth Engine initialized successfully

 Step 1: Loading admin boundaries from Google Earth Engine
   Country: Kenya
   Admin level: 2
   Found 74 admin areas in Kenya
   Filtered to 2 specified areas: ['Nairobi', 'Mombasa']
   ✓ Loaded 2 admin boundaries

 Step 2: Converting shapefile to Earth Engine format...
   Created FeatureCollection with 2 features

 Step 3: Loading CHIRPS PENTAD dataset from Earth Engine...
   Date filter: 2023-01-01 to 2024-01-01
   CHIRPS data range: 2023-01-01 to 2023-12-26 (72 images)

 Step 4: Calculating spatial averages (this may take several minutes)...
   Total records: 144
   ✓ Dataset size OK - using direct download
   ✓ Downloaded 144 records

 Step 6: Creating admin defaults file...
   ✓ Created defaults for 2 admin areas

 Step 7: Saving output files...
   ✓ Saved: ./examples/output_gee/chirps_raw.csv
   ✓ Saved: ./examples/output_gee/admin_raw.csv

✅ Pipeline complete!
```

### Result: `chirps_raw.csv` (144 rows, 21 columns)

| system:index | ADM0_NAME | ADM2_NAME | mean | month | pentad | year |
|---|---|---|---|---|---|---|
| 20230101_0000...0000 | Kenya | Mombasa | 3.12 | 1.0 | 1.0 | 2023 |
| 20230101_0000...0001 | Kenya | Nairobi | 4.30 | 1.0 | 1.0 | 2023 |
| 20230106_0000...0000 | Kenya | Mombasa | 3.47 | 1.0 | 2.0 | 2023 |

Each row = one district's average rainfall for one 5-day pentad.

### Result: `admin_raw.csv`

| district | gid | chirps_early_first | chirps_early_last | chirps_late_first | chirps_late_last |
|---|---|---|---|---|---|
| Mombasa | 51344 | 9 | 17 | 28 | 36 |
| Nairobi | 51360 | 9 | 17 | 28 | 36 |

---

## Example 2: Local Shapefile

Use this when you have your own `.shp` file with custom admin boundaries.

### Config file: `examples/example2_shapefile_config.json`

```json
{
  "source": {
    "shapefile": "./examples/senegal_shapefile/senegal_districts.shp",
    "use_gee_boundaries": false,
    "country_name": null,
    "admin_level": 2
  },

  "filter": {
    "admin_field": "ADM2_NAME",
    "admin_names": ["Dakar", "Thies"]
  },

  "date_range": {
    "start_date": "2022-01-01",
    "end_date": "2023-01-01"
  },

  "season": {
    "early_first": 18,
    "early_last": 27,
    "late_first": 28,
    "late_last": 36
  },

  "output_dir": "./examples/output_shapefile"
}
```

**Key differences from Example 1:**

| Field | Value | Why |
|---|---|---|
| `shapefile` | `"./examples/senegal_shapefile/senegal_districts.shp"` | Path to your local `.shp` file |
| `use_gee_boundaries` | `false` | Read boundaries from the shapefile, not GEE |
| `admin_field` | `"ADM2_NAME"` | The column in *your* shapefile that holds district names. Inspect your shapefile to find the right column -- it might be `NAME_2`, `DISTRICT`, `GID`, etc. |
| `admin_names` | `["Dakar", "Thies"]` | Only process these districts (out of 3 in the file). Omit to process all. |
| Season dekads | 18-27, 28-36 | Senegal's rainy season (Jun-Dec) |

### Run it

```bash
python3 chirps_pipeline.py --config examples/example2_shapefile_config.json
```

### Expected output

```
✓ Google Earth Engine initialized successfully

 Step 1: Loading shapefile from ./examples/senegal_shapefile/senegal_districts.shp
   Found 3 features in shapefile
   Filtered to 2 specified admin areas: ['Dakar', 'Thies']
   Using admin field: ADM2_NAME
   Using admin code field: ADM2_CODE

 Step 2: Converting shapefile to Earth Engine format...
   Created FeatureCollection with 2 features

 Step 3: Loading CHIRPS PENTAD dataset from Earth Engine...
   Date filter: 2022-01-01 to 2023-01-01
   CHIRPS data range: 2022-01-01 to 2022-12-26 (72 images)

 Step 4: Calculating spatial averages (this may take several minutes)...
   Total records: 144
   ✓ Dataset size OK - using direct download
   ✓ Downloaded 144 records

 Step 6: Creating admin defaults file...
   ✓ Created defaults for 2 admin areas

 Step 7: Saving output files...
   ✓ Saved: ./examples/output_shapefile/chirps_raw.csv
   ✓ Saved: ./examples/output_shapefile/admin_raw.csv

✅ Pipeline complete!
```

### Result: `chirps_raw.csv` (144 rows, 21 columns)

| system:index | ADM0_NAME | ADM2_NAME | mean | month | pentad | year |
|---|---|---|---|---|---|---|
| 20220101_0000...0000 | Senegal | Dakar | 0.13 | 1.0 | 1.0 | 2022 |
| 20220101_0000...0002 | Senegal | Thies | 0.14 | 1.0 | 1.0 | 2022 |
| 20220106_0000...0000 | Senegal | Dakar | 0.08 | 1.0 | 2.0 | 2022 |

### Result: `admin_raw.csv`

| district | gid | chirps_early_first | chirps_early_last | chirps_late_first | chirps_late_last |
|---|---|---|---|---|---|
| Dakar | 1382 | 18 | 27 | 28 | 36 |
| Thies | 25344 | 18 | 27 | 28 | 36 |

---

## Using CLI flags instead of a config file

You can skip the config file and pass everything as command-line arguments.

### GEE boundaries via CLI

```bash
python3 chirps_pipeline.py \
  --use-gee-boundaries \
  --country-name "Kenya" \
  --admin-level 2 \
  --admin-names "Nairobi,Mombasa" \
  --start-date "2023-01-01" \
  --end-date "2024-01-01" \
  --output-dir ./output_kenya
```

### Local shapefile via CLI

```bash
python3 chirps_pipeline.py \
  --shapefile ./path/to/your_boundaries.shp \
  --admin-field ADM2_NAME \
  --admin-names "Dakar,Thies" \
  --start-date "2022-01-01" \
  --end-date "2023-01-01" \
  --output-dir ./output_senegal
```

### Config file with CLI overrides

CLI arguments take precedence over the config file. Useful for quick one-off changes:

```bash
python3 chirps_pipeline.py \
  --config my_config.json \
  --admin-names "Nairobi" \
  --output-dir ./output_nairobi_only
```

---

## How to find the right `admin_field` for your shapefile

If you have a shapefile and aren't sure what column holds the district names:

```python
import geopandas as gpd
gdf = gpd.read_file("your_file.shp")
print(gdf.columns.tolist())
print(gdf.head())
```

Common column names by source:

| Source | Typical column |
|---|---|
| FAO GAUL | `ADM2_NAME`, `ADM1_NAME` |
| GADM | `NAME_2`, `NAME_1` |
| Natural Earth | `name`, `NAME` |
| Custom | Varies -- check the attribute table |

Set `admin_field` to whatever column contains the names you want to filter by.

---

## Output schema reference

### `chirps_raw.csv`

| Column | Description |
|---|---|
| `system:index` | Unique row ID (date + feature ID) |
| `ADM0_CODE` / `ADM0_NAME` | Country code/name |
| `ADM1_CODE` / `ADM1_NAME` | Province/region code/name |
| `ADM2_CODE` / `ADM2_NAME` | District code/name |
| `mean` | Average rainfall (mm) for this district and pentad |
| `month` | Month number (1-12) |
| `pentad` | Pentad number within the month (1-6) |
| `year` | Year |
| `system:time_start` | Unix timestamp (ms) of the pentad start |

### `admin_raw.csv`

| Column | Description |
|---|---|
| `district` | District name |
| `gid` | District code (used as join key in the Sliders app) |
| `chirps_early_first` | First dekad of the early rainy season |
| `chirps_early_last` | Last dekad of the early rainy season |
| `chirps_late_first` | First dekad of the late rainy season |
| `chirps_late_last` | Last dekad of the late rainy season |

---

## Next steps: loading into the Sliders app

After generating the CSVs, convert them to Parquet and place them in the Sliders-2 app:

```python
import pandas as pd

df = pd.read_csv("output/chirps_raw.csv")
df.to_parquet("chirps_raw.parquet", index=False)

admin = pd.read_csv("output/admin_raw.csv")
admin.to_parquet("admin_raw.parquet", index=False)
```

Copy `chirps_raw.parquet` and `admin_raw.parquet` into the Sliders-2 static assets directory. The app will load them into DuckDB-WASM on page load and run the SQL model chain to power the dashboard.
