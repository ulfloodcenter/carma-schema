# Testing validity of CARMA data against CARMA-schema

## Install [`jsonschema`](https://github.com/Julian/jsonschema)
```
pip install jsonschema
```

## Run tests from the command line

Broken/invalid root structure of document:
```
$ jsonschema -i test/fixtures/sample_carma_data_3_invalid.json src/schema/CARMA-schema-20200709.json 
{'id': '080801030109', 'description': 'Anselm Coulee-Vermilion River', 'area': 14270.41780358217, 'cropArea': 4270.21704054178, 'developedArea': 270.4358217801704, 'maxStreamOrder': 5, 'environmentalFlow': 105}: 'HUC12Watersheds' is a required property
```

Missing geometry field from HUC12Watersheds instance:
```
$ jsonschema -i test/fixtures/sample_carma_data_2_broken.json src/schema/CARMA-schema-20200709.json
{'id': '080801030109', 'description': 'Anselm Coulee-Vermilion River', 'area': 14270.41780358217, 'cropArea': 4270.21704054178, 'developedArea': 270.4358217801704, 'maxStreamOrder': 5, 'environmentalFlow': 105}: 'geometry' is a required property
```

Valid HUC12Watersheds instance:
```
$ jsonschema -i test/fixtures/sample_carma_data_1.json src/schema/CARMA-schema-20200709.json
```

> i.e. no output=valid according to schema.
