# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

from collections import Counter


def get_sub_huc12_id(sub_huc12: dict) -> str:
    return f"{sub_huc12['huc12']}:{sub_huc12['county']}"


def find_duplicates(lst: list) -> set:
    c = Counter()
    for l in lst:
        c[l] += 1
    dupes = set()
    for k in c:
        if c[k] > 1:
            dupes.add(k)
    return dupes
