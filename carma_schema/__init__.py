import json
import sys

import jsonschema

def validate(schema_path: str, document_path: str) -> (bool, dict):
    schema = None
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    document = None
    with open(document_path, 'r') as f:
        document = json.load(f)

    try:
        jsonschema.validate(document, schema)
        return (True, {})
    except jsonschema.exceptions.SchemaError as e:
        return (False, {"error": e})
    except jsonschema.exceptions.ValidationError as e:
        return (False, {"error": e})
