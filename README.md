# JSON Schema and Python utilities for Coastal Aquifer Research and Management Analytics (CARMA) platform

## License
Copyright (C) 2021 University of Louisiana at Lafayette

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.

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
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210505.json -d tests/fixtures/sample_carma_data_3_missingHuc12.json
Validation of tests/fixtures/sample_carma_data_3_missingHuc12.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /, error: Neither HUC12Watersheds nor Counties encountered in document tests/fixtures/sample_carma_data_3_missingHuc12.json, when at least one must be present
```

### Missing geometry field from HUC12Watersheds and Counties instance:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_2_missingGeom.json
Validation of tests/fixtures/sample_carma_data_2_missingGeom.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /HUC12Watersheds/0, error: 'geometry' is a required property
Path: /Counties/0, error: 'geometry' is a required property
```

### Using undefined HUC-12s:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_unknown-huc12.json
Validation of tests/fixtures/sample_carma_data_1_unknown-huc12.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /PowerPlantDatasets, error: Undefined HUC12s encountered in PowerPlantDatasets: {'https://geoconnex.us/usgs/hydrologic-unit/080801030159'}
Path: /WaterUseDatasets, error: Undefined HUC12s encountered in WaterUseDatasets: {'https://geoconnex.us/usgs/hydrologic-unit/080801030190', 'https://geoconnex.us/usgs/hydrologic-unit/080801030350'}
```

### Duplicate counties
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_dupCounty.json
Validation of tests/fixtures/sample_carma_data_1_dupCounty.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /Counties, error: [{'id': 'https://geoconnex.us/ref/counties/22055', 'state': 'Louisiana', 'county': 'Lafayette', 'area': 697.23849898, 'maxStreamOrder': 3, 'minStreamLevel': 1, 'meanAnnualFlow': 34.747, 'population': [{'year': 2020, 'count': 221578}], 'crops': [{'year': 2019, 'cropArea': 34.37362276276971, 'cropAreaDetail': {'Corn': 12.395423572711515, 'Soybeans': 18.41814812247691, 'Mint': 0.0009886284553127704, 'Winter Wheat': 0.6465630097745517, 'Rye': 0.002965885365938311, 'Alfalfa': 1.6688048325679563, 'Other Hay/Non Alfalfa': 0.4725644016395042, 'Clover/Wildflowers': 0.004943142276563851, 'Fallow/Idle Cropland': 4.929301478189473, 'Open Water': 1.3059781894681695, 'Developed/Open Space': 5.306957548118951, 'Developed/Low Intensity': 2.5368206163325686, 'Developed/Med Intensity': 1.39890926426757, 'Developed/High Intensity': 0.22244140244537333, 'Barren': 0.0632722211400173, 'Deciduous Forest': 15.945588355739673, 'Evergreen Forest': 0.04053376666782358, 'Mixed Forest': 0.0365792528465725, 'Shrubland': 0.19772569106255405, 'Woody Wetlands': 4.639633340782831, 'Herbaceous Wetlands': 0.7632211675014586}}], 'developedArea': [{'year': 2016, 'area': 120.22441}], 'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[-90.56719273910849, 30.643084757618922], [-90.56719273911638, 30.64309475764262], [-90.56718674020803, 30.6444787609383], [-90.56717074348666, 30.648633770828162]]]]}}, {'id': 'https://geoconnex.us/ref/counties/22055', 'state': 'Louisiana', 'county': 'Lafayette', 'area': 697.23849898, 'maxStreamOrder': 3, 'minStreamLevel': 1, 'meanAnnualFlow': 34.747, 'population': [{'year': 2020, 'count': 221578}], 'crops': [{'year': 2019, 'cropArea': 34.37362276276971, 'cropAreaDetail': {'Corn': 12.395423572711515, 'Soybeans': 18.41814812247691, 'Mint': 0.0009886284553127704, 'Winter Wheat': 0.6465630097745517, 'Rye': 0.002965885365938311, 'Alfalfa': 1.6688048325679563, 'Other Hay/Non Alfalfa': 0.4725644016395042, 'Clover/Wildflowers': 0.004943142276563851, 'Fallow/Idle Cropland': 4.929301478189473, 'Open Water': 1.3059781894681695, 'Developed/Open Space': 5.306957548118951, 'Developed/Low Intensity': 2.5368206163325686, 'Developed/Med Intensity': 1.39890926426757, 'Developed/High Intensity': 0.22244140244537333, 'Barren': 0.0632722211400173, 'Deciduous Forest': 15.945588355739673, 'Evergreen Forest': 0.04053376666782358, 'Mixed Forest': 0.0365792528465725, 'Shrubland': 0.19772569106255405, 'Woody Wetlands': 4.639633340782831, 'Herbaceous Wetlands': 0.7632211675014586}}], 'developedArea': [{'year': 2016, 'area': 120.22441}], 'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[-90.56719273910849, 30.643084757618922], [-90.56719273911638, 30.64309475764262], [-90.56718674020803, 30.6444787609383], [-90.56717074348666, 30.648633770828162]]]]}}] has non-unique elements
```

### Duplicate HUC-12s:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_dupHUC12.json
Validation of tests/fixtures/sample_carma_data_1_dupHUC12.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /HUC12Watersheds, error: Duplicate HUC12 watershed definitions found for: ['https://geoconnex.us/usgs/hydrologic-unit/080801030109']
Path: /WaterUseDatasets, error: Undefined HUC12s encountered in WaterUseDatasets: {'https://geoconnex.us/usgs/hydrologic-unit/080801030305'}
```

### Unknown waterSource for WaterUseDataset:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_invalidWaterSource.json
Validation of tests/fixtures/sample_carma_data_1_invalidWaterSource.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /WaterUseDatasets/0/waterSource, error: 'GARBLE GARBLE Groundwater' is not one of ['Surface Water', 'Groundwater', 'Plant Discharge Water', 'All', 'Other', 'Not reported', 'N/A']
```

### Unknown Sector:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_invalidSector.json
Validation of tests/fixtures/sample_carma_data_1_invalidSector.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /WaterUseDatasets/0/sector, error: 'GARBLE GARBLE Public Supply' is not one of ['Public Supply', 'Domestic', 'Commercial', 'Industrial', 'Total Thermoelectric Power', 'Fossil-fuel Thermoelectric Power', 'Geothermal Thermoelectric Power', 'Nuclear Thermoelectric Power', 'Thermoelectric Power (Once-through cooling)', 'Thermoelectric Power (Closed-loop cooling)', 'Mining', 'Livestock', 'Livestock (Stock)', 'Livestock (Animal Specialties)', 'Aquaculture', 'Irrigation, Total', 'Irrigation, Crop', 'Irrigation, Golf Courses', 'Hydroelectric Power', 'Wastewater Treatment']
```

### Missing Unit:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_missingUnit.json
Validation of tests/fixtures/sample_carma_data_1_missingUnit.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /WaterUseDatasets/0, error: 'unit' is a required property
```

### Invalid Unit:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_invalidUnit.json
Validation of tests/fixtures/sample_carma_data_1_invalidUnit.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /WaterUseDatasets/0/unit/primaryDimension, error: 'Bagillion' is not one of ['One', 'Thousand', 'Million', 'Millimeter', 'Capita', 'Meter', 'Cubic meter', 'Acre', 'Hectare', 'Liter', 'Gallon', 'Kilogram', 'Kelvin', 'Gigawatt', 'Second', 'Minute', 'Hour', 'Day', 'Year']
```

### Invalid Years:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_invalidYear.json
Validation of tests/fixtures/sample_carma_data_1_invalidYear.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /WaterUseDatasets/0/year, error: 2015.5 is not of type 'integer'
Path: /WaterUseDatasets/1/year, error: -2015 is less than the minimum of 1
```

### Invalid Numbers:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1_invalidNumbers.json
Validation of tests/fixtures/sample_carma_data_1_invalidNumbers.json against schema carma_schema/data/schema/CARMA-schema-20210505.json failed due to the following errors:
Path: /Counties/1/developedArea/0/area, error: -456.22441334 is less than the minimum of 0
Path: /Counties/1/maxStreamOrder, error: -10 is less than the minimum of -9
```

### Valid:
```
$ carma-validator -s carma_schema/data/schema/CARMA-schema-20210908.json -d tests/fixtures/sample_carma_data_1.json
Document tests/fixtures/sample_carma_data_1.json appears to validate to schema schema/CARMA-schema-20210505.json.
```
