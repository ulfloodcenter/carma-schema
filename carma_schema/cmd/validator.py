# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse

from carma_schema import validate


def main():
    parser = argparse.ArgumentParser(description='Validate CARMA document.')
    parser.add_argument('-s', '--schema', help='Schema file to use for validation', required=True)
    parser.add_argument('-d', '--document', help='CARMA document to validate', required=True)
    args = parser.parse_args()

    (valid, result) = validate(args.schema, args.document)
    if not valid:
        print(f"Validation of {args.document} against schema {args.schema} failed due to the following errors: ")
        for e in result['errors']:
            print(f"Path: {e['path']}, error: {e['message']}")
    else:
        print(f"Document {args.document} appears to validate to schema {args.schema}.")
