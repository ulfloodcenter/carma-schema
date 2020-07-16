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

Broken/invalid root structure of CARMA document:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d test/fixtures/sample_carma_data_3_missingHuc12.json 
Validation of test/fixtures/sample_carma_data_3_missingHuc12.json against schema schema/CARMA-schema-20200709.json failed: 'HUC12Watersheds' is a required property
```

Missing geometry field from HUC12Watersheds instance:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d test/fixtures/sample_carma_data_2_missingGeom.json
Validation of test/fixtures/sample_carma_data_2_missingGeom.json against schema schema/CARMA-schema-20200709.json failed: 'geometry' is a required property
```

Valid HUC12Watersheds instance:
```
$ carma-validator -s schema/CARMA-schema-20200709.json -d test/fixtures/Document test/fixtures/sample_carma_data_1.json appears to validate to schema schema/CARMA-schema-20200709.json.
```

> i.e. no output=valid according to schema.
