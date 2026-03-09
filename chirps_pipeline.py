"""
CHIRPS Data Pipeline for DESDR
==============================

This script automates the process of downloading CHIRPS rainfall data from Google Earth Engine
and formatting it for use in the DESDR Sliders platform.

It replaces the manual two-step process:
1. JavaScript script in Google Earth Engine (downloads pentad data)
2. R script (converts pentads to dekads and formats)

GEE Setup (one-time):
    1. Install dependencies:
         pip3 install -r requirements.txt

    2. Authenticate with Google Earth Engine:
         python3 -c "import ee; ee.Authenticate()"
       This opens a browser window. Sign in with your Google account and authorize access.
       On success it prints "Successfully saved authorization token."

    3. Register your GCP project for Earth Engine (if not already done):
       - Go to: https://console.cloud.google.com/earth-engine/configuration?project=YOUR_PROJECT_ID
       - Register for noncommercial/research use.
       - Then go to: https://console.developers.google.com/apis/api/earthengine.googleapis.com/overview?project=YOUR_PROJECT_ID
       - Click "Enable" to turn on the Earth Engine API.

    4. Update the project ID in initialize_earth_engine() below (currently set to 'desdr-testing-project').

    Note: If you hit an SSL certificate error on macOS, run:
         /Applications/Python\ 3.13/Install\ Certificates.command
    (Replace 3.13 with your Python version.)

Usage:
    # Recommended: provide a JSON config file (see chirps_config.example.json)
    python3 chirps_pipeline.py --config my_config.json

    # CLI-only: use GEE boundaries (no shapefile needed)
    python3 chirps_pipeline.py --use-gee-boundaries --country-name "Kenya" --admin-level 2 --admin-names "Nairobi,Mombasa"

    # CLI-only: use a local shapefile
    python3 chirps_pipeline.py --shapefile path/to/boundaries.shp --admin-field ADM2_NAME --admin-names "Area1,Area2"

    # Mix config file with CLI overrides (CLI wins)
    python3 chirps_pipeline.py --config my_config.json --output-dir ./custom_output

Output:
    - chirps_raw.csv  : Pentad rainfall data with full DESDR schema (system:index, ADM0-2, mean, etc.)
    - admin_raw.csv   : Admin area defaults with dekad season ranges
"""

import ee
import pandas as pd
import geopandas as gpd
import argparse
import os
import json
from pathlib import Path
from typing import List, Optional, Tuple
from shapely.geometry import shape


def load_config(config_path: str) -> dict:
    """
    Load pipeline configuration from a JSON file.

    The config file provides all parameters without editing the script.
    See chirps_config.example.json for the expected structure.

    Any CLI arguments provided alongside --config will override the
    corresponding config file values.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw = json.load(f)

    source = raw.get("source", {})
    filt = raw.get("filter", {})
    date_range = raw.get("date_range", {})
    season = raw.get("season", {})

    return {
        "shapefile": source.get("shapefile"),
        "use_gee_boundaries": source.get("use_gee_boundaries", False),
        "country_name": source.get("country_name"),
        "admin_level": source.get("admin_level", 2),
        "admin_field": filt.get("admin_field", "ADM2_NAME"),
        "admin_names": filt.get("admin_names"),
        "start_date": date_range.get("start_date"),
        "end_date": date_range.get("end_date"),
        "early_first": season.get("early_first", 31),
        "early_last": season.get("early_last", 39),
        "late_first": season.get("late_first", 40),
        "late_last": season.get("late_last", 48),
        "output_dir": raw.get("output_dir", "./output"),
    }


def initialize_earth_engine():
    """
    Initialize Google Earth Engine.
    Requires authentication - run 'earthengine authenticate' first if not already done.
    """
    try:
        ee.Initialize(project='desdr-testing-project')
        print("✓ Google Earth Engine initialized successfully")
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        print("\nTo authenticate, run: earthengine authenticate")
        raise


def load_admin_boundaries_from_gee(
    country_name: str,
    admin_level: int = 2,
    admin_names: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Load admin boundaries directly from Google Earth Engine (GAUL dataset).
    
    This matches the approach in the paper - using GEE's built-in admin boundaries
    instead of requiring a local shapefile.
    
    Args:
        country_name: Country name (e.g., "Madagascar")
        admin_level: Administrative level (0=country, 1=province, 2=district)
        admin_names: Optional list of specific admin area names to filter
    
    Returns:
        GeoDataFrame with admin boundaries and attributes
    """
    print(f"\n📥 Loading admin boundaries from Google Earth Engine...")
    print(f"   Country: {country_name}")
    print(f"   Admin level: {admin_level}")
    
    # Load GAUL dataset from Earth Engine
    # GAUL has levels: level0 (country), level1 (province), level2 (district)
    gaul_dataset = f"FAO/GAUL_SIMPLIFIED_500m/2015/level{admin_level}"
    
    print(f"   Loading dataset: {gaul_dataset}")
    gaul = ee.FeatureCollection(gaul_dataset)
    
    # Filter to country
    country_filtered = gaul.filter(ee.Filter.eq('ADM0_NAME', country_name))
    
    # Get count
    count = country_filtered.size().getInfo()
    print(f"   Found {count} admin areas in {country_name}")
    
    if count == 0:
        raise ValueError(f"No admin areas found for country: {country_name}")
    
    # Filter to specific admin names if provided
    if admin_names:
        admin_field = f'ADM{admin_level}_NAME'
        country_filtered = country_filtered.filter(
            ee.Filter.inList(admin_field, admin_names)
        )
        filtered_count = country_filtered.size().getInfo()
        print(f"   Filtered to {filtered_count} specified areas: {admin_names}")
    
    # Download to Python
    print("   Downloading boundaries from Earth Engine...")
    features_list = country_filtered.getInfo()['features']
    
    # Convert to GeoDataFrame
    data_records = []
    for feature in features_list:
        props = feature['properties']
        geom = feature.get('geometry')
        
        record = dict(props)
        if geom:
            record['geometry'] = geom
        
        data_records.append(record)
    
    # Create GeoDataFrame
    geometries = []
    properties = []
    
    for record in data_records:
        if 'geometry' in record:
            geom = record.pop('geometry')
            geometries.append(shape(geom))
            properties.append(record)
    
    gdf = gpd.GeoDataFrame(properties, geometry=geometries, crs='EPSG:4326')
    
    print(f"   ✓ Loaded {len(gdf)} admin boundaries")
    
    return gdf


def download_chirps_data(
    shapefile_path: Optional[str] = None,
    country_name: Optional[str] = None,
    admin_level: int = 2,
    admin_field: str = "ADM2_NAME",
    admin_names: Optional[List[str]] = None,
    country_filter: Optional[str] = None,
    use_gee_boundaries: bool = False,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Download CHIRPS pentad (5-day) data from Google Earth Engine.
    
    This function replicates the JavaScript Earth Engine script functionality:
    - Loads CHIRPS PENTAD dataset
    - Filters to specified admin areas (from shapefile OR GEE)
    - Calculates spatial average rainfall for each area
    - Returns as pandas DataFrame
    
    Args:
        shapefile_path: Path to shapefile (optional if use_gee_boundaries=True)
        country_name: Country name for GEE boundaries (required if use_gee_boundaries=True)
        admin_level: Admin level for GEE (0=country, 1=province, 2=district)
        admin_field: Field name in shapefile that contains admin area names (default: "ADM2_NAME")
        admin_names: Optional list of specific admin area names to filter
        country_filter: Optional country name to filter (deprecated, use country_name)
        use_gee_boundaries: If True, load boundaries from GEE instead of shapefile
    
    Returns:
        DataFrame with columns: [admin_field, admin_code_field, 'system:time_start', 'mean', 'id']
    """
    # Load admin boundaries
    if use_gee_boundaries:
        if not country_name:
            raise ValueError("country_name is required when use_gee_boundaries=True")
        print(f"\n Step 1: Loading admin boundaries from Google Earth Engine")
        gdf = load_admin_boundaries_from_gee(
            country_name=country_name,
            admin_level=admin_level,
            admin_names=admin_names
        )
        # Set admin field based on level
        admin_field = f'ADM{admin_level}_NAME'
        admin_code_field = f'ADM{admin_level}_CODE'
    else:
        if not shapefile_path:
            raise ValueError("shapefile_path is required when use_gee_boundaries=False")
        print(f"\n📥 Step 1: Loading shapefile from {shapefile_path}")
        
        # Load shapefile using geopandas
        gdf = gpd.read_file(shapefile_path)
        print(f"   Found {len(gdf)} features in shapefile")
    
        # Filter by country if specified (for shapefile mode)
        if country_filter:
            country_field = "ADM0_NAME"  # Assuming country is in this field
            if country_field in gdf.columns:
                gdf = gdf[gdf[country_field] == country_filter]
                print(f"   Filtered to {len(gdf)} features in {country_filter}")
        
        # Filter by specific admin names if provided (for shapefile mode)
        if admin_names:
            if admin_field not in gdf.columns:
                raise ValueError(f"Field '{admin_field}' not found in shapefile. Available fields: {list(gdf.columns)}")
            
            gdf = gdf[gdf[admin_field].isin(admin_names)]
            print(f"   Filtered to {len(gdf)} specified admin areas: {admin_names}")
        
        if len(gdf) == 0:
            raise ValueError("No features found after filtering. Check your filters.")
        
        # Find the admin code field (typically ADM2_CODE or similar)
        admin_code_field = None
        for code_field in ["ADM2_CODE", "ADM1_CODE", "ADM0_CODE", "GID", "gid"]:
            if code_field in gdf.columns:
                admin_code_field = code_field
                break
        
        if admin_code_field is None:
            # Try to find any field with 'code' or 'id' in the name
            code_fields = [col for col in gdf.columns if 'code' in col.lower() or 'id' in col.lower()]
            if code_fields:
                admin_code_field = code_fields[0]
                print(f"   Using '{admin_code_field}' as admin code field")
            else:
                raise ValueError("Could not find admin code field. Please specify manually.")
        
        print(f"   Using admin field: {admin_field}")
        print(f"   Using admin code field: {admin_code_field}")
    
    # Convert GeoDataFrame to Earth Engine FeatureCollection
    print("\n Step 2: Converting shapefile to Earth Engine format...")
    
    # Ensure CRS is WGS84 for Earth Engine
    if gdf.crs != 'EPSG:4326':
        print(f"   Converting CRS from {gdf.crs} to EPSG:4326 (WGS84)")
        gdf = gdf.to_crs('EPSG:4326')
    
    # Calculate shape area and length if not present (for DESDR format)
    if 'Shape_Area' not in gdf.columns:
        print("   Calculating Shape_Area and Shape_Leng...")
        gdf['Shape_Area'] = gdf.geometry.area
        gdf['Shape_Leng'] = gdf.geometry.length
    
    # Ensure admin level fields exist (for DESDR format)
    admin_level_fields = {
        'ADM0_CODE': ['ADM0_CODE', 'GID_0', 'ISO_A3'],
        'ADM0_NAME': ['ADM0_NAME', 'NAME_0', 'COUNTRY'],
        'ADM1_CODE': ['ADM1_CODE', 'GID_1', 'ADMIN1_CODE'],
        'ADM1_NAME': ['ADM1_NAME', 'NAME_1', 'ADMIN1'],
        'ADM2_CODE': [admin_code_field, 'ADM2_CODE', 'GID_2'],
        'ADM2_NAME': [admin_field, 'ADM2_NAME', 'NAME_2']
    }
    
    for target_field, possible_fields in admin_level_fields.items():
        if target_field not in gdf.columns:
            for possible in possible_fields:
                if possible in gdf.columns:
                    gdf[target_field] = gdf[possible]
                    break
            # If still not found, use default
            if target_field not in gdf.columns:
                if 'CODE' in target_field:
                    gdf[target_field] = 0
                else:
                    gdf[target_field] = ''
    
    # Add default fields if missing
    if 'DISP_AREA' not in gdf.columns:
        gdf['DISP_AREA'] = 'NO'
    if 'EXP2_YEAR' not in gdf.columns:
        gdf['EXP2_YEAR'] = 3000
    if 'STATUS' not in gdf.columns:
        gdf['STATUS'] = 'Member State'
    if 'STR2_YEAR' not in gdf.columns:
        gdf['STR2_YEAR'] = 2007
    
    geojson = gdf.to_json()
    ee_features = ee.FeatureCollection(json.loads(geojson))
    
    print(f"   Created FeatureCollection with {ee_features.size().getInfo()} features")
    print(f"   Preserved admin fields: ADM0, ADM1, ADM2")
    
    # Load CHIRPS dataset
    print("\n Step 3: Loading CHIRPS PENTAD dataset from Earth Engine...")
    dataset = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD").select('precipitation')
    
    # Apply date filter if provided
    if start_date:
        dataset = dataset.filterDate(start_date, end_date or '2099-12-31')
        print(f"   Date filter: {start_date} to {end_date or 'present'}")
    
    # Get date range info
    first_image = ee.Image(dataset.first())
    last_image = ee.Image(dataset.sort('system:time_start', False).first())
    
    actual_start = ee.Date(first_image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
    actual_end = ee.Date(last_image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
    image_count = dataset.size().getInfo()
    
    print(f"   CHIRPS data range: {actual_start} to {actual_end} ({image_count} images)")
    
    # Calculate areal mean for each feature and each image
    print("\n Step 4: Calculating spatial averages (this may take several minutes)...")
    
    def calculate_areal_mean(image):
        """Calculate mean precipitation for each feature in the collection."""
        # Get image date for system:index
        image_date = ee.Date(image.get('system:time_start'))
        
        reduced = image.reduceRegions(
            collection=ee_features,
            reducer=ee.Reducer.mean(),
            scale=10000  # 10km scale as in original script
        )
        
        # Process each feature to add image properties and preserve all admin fields
        def process_feature(feature):
            # Create system:index from date and feature id
            date_str = image_date.format('YYYYMMdd')
            feature_id = feature.id()
            system_index = ee.String(date_str).cat('_').cat(feature_id)
            
            # Preserve all original properties and add image properties
            return feature.setGeometry(None)\
                .copyProperties(image, ['system:time_start'])\
                .set('id', feature_id)\
                .set('system:index', system_index)\
                .set('mean', feature.get('mean'))
        
        return reduced.map(process_feature)
    
    # Map over all images
    areal_means = dataset.map(calculate_areal_mean)
    
    # Flatten the collection
    final_collection = areal_means.flatten()
    
    # Check collection size to decide download method
    print("\n Checking data size...")
    try:
        collection_size = final_collection.size().getInfo()
        print(f"   Total records: {collection_size:,}")
        
        # Estimate size (rough: ~1.5KB per feature)
        estimated_size_mb = (collection_size * 1.5) / 1024
        print(f"   Estimated size: ~{estimated_size_mb:.1f} MB")
        
        # Use export method for large datasets (>50MB to be safe)
        if estimated_size_mb > 50:
            print("   ⚠️  Dataset is large - using export method (more reliable)")
            print("   Note: This will export to Google Drive - you'll need to download manually")
            print("   See GEE_DOWNLOAD_GUIDE.md for instructions")
            df = _download_via_export(final_collection, admin_field, admin_code_field)
        else:
            print("   ✓ Dataset size OK - using direct download")
            df = _download_via_getinfo(final_collection, admin_field, admin_code_field)
            
    except Exception as e:
        print(f"   ⚠️  Could not estimate size: {e}")
        print("   Attempting direct download (may fail for large datasets)...")
        df = _download_via_getinfo(final_collection, admin_field, admin_code_field)
    
    print(f"   ✓ Downloaded {len(df)} records")
    if len(df) > 0:
        print(f"   ✓ Date range: {df['system:time_start'].min()} to {df['system:time_start'].max()}")
    
    return df, admin_field, admin_code_field


def _download_via_getinfo(collection, admin_field, admin_code_field):
    """
    Download data using .getInfo() - works for small datasets.
    
    This method directly downloads data from Earth Engine to Python.
    Limited to ~10MB responses.
    
    Preserves all columns from Earth Engine export to match DESDR format.
    """
    print("   Downloading data directly from Earth Engine...")
    print("   (This may take a few minutes)")
    
    try:
        # Get all features as a list
        features_list = collection.getInfo()['features']
        
        # Convert to list of dictionaries - preserve ALL properties
        data_records = []
        for feature in features_list:
            props = feature['properties']
            
            # Create record with all properties (preserve full format)
            record = dict(props)  # Start with all properties
            
            # Ensure key fields exist
            if 'system:time_start' not in record:
                record['system:time_start'] = props.get('system:time_start')
            if 'mean' not in record:
                record['mean'] = props.get('mean')
            if 'id' not in record:
                record['id'] = props.get('id')
            
            # Add geometry if present (as GeoJSON string)
            if 'geometry' in feature:
                import json
                record['.geo'] = json.dumps(feature['geometry'])
            
            data_records.append(record)
        
        df = pd.DataFrame(data_records)
        
        # Ensure system:index is created if not present
        if 'system:index' not in df.columns and 'system:time_start' in df.columns:
            # Create system:index from date and id
            df['date_str'] = pd.to_datetime(df['system:time_start'], unit='ms').dt.strftime('%Y%m%d')
            df['id_str'] = df['id'].astype(str).str.zfill(24)  # Pad to 24 chars with zeros
            df['system:index'] = df['date_str'] + '_' + df['id_str']
            df = df.drop(columns=['date_str', 'id_str'])
        
        return df
        
    except Exception as e:
        error_msg = str(e)
        if 'size' in error_msg.lower() or 'too large' in error_msg.lower():
            print(f"\n   ❌ Error: Dataset too large for direct download")
            print(f"   Error: {error_msg}")
            print(f"\n   💡 Solution: Use export method instead")
            print(f"   Run with --use-export flag or modify code to use export")
            raise ValueError(
                "Dataset too large for direct download. "
                "Please use export method (see GEE_API_EXPLAINED.md for details)"
            )
        else:
            raise


def _download_via_export(collection, admin_field, admin_code_field, drive_folder='CHIRPS'):
    """
    Download data using Earth Engine export to Google Drive.
    
    This method exports data to Google Drive, then you download it manually
    or programmatically. More reliable for large datasets.
    
    Note: This requires manual download from Drive, or you can use
    Google Drive API to automate the download step.
    """
    import time
    from datetime import datetime
    
    print("   Exporting data to Google Drive...")
    print("   (This will take 10-30 minutes depending on data size)")
    
    # Create export task
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task = ee.batch.Export.table.toDrive(
        collection=collection,
        description=f'chirps_export_{timestamp}',
        folder=drive_folder,
        fileNamePrefix=f'chirps_export_{timestamp}',
        fileFormat='CSV'
    )
    
    # Start the task
    task.start()
    print(f"   ✓ Export task started: {task.id}")
    print(f"   Task name: chirps_export_{timestamp}")
    
    # Monitor task status
    print("\n   Monitoring export progress...")
    print("   (You can check status in Earth Engine Code Editor: https://code.earthengine.google.com/)")
    
    max_wait_time = 3600  # 1 hour max wait
    start_time = time.time()
    check_interval = 30  # Check every 30 seconds
    
    while task.active() and (time.time() - start_time) < max_wait_time:
        status = task.status()
        state = status.get('state', 'UNKNOWN')
        
        if state == 'RUNNING':
            print(f"   ⏳ Status: {state} (elapsed: {int(time.time() - start_time)}s)")
        elif state == 'READY':
            print(f"   ✓ Status: {state} - Export complete!")
            break
        elif state in ['FAILED', 'CANCELLED']:
            error = status.get('error_message', 'Unknown error')
            raise RuntimeError(f"Export failed: {error}")
        
        time.sleep(check_interval)
    
    if task.active():
        print(f"\n   ⚠️  Export still running after {max_wait_time}s")
        print(f"   Task ID: {task.id}")
        print(f"   Check status: https://code.earthengine.google.com/")
        print(f"   File will be in Google Drive folder: {drive_folder}")
        raise TimeoutError(
            "Export taking longer than expected. "
            f"Check Google Drive folder '{drive_folder}' for the file when complete."
        )
    
    # Get final status
    final_status = task.status()
    if final_status['state'] == 'COMPLETED':
        print(f"\n   ✅ Export completed successfully!")
        print(f"   📁 File location: Google Drive → {drive_folder} → chirps_export_{timestamp}.csv")
        print(f"\n   Next steps:")
        print(f"   1. Go to https://drive.google.com")
        print(f"   2. Navigate to folder: {drive_folder}")
        print(f"   3. Download: chirps_export_{timestamp}.csv")
        print(f"   4. Load it: df = pd.read_csv('chirps_export_{timestamp}.csv')")
        print(f"\n   Or use Google Drive API to download programmatically")
        
        # Return empty DataFrame with note
        return pd.DataFrame({
            'note': ['Data exported to Google Drive - download manually']
        })
    else:
        raise RuntimeError(f"Export did not complete: {final_status}")


def format_output_dataframe(df: pd.DataFrame, admin_field: str, admin_code_field: str, preserve_full_format: bool = True) -> pd.DataFrame:
    """
    Format the downloaded data to match DESDR output format.
    
    If preserve_full_format=True, keeps all columns from Earth Engine export.
    If False, converts to simplified dekadal format.
    """
    if preserve_full_format:
        # Add month and pentad columns if not present
        if 'system:time_start' in df.columns:
            df['date'] = pd.to_datetime(df['system:time_start'], unit='ms')
            if 'year' not in df.columns:
                df['year'] = df['date'].dt.year
            if 'month' not in df.columns:
                df['month'] = df['date'].dt.month.astype(float)
            
            # Calculate pentad from date (if not already present)
            if 'pentad' not in df.columns:
                # Pentad calculation: Pentads reset each month
                # Pentad = floor((day_of_month - 1) / 5) + 1
                day_of_month = df['date'].dt.day
                df['pentad'] = ((day_of_month - 1) // 5 + 1).astype(float)
        
        # Ensure all expected columns are present (fill with defaults if missing)
        expected_cols = [
            'system:index', 'ADM0_CODE', 'ADM0_NAME', 'ADM1_CODE', 'ADM1_NAME',
            'ADM2_CODE', 'ADM2_NAME', 'DISP_AREA', 'EXP2_YEAR', 'STATUS', 'STR2_YEAR',
            'Shape_Area', 'Shape_Leng', 'id', 'mean', 'month', 'pentad', 'year', '.geo'
        ]
        
        # Map admin fields to expected names
        field_mapping = {
            admin_field: 'ADM2_NAME',
            admin_code_field: 'ADM2_CODE'
        }
        
        # Rename fields if needed
        for old_name, new_name in field_mapping.items():
            if old_name in df.columns and new_name not in df.columns:
                df[new_name] = df[old_name]
        
        # Fill missing columns with defaults
        defaults = {
            'DISP_AREA': 'NO',
            'EXP2_YEAR': 3000,
            'STATUS': 'Member State',
            'STR2_YEAR': 2007,
            'Shape_Area': 0.0,
            'Shape_Leng': 0.0
        }
        
        for col, default_val in defaults.items():
            if col not in df.columns:
                df[col] = default_val
        
        # Reorder columns to match expected format
        available_cols = [col for col in expected_cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in expected_cols]
        df = df[available_cols + other_cols]
        
        return df
    else:
        # Use the original pentad_to_dekad function
        return pentad_to_dekad(df, admin_field, admin_code_field)


def pentad_to_dekad(df: pd.DataFrame, admin_field: str, admin_code_field: str) -> pd.DataFrame:
    """
    Convert CHIRPS pentad (5-day) data to dekad (10-day) data.
    
    This replicates the R script logic:
    - Groups pentads into dekads (2 pentads = 1 dekad)
    - Sums rainfall over each dekad
    - Extracts year from timestamp
    
    Args:
        df: DataFrame with pentad data (must have 'system:time_start' and 'mean' columns)
        admin_field: Name of the admin area name field
        admin_code_field: Name of the admin code field
    
    Returns:
        DataFrame with columns: [year, dekad, value, gid]
    """
    print("\n🔄 Step 5: Converting pentads to dekads...")
    
    # Convert timestamp to datetime
    df['date'] = pd.to_datetime(df['system:time_start'], unit='ms')
    df['year'] = df['date'].dt.year
    
    # Group by admin and year, then number all pentads sequentially
    df = df.sort_values([admin_field, 'year', 'date'])
    
    # Create pentad number within each admin-year group
    df['pentad_all'] = df.groupby([admin_field, 'year']).cumcount() + 1
    
    # Convert pentad to dekad (ceiling of pentad/2)
    df['dekad'] = (df['pentad_all'] / 2).apply(lambda x: int(x) if x == int(x) else int(x) + 1)
    
    # Group by admin code, year, and dekad, then sum the rainfall
    chirps_dekadal = df.groupby([admin_code_field, 'year', 'dekad']).agg({
        'mean': 'sum'
    }).reset_index()
    
    # Rename columns to match DESDR schema
    chirps_dekadal = chirps_dekadal.rename(columns={
        'mean': 'value',
        admin_code_field: 'gid'
    })
    
    # Select and reorder columns
    chirps_formatted = chirps_dekadal[['year', 'dekad', 'value', 'gid']].copy()
    
    print(f"   ✓ Converted to {len(chirps_formatted)} dekadal records")
    print(f"   ✓ Years: {chirps_formatted['year'].min()} to {chirps_formatted['year'].max()}")
    print(f"   ✓ Dekads: 1 to {chirps_formatted['dekad'].max()}")
    
    return chirps_formatted


def create_admin_defaults(
    df_original: pd.DataFrame,
    admin_field: str,
    admin_code_field: str,
    early_first: int = 31,
    early_last: int = 39,
    late_first: int = 40,
    late_last: int = 48
) -> pd.DataFrame:
    """
    Create admin defaults file with dekad ranges.
    
    This replicates the admin_raw.csv output from the R script.
    
    Args:
        df_original: Original DataFrame with admin information
        admin_field: Name of the admin area name field
        admin_code_field: Name of the admin code field
        early_first: First dekad of early season (default: 31)
        early_last: Last dekad of early season (default: 39)
        late_first: First dekad of late season (default: 40)
        late_last: Last dekad of late season (default: 48)
    
    Returns:
        DataFrame with columns: [district, gid, chirps_early_first, chirps_early_last, 
                                 chirps_late_first, chirps_late_last]
    """
    print("\n📋 Step 6: Creating admin defaults file...")
    
    # Get unique admin areas with their codes
    admin_defaults = df_original.groupby(admin_field).agg({
        admin_code_field: 'max'
    }).reset_index()
    
    # Rename columns
    admin_defaults = admin_defaults.rename(columns={
        admin_field: 'district',
        admin_code_field: 'gid'
    })
    
    # Add dekad range columns
    admin_defaults['chirps_early_first'] = early_first
    admin_defaults['chirps_early_last'] = early_last
    admin_defaults['chirps_late_first'] = late_first
    admin_defaults['chirps_late_last'] = late_last
    
    print(f"   ✓ Created defaults for {len(admin_defaults)} admin areas")
    
    return admin_defaults


def process_chirps_pipeline(
    shapefile_path: Optional[str] = None,
    country_name: Optional[str] = None,
    admin_level: int = 2,
    admin_field: str = "ADM2_NAME",
    admin_names: Optional[List[str]] = None,
    country_filter: Optional[str] = None,
    use_gee_boundaries: bool = False,
    output_dir: str = "./output",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    early_first: int = 31,
    early_last: int = 39,
    late_first: int = 40,
    late_last: int = 48
) -> Tuple[str, str]:
    """
    Main pipeline function that processes CHIRPS data from shapefile or GEE boundaries to formatted CSVs.
    
    Args:
        shapefile_path: Path to shapefile (optional if use_gee_boundaries=True)
        country_name: Country name for GEE boundaries (required if use_gee_boundaries=True)
        admin_level: Admin level for GEE (0=country, 1=province, 2=district)
        admin_field: Field name containing admin area names (for shapefile mode)
        admin_names: Optional list of specific admin areas to process
        country_filter: Optional country name filter (deprecated, use country_name)
        use_gee_boundaries: If True, load boundaries from GEE instead of shapefile
        output_dir: Directory to save output files
        early_first: First dekad of early season
        early_last: Last dekad of early season
        late_first: First dekad of late season
        late_last: Last dekad of late season
    
    Returns:
        Tuple of (chirps_csv_path, admin_csv_path)
    """
    # Initialize Earth Engine
    initialize_earth_engine()
    
    # Download CHIRPS data
    df_raw, admin_field_used, admin_code_field = download_chirps_data(
        shapefile_path=shapefile_path,
        country_name=country_name,
        admin_level=admin_level,
        admin_field=admin_field,
        admin_names=admin_names,
        country_filter=country_filter,
        use_gee_boundaries=use_gee_boundaries,
        start_date=start_date,
        end_date=end_date
    )
    
    # Format output (preserve full format by default)
    df_formatted = format_output_dataframe(df_raw, admin_field_used, admin_code_field, preserve_full_format=True)
    
    # Create admin defaults
    df_admin = create_admin_defaults(
        df_raw,
        admin_field_used,
        admin_code_field,
        early_first=early_first,
        early_last=early_last,
        late_first=late_first,
        late_last=late_last
    )
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save formatted CSVs
    chirps_path = os.path.join(output_dir, "chirps_raw.csv")
    admin_path = os.path.join(output_dir, "admin_raw.csv")
    
    print(f"\n💾 Step 7: Saving output files...")
    # Save with all columns preserved (matches Earth Engine export format)
    df_formatted.to_csv(chirps_path, index=False)
    print(f"   ✓ Saved: {chirps_path}")
    print(f"   Columns: {', '.join(df_formatted.columns[:5])}... ({len(df_formatted.columns)} total)")
    
    df_admin.to_csv(admin_path, index=False)
    print(f"   ✓ Saved: {admin_path}")
    
    print(f"\n✅ Pipeline complete! Output files saved to {output_dir}")
    
    return chirps_path, admin_path


def main():
    """Command-line interface for the CHIRPS pipeline."""
    parser = argparse.ArgumentParser(
        description="Download and format CHIRPS rainfall data for DESDR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use a JSON config file (recommended):
  python chirps_pipeline.py --config chirps_config.example.json

  # Use a local shapefile via CLI:
  python chirps_pipeline.py --shapefile boundaries.shp --admin-field ADM2_NAME

  # Use GEE boundaries via CLI:
  python chirps_pipeline.py --use-gee-boundaries --country-name "Kenya" --admin-level 2

  # Config file with CLI overrides (CLI takes precedence):
  python chirps_pipeline.py --config my_config.json --admin-names "Area1,Area2"
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to a JSON config file (see chirps_config.example.json). '
             'CLI arguments override config file values.'
    )

    parser.add_argument(
        '--shapefile',
        type=str,
        default=None,
        help='Path to shapefile containing admin boundaries'
    )

    parser.add_argument(
        '--use-gee-boundaries',
        action='store_true',
        default=None,
        help='Load admin boundaries from Google Earth Engine (GAUL dataset) instead of a shapefile'
    )

    parser.add_argument(
        '--country-name',
        type=str,
        default=None,
        help='Country name for GEE boundaries (required with --use-gee-boundaries)'
    )

    parser.add_argument(
        '--admin-level',
        type=int,
        default=None,
        help='Administrative level for GEE (0=country, 1=province, 2=district)'
    )

    parser.add_argument(
        '--admin-field',
        type=str,
        default=None,
        help='Column/field name in the shapefile that identifies sub-units (e.g. ADM2_NAME, NAME_2, GID)'
    )

    parser.add_argument(
        '--admin-names',
        type=str,
        default=None,
        help='Comma-separated list of sub-unit names to include (optional; omit to process all)'
    )

    parser.add_argument(
        '--country-filter',
        type=str,
        default=None,
        help='Country name to filter features by (useful when a shapefile spans multiple countries)'
    )

    parser.add_argument(
        '--start-date',
        type=str,
        default=None,
        help='Start date for CHIRPS data (YYYY-MM-DD). Defaults to all available data.'
    )

    parser.add_argument(
        '--end-date',
        type=str,
        default=None,
        help='End date for CHIRPS data (YYYY-MM-DD). Defaults to present.'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for CSV files (default: ./output)'
    )

    parser.add_argument(
        '--early-first', type=int, default=None,
        help='First dekad of early season (default: 31)'
    )
    parser.add_argument(
        '--early-last', type=int, default=None,
        help='Last dekad of early season (default: 39)'
    )
    parser.add_argument(
        '--late-first', type=int, default=None,
        help='First dekad of late season (default: 40)'
    )
    parser.add_argument(
        '--late-last', type=int, default=None,
        help='Last dekad of late season (default: 48)'
    )

    args = parser.parse_args()

    # -----------------------------------------------------------
    # Build effective params: config file defaults < CLI overrides
    # -----------------------------------------------------------
    defaults = {
        "shapefile": None,
        "use_gee_boundaries": False,
        "country_name": None,
        "admin_level": 2,
        "admin_field": "ADM2_NAME",
        "admin_names": None,
        "start_date": None,
        "end_date": None,
        "output_dir": "./output",
        "early_first": 31,
        "early_last": 39,
        "late_first": 40,
        "late_last": 48,
    }

    if args.config:
        cfg = load_config(args.config)
        defaults.update({k: v for k, v in cfg.items() if v is not None})

    def pick(cli_val, key):
        """Return CLI value if explicitly provided, otherwise the config/default."""
        return cli_val if cli_val is not None else defaults[key]

    shapefile      = pick(args.shapefile, "shapefile")
    use_gee        = pick(args.use_gee_boundaries, "use_gee_boundaries")
    country_name   = pick(args.country_name, "country_name")
    admin_level    = pick(args.admin_level, "admin_level")
    admin_field    = pick(args.admin_field, "admin_field")
    start_date     = pick(args.start_date, "start_date")
    end_date       = pick(args.end_date, "end_date")
    output_dir     = pick(args.output_dir, "output_dir")
    early_first    = pick(args.early_first, "early_first")
    early_last     = pick(args.early_last, "early_last")
    late_first     = pick(args.late_first, "late_first")
    late_last      = pick(args.late_last, "late_last")

    # admin_names: CLI is a comma-separated string; config is a list
    if args.admin_names is not None:
        admin_names = [n.strip() for n in args.admin_names.split(',')]
    else:
        admin_names = defaults["admin_names"]

    # Validate: user must supply either a shapefile or GEE boundaries
    if use_gee:
        if not country_name:
            parser.error(
                "--country-name (or source.country_name in config) is required "
                "when using GEE boundaries"
            )
    else:
        if not shapefile:
            parser.error(
                "Provide --shapefile (or source.shapefile in config), "
                "or use --use-gee-boundaries with --country-name"
            )

    # Run pipeline
    try:
        process_chirps_pipeline(
            shapefile_path=shapefile,
            country_name=country_name,
            admin_level=admin_level,
            admin_field=admin_field,
            admin_names=admin_names,
            country_filter=args.country_filter,
            use_gee_boundaries=use_gee,
            output_dir=output_dir,
            start_date=start_date,
            end_date=end_date,
            early_first=early_first,
            early_last=early_last,
            late_first=late_first,
            late_last=late_last
        )
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

