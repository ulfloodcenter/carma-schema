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
Validation of tests/fixtures/sample_carma_data_3_missingHuc12.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'HUC12Watersheds' is a required property">, <ValidationError: "'Counties' is a required property">]
```

### Missing geometry field from HUC12Watersheds and Counties instance:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_2_missingGeom.json
Validation of tests/fixtures/sample_carma_data_2_missingGeom.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'geometry' is a required property">, <ValidationError: "'geometry' is a required property">]
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

### Unknown UseType:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_invalidUseType.json
Validation of tests/fixtures/sample_carma_data_1_invalidUseType.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'GARBLE GARBLE Ground Water' is not one of ['Surface Water', 'Ground Water']">]
```

### Unknown Sector:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_invalidSector.json
Validation of tests/fixtures/sample_carma_data_1_invalidSector.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'GARBLE GARBLE Public Supply' is not one of ['Public Supply', 'Domestic', 'Commercial', 'Industrial', 'Total Thermoelectric Power', 'Fossil-fuel Thermoelectric Power', 'Geothermal Thermoelectric Power', 'Nuclear Thermoelectric Power', 'Thermoelectric Power (Once-through cooling)', 'Thermoelectric Power (Closed-loop cooling)', 'Mining', 'Livestock', 'Livestock (Stock)', 'Livestock (Animal Specialities)', 'Aquaculture', 'Irrigation, Total', 'Irrigation, Crop', 'Irrigation, Golf Courses', 'Hydroelectric Power', 'Wastewater Treatment']">]
```

### Missing Unit:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_missingUnit.json
Validation of tests/fixtures/sample_carma_data_1_missingUnit.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'unit' is a required property">]
```

### Invalid Unit:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_invalidUnit.json
Validation of tests/fixtures/sample_carma_data_1_invalidUnit.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "'GARBLE GARBLE Millimeter' is not one of ['Millimeter', 'Meter', 'Cubic meter', 'Hectare', 'Liter', 'Million liter', 'Kilogram', 'Kelvin', 'Second', 'Minute', 'Hour', 'Day', 'Year']">]
```

### Invalid Years:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_invalidYear.json
Validation of tests/fixtures/sample_carma_data_1_invalidYear.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: "2002.5 is not of type 'integer'">, <ValidationError: '-42 is less than the minimum of 1'>]
```

### Invalid Numbers:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1_invalidNumbers.json
Validation of tests/fixtures/sample_carma_data_1_invalidNumbers.json against schema schema/CARMA-schema-20200709.json failed due to the following errors: [<ValidationError: '-14270.41780358217 is less than the minimum of 1'>, <ValidationError: '-270.4358217801704 is less than the minimum of 0'>, <ValidationError: '0 is less than the minimum of 1'>, <ValidationError: '0 is less than the minimum of 1'>, <ValidationError: '-5 is less than the minimum of 1'>, <ValidationError: '-125 is less than the minimum of 0'>, <ValidationError: '-1 is less than the minimum of 1'>, <ValidationError: '-125 is less than the minimum of 0'>, <ValidationError: '-123.45 is less than the minimum of 0'>, <ValidationError: '-3029.587 is less than the minimum of 0'>, <ValidationError: '-20.6 is less than the minimum of 0'>]
```

### Valid:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d tests/fixtures/sample_carma_data_1.json
Document tests/fixtures/sample_carma_data_1.json appears to validate to schema schema/CARMA-schema-20200709.json.
```
