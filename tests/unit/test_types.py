import unittest
from dataclasses import asdict
import json

from carma_schema.types import AnalysisWaSSI, SurfaceWeightsWaSSI


class TestTypes(unittest.TestCase):
    def test_analysis_wassi(self):
        wassi1 = AnalysisWaSSI("fakehuc12", "county fake", 2019, 2016,
                               SurfaceWeightsWaSSI(1.2, 3.4, 5.6, 7.8))
        wassi1_dict = asdict(wassi1)
        self.assertEqual("fakehuc12", wassi1_dict['huc12'])
        self.assertEqual("county fake", wassi1_dict['county'])
        self.assertEqual(2019, wassi1_dict['cropYear'])
        self.assertEqual(2016, wassi1_dict['developedAreaYear'])
        w = wassi1_dict['surfaceWeights']
        self.assertTrue(isinstance(w, dict))
        self.assertEqual(1.2, w['w1'])
        self.assertEqual(3.4, w['w2'])
        self.assertEqual(5.6, w['w3'])
        self.assertEqual(7.8, w['w4'])
        keys = [k for k in w]
        self.assertTrue('w1', keys[0])
        self.assertTrue('w2', keys[1])
        self.assertTrue('w3', keys[2])
        self.assertTrue('w4', keys[3])

        wassi1_json = json.dumps(wassi1_dict, separators=(',', ':'))
        self.assertEqual('{"huc12":"fakehuc12","county":"county fake","cropYear":2019,"developedAreaYear":2016,"surfaceWeights":{"w1":1.2,"w2":3.4,"w3":5.6,"w4":7.8}}',
                         wassi1_json)
