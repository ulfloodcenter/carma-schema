# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import unittest

from carma_schema.util import find_duplicates


class TestFindDuplicates(unittest.TestCase):
    def test_find_duplicates(self):
        # Test no duplicates cases
        no_dupes1 = [1, 2, 3]
        no_dupes2 = [1, 2]
        no_dupes3 = [1]
        no_dupes4 = []

        self.assertEqual(0, len(find_duplicates(no_dupes1)))
        self.assertEqual(0, len(find_duplicates(no_dupes2)))
        self.assertEqual(0, len(find_duplicates(no_dupes3)))
        self.assertEqual(0, len(find_duplicates(no_dupes4)))

        # Test duplicates cases
        dupes1 = [1, 1]
        dupes2 = [1, 2, 2, 3]
        dupes3 = [1, 1, 2, 2, 3, 3]


        self.assertEqual(1, len(find_duplicates(dupes1)))
        self.assertEqual(1, len(find_duplicates(dupes2)))
        self.assertEqual(3, len(find_duplicates(dupes3)))
