# Testing validity of CARMA data against CARMA-schema

## Installation

First setup a virtual environment:
- Using [venv](https://docs.python.org/3/library/venv.html)

HTTPS:
```
pip install git+https://bitbucket.org/watershedfloodcenter/carma-schema.git
```

> Note: You will need to enter your user ID and password

SSH:
```
pip install git+ssh://git@bitbucket.org/watershedfloodcenter/carma-schema.git
```

> Note: You will need to have [setup an SSH key](https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html) for this to work.

## Usage

### Broken/invalid root structure of CARMA document:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_3_missingHuc12.json
Validation of test/fixtures/sample_carma_data_3_missingHuc12.json against schema schema/CARMA-schema-20200709.json failed: 'HUC12Watersheds' is a required property
```

### Missing geometry field from HUC12Watersheds instance:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_2_missingGeom.json
Validation of test/fixtures/sample_carma_data_2_missingGeom.json against schema schema/CARMA-schema-20200709.json failed: 'geometry' is a required property
```

### Valid HUC12Watersheds instance:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1.json
Document tests/fixtures/sample_carma_data_1.json appears to validate to schema schema/CARMA-schema-20200709.json.
```

### Using undefined HUC-12:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_unknown-huc12.json
Validation of tests/fixtures/sample_carma_data_1_unknown-huc12.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: ["Undefined HUC12s encountered in GroundWaterAvailabilityDatasets: {'180801030109'}", "Undefined HUC12s encountered in SurfaceWaterAvailabilityDatasets: {'180801030305'}", "Undefined HUC12s encountered in WaterUseDatasets: {'180801030109', '180801030305'}", "Undefined HUC12s encountered in GroundWaterAvailabilityDatasets: {'180801030109'}"]
```

### Duplicate HUC-12s:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_dupHUC12.json
Validation of tests/fixtures/sample_carma_data_1_dupHUC12.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "[{'huc12': '080801030109', 'useType': {'name': 'Ground Water'}, 'sector': {'name': 'Public Supply'}, 'description': 'Water use by public water utilities', 'sourceData': 'https://waterdata.usgs.gov/la/nwis/water_use?format=rdb&rdb_compression=file&wu_area=County&wu_year=2015&wu_county=001&wu_category=PS&wu_county_nms=Acadia%2BParish&wu_category_nms=Public%2BSupply', 'year': 2015, 'value': 20.6, 'unit': {'name': 'million liter/day', 'primaryDimension': {'name': 'Million liter'}, 'secondaryDimension': {'name': 'Day'}}}, {'huc12': '080801030305', 'useType': {'name': 'Ground Water'}, 'sector': {'name': 'Public Supply'}, 'description': 'Water use by public water utilities', 'sourceData': 'https://waterdata.usgs.gov/la/nwis/water_use?format=rdb&rdb_compression=file&wu_area=County&wu_year=2015&wu_county=001&wu_category=PS&wu_county_nms=Acadia%2BParish&wu_category_nms=Public%2BSupply', 'year': 2015, 'value': 42.8, 'unit': {'name': 'million liter/day', 'primaryDimension': {'name': 'Million liter'}, 'secondaryDimension': {'name': 'Day'}}}, {'huc12': '080801030109', 'useType': {'name': 'Ground Water'}, 'sector': {'name': 'Public Supply'}, 'description': 'Water use by public water utilities', 'sourceData': 'https://waterdata.usgs.gov/la/nwis/water_use?format=rdb&rdb_compression=file&wu_area=County&wu_year=2015&wu_county=001&wu_category=PS&wu_county_nms=Acadia%2BParish&wu_category_nms=Public%2BSupply', 'year': 2015, 'value': 20.6, 'unit': {'name': 'million liter/day', 'primaryDimension': {'name': 'Million liter'}, 'secondaryDimension': {'name': 'Day'}}}] has non-unique elements">]
...
```
