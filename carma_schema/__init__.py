import json
from collections import Counter

import jsonschema

from carma_schema.util import find_duplicates


DATASET_TYPES = [
    'GroundWaterAvailabilityDatasets',
    'SurfaceWaterAvailabilityDatasets',
    'WaterUseDatasets',
    'GroundWaterAvailabilityDatasets'
]


def get_county_ids(document: dict) -> list[str]:
    county_list = []
    if 'Counties' in document:
        county_list = [h['id'] for h in document['Counties']]
    return county_list


def validate(schema_path: str, document_path: str) -> (bool, dict):
    schema = None
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    document = None
    with open(document_path, 'r') as f:
        document = json.load(f)

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for e in validator.iter_errors(document):
        errors.append(e)

    # Basic validation against schema failed, bail out before trying higher-order validation
    # (e.g. validating that HUC12 references are correct)
    if len(errors) > 0:
        return False, {'errors': errors}

    # Get set of HUC-12 defined in HUC12Watersheds (jsonschema and CARMA schema will make sure HUC12s are unique)
    if 'HUC12Watersheds' not in document:
        huc12_present = False
        huc12_ids = set()
    else:
        huc12_present = True
        huc12_ids_list = [h['id'] for h in document['HUC12Watersheds']]
        huc12_ids_counter = Counter(huc12_ids_list)
        duplicate_huc12s = []
        for id in huc12_ids_counter:
            if huc12_ids_counter[id] > 1:
                duplicate_huc12s.append(id)
        if len(duplicate_huc12s) > 0:
            errors.append(f"Duplicate HUC12 watershed definitions found for: {duplicate_huc12s}")
        huc12_ids = set(huc12_ids_list)

    if 'Counties' not in document:
        counties_present = False
        county_ids = set()
    else:
        counties_present = True
        county_list = [h['id'] for h in document['Counties']]
        county_counter = Counter(county_list)
        duplicate_counties = []
        for id in county_counter:
            if county_counter[id] > 1:
                duplicate_counties.append(id)
        if len(duplicate_counties) > 0:
            errors.append(f"Duplicate county definitions found for: {duplicate_counties}")
        county_ids = set(county_list)

    if not (huc12_present or counties_present):
        errors.append(f"Neither HUC12Watersheds nor Counties encountered in document {document_path}, "
                      "when at least one must be present")

    # Make sure that HUC-12s and county ID references from: GroundWaterAvailabilityDatasets,
    # SurfaceWaterAvailabilityDatasets, WaterUseDatasets
    # GroundWaterAvailabilityDatasets are actually defined.
    for dataset_type in DATASET_TYPES:
        # Validate HUC-12 IDs
        undef_huc12 = set()
        try:
            dataset_huc12s = [d['huc12'] for d in document[dataset_type]]
            for huc in dataset_huc12s:
                if huc not in huc12_ids:
                    undef_huc12.add(huc)
        except KeyError:
            pass
        if len(undef_huc12):
            errors.append(f"Undefined HUC12s encountered in {dataset_type}: {undef_huc12}")
        # Validate county IDs
        undef_county = set()
        try:
            dataset_counties = [d['county'] for d in document[dataset_type]]
            for county in dataset_counties:
                if county not in county_ids:
                    undef_county.add(county)
        except KeyError:
            pass
        if len(undef_county):
            errors.append(f"Undefined counties encountered in {dataset_type}: {undef_county}")

    if len(errors) > 0:
        return False, {'errors': errors, 'document': document}
    else:
        return True, {'document': document}
