import json
from collections import Counter
from typing import List
from uuid import UUID
from dataclasses import asdict

import jsonschema

from carma_schema.types import CropData, DevelopedArea, GroundwaterWell, AnalysisWaSSI, WaterUseDataset


DEFINITION_TYPES = [
    'HUC12Watersheds',
    'Counties',
    'SubHUC12Watersheds',
    'Analyses'
]

DATASET_TYPES = [
    'PowerPlantDatasets',
    'WaterUseDatasets'
]


def get_huc12_ids(document: dict) -> List[str]:
    huc12_list = []
    if 'HUC12Watersheds' in document:
        huc12_list = [h['id'] for h in document['HUC12Watersheds']]
    return huc12_list


def get_county_ids(document: dict) -> List[str]:
    county_list = []
    if 'Counties' in document:
        county_list = [h['id'] for h in document['Counties']]
    return county_list


def get_water_use_data_for_county(document: dict, county: str, year: int) -> List[WaterUseDataset]:
    wu_datasets = []
    if 'WaterUseDatasets' in document:
        for wud in document['WaterUseDatasets']:
            if 'county' in wud:
                if wud['county'] == county and wud['year'] == year:
                    d = WaterUseDataset(wud['entityType'],
                                        wud['waterSource'],
                                        wud['waterType'],
                                        wud['sector'],
                                        wud['description'],
                                        wud['sourceData'],
                                        year,
                                        wud['value'],
                                        wud['unit'],
                                        county=county)
                    wu_datasets.append(d)
    return wu_datasets


def get_crop_data_for_entity(entity: dict, year: int) -> CropData:
    crop_data = None
    for crop in entity['crops']:
        if crop['year'] == year:
            crop_data = CropData(year, crop['cropArea'], crop['cropAreaDetail'])
            break
    return crop_data


def get_developed_area_data_for_entity(entity: dict, year: int) -> DevelopedArea:
    developed_area = None
    for da in entity['developedArea']:
        if da['year'] == year:
            developed_area = DevelopedArea(year, da['area'])
            break
    return developed_area


def get_well_counts_for_entity(entity: dict, year_completed: int) -> List[GroundwaterWell]:
    well_counts = []
    for wc in entity['groundwaterWells']:
        if wc['yearCompleted'] == year_completed:
            well_counts.append(GroundwaterWell(wc['sector'],
                                               wc['status'],
                                               year_completed,
                                               wc['count']))
    return well_counts


def get_wassi_analysis_by_id(document: dict, id: UUID) -> AnalysisWaSSI:
    if 'Analyses' in document:
        for a in document['Analyses']:
            if 'WaSSI' in a:
                for w in a['WaSSI']:
                    if w['id'] == str(id):
                        return AnalysisWaSSI.from_dict(w)
    return None


def update_wassi_analysis_instance(document: dict, wassi: AnalysisWaSSI) -> bool:
    if 'Analyses' in document:
        for a in document['Analyses']:
            if 'WaSSI' in a:
                for w in a['WaSSI']:
                    if w['id'] == str(wassi.id):
                        w['cropYear'] = wassi.cropYear
                        w['developedAreaYear'] = wassi.developedAreaYear
                        w['description'] = wassi.description
                        w['countyDisaggregations'] = asdict(wassi)['countyDisaggregations']
                        return True
    return False


def _error_factory(path: str, message: str) -> dict:
    return {'path': path, 'message': message}


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
        errors.append(_error_factory('/' + '/'.join([str(elem) for elem in e.absolute_path]),
                                     e.message))

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
            errors.append(_error_factory('/HUC12Watersheds',
                                         f"Duplicate HUC12 watershed definitions found for: {duplicate_huc12s}")
                          )
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
            errors.append(_error_factory('/Counties',
                                         f"Duplicate county definitions found for: {duplicate_counties}")
                          )
        county_ids = set(county_list)

    if not (huc12_present or counties_present):
        errors.append(_error_factory('/',
                                     (f"Neither HUC12Watersheds nor Counties encountered in document {document_path}, "
                                     "when at least one must be present"))
                      )

    # Make sure that HUC-12s and county ID references from WaterUseDatasets are actually defined.
    for dataset_type in DATASET_TYPES:
        # Validate HUC-12 IDs
        undef_huc12 = set()
        undef_county = set()
        if dataset_type in document:
            for d in document[dataset_type]:
                if 'huc12' in d:
                    huc = d['huc12']
                    if huc not in huc12_ids:
                        undef_huc12.add(huc)
                if 'county' in d:
                    county = d['county']
                    if county not in county_ids:
                        undef_county.add(county)

            if len(undef_huc12):
                errors.append(_error_factory('/' + dataset_type,
                                             f"Undefined HUC12s encountered in {dataset_type}: {undef_huc12}")
                              )
            if len(undef_county):
                errors.append(_error_factory('/' + dataset_type,
                                             f"Undefined counties encountered in {dataset_type}: {undef_county}")
                              )

    if len(errors) > 0:
        return False, {'errors': errors, 'document': document}
    else:
        return True, {'document': document}
