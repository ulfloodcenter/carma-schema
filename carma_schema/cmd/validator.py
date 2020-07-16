import sys
import argparse

from carma_schema import validate

def main():
    parser = argparse.ArgumentParser(description='Validate CARMA document.')
    parser.add_argument('-s', '--schema', help='Schema file to use for validation', required=True)
    parser.add_argument('-d', '--document', help='CARMA document to validate', required=True)
    args = parser.parse_args()

    (valid, result) = validate(args.schema, args.document)
    if not valid:
        sys.exit(f"Validation of {args.document} against schema {args.schema} failed: {result['error']}")
    else:
        print(f"Document {args.document} appears to validate to schema {args.schema}.")
