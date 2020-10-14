import json

import jsonschema

from carma_schema.util import find_duplicates


DATASET_TYPES = [
    'GroundWaterAvailabilityDatasets',
    'SurfaceWaterAvailabilityDatasets',
    'WaterUseDatasets',
    'GroundWaterAvailabilityDatasets'
]


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
    # (i.e. validating that HUC12 references are correct)
    if len(errors) > 0:
        return False, {'errors': errors}

    # Get set of HUC-12 defined in HUC12Watersheds (jsonschema and CARMA schema will make sure HUC12s are unique)
    huc12_ids = {h['id'] for h in document['HUC12Watersheds']}

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
        # TODO

    if len(errors) > 0:
        return False, {'errors': errors}
    else:
        return True, {}
