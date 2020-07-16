from collections import Counter


def find_duplicates(lst: list) -> set:
    c = Counter()
    for l in lst:
        c[l] += 1
    dupes = set()
    for k in c:
        if c[k] > 1:
            dupes.add(k)
    return dupes
