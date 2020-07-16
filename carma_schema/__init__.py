import json
import sys

import jsonschema

from carma_schema.util import find_duplicates


def validate(schema_path: str, document_path: str) -> (bool, dict):
    schema = None
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    document = None
    with open(document_path, 'r') as f:
        document = json.load(f)

    try:
        jsonschema.validate(document, schema)
        # import pdb; pdb.set_trace()

        # Get list of HUC-12 defined in HUC12Watersheds
        huc12_ids = [h['id'] for h in document['HUC12Watersheds']]
        duplicates = find_duplicates(huc12_ids)
        if len(duplicates):
            return False, {"error": f"Duplicate HUC12Watersheds encountered: {duplicates}"}
        huc12_ids = set(huc12_ids)

        # Get list of HUC-12 IDs from: GroundWaterAvailabilityDatasets,
        # SurfaceWaterAvailabilityDatasets, WaterUseDatasets
        # GroundWaterAvailabilityDatasets
        undef_huc12 = set()
        gwa_huc12s = [d['huc12'] for d in document['GroundWaterAvailabilityDatasets']]
        for g in gwa_huc12s:
            if not g in huc12_ids:
                undef_huc12.add(g)
        if len(undef_huc12):
            return False, {"error", f"Undefined HUC12s encountered in GroundWaterAvailabilityDatasets: {undef_huc12}"}

        return True, {}
    except jsonschema.exceptions.SchemaError as e:
        return False, {"error": e}
    except jsonschema.exceptions.ValidationError as e:
        return False, {"error": e}
