import unittest
from dataclasses import asdict
import uuid

from carma_schema.types import *


class TestTypes(unittest.TestCase):
    def test_analysis_wassi(self):
        id1 = uuid.uuid4()
        wassi1 = AnalysisWaSSI(id1, 2019, 2016, description="Test WaSSI analysis 1")
        wassi1_dict = asdict(wassi1)
        self.assertEqual(id1, wassi1_dict['id'])
        self.assertEqual(2019, wassi1_dict['cropYear'])
        self.assertEqual(2016, wassi1_dict['developedAreaYear'])
        self.assertEqual("Test WaSSI analysis 1", wassi1_dict['description'])
        self.assertIsNone(wassi1_dict['countyDisaggregations'])

        county_disagg1 = CountyDisaggregationWaSSI("fakehuc1", "fakecounty1",
                                                   SurfaceWeightsWaSSI(1.2, 3.4, 5.6, 7.8),
                                                   GroundwaterWeightsWaSSI(1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7))
        county_disagg2 = CountyDisaggregationWaSSI("fakehuc2", "fakecounty2",
                                                   SurfaceWeightsWaSSI(7.8, 5.6, 3.4, 1.2),
                                                   GroundwaterWeightsWaSSI(7.7, 6.6, 5.5, 4.4, 3.3, 2.2, 1.1))

        id2 = uuid.uuid4()
        wassi2 = AnalysisWaSSI(id2, 2019, 2016, description="Test WaSSI analysis 2",
                               countyDisaggregations=[county_disagg1, county_disagg2])
        wassi2_dict = asdict(wassi2)
        self.assertEqual(id2, wassi2_dict['id'])
        self.assertEqual(2019, wassi2_dict['cropYear'])
        self.assertEqual(2016, wassi2_dict['developedAreaYear'])
        self.assertEqual("Test WaSSI analysis 2", wassi2_dict['description'])
        self.assertTrue('countyDisaggregations' in wassi2_dict)

        cd1_dict = wassi2_dict['countyDisaggregations'][0]
        self.assertEqual("fakehuc1", cd1_dict['huc12'])
        self.assertEqual("fakecounty1", cd1_dict['county'])
        w1 = cd1_dict['surfaceWeights']
        self.assertTrue(isinstance(w1, dict))
        self.assertEqual(1.2, w1['w1'])
        self.assertEqual(3.4, w1['w2'])
        self.assertEqual(5.6, w1['w3'])
        self.assertEqual(7.8, w1['w4'])
        # Ensure order of keys in dict is as expected
        keys = [k for k in w1]
        self.assertTrue('w1', keys[0])
        self.assertTrue('w2', keys[1])
        self.assertTrue('w3', keys[2])
        self.assertTrue('w4', keys[3])
        gw1 = cd1_dict['groundwaterWeights']
        self.assertTrue(isinstance(gw1, dict))
        self.assertEqual(1.1, gw1['publicSupply'])
        self.assertEqual(2.2, gw1['domestic'])
        self.assertEqual(3.3, gw1['commercial'])
        self.assertEqual(4.4, gw1['industrial'])
        self.assertEqual(5.5, gw1['powerGeneration'])
        self.assertEqual(6.6, gw1['irrigation'])
        self.assertEqual(7.7, gw1['livestock'])
        # Ensure order of keys in dict is as expected
        keys = [k for k in gw1]
        self.assertTrue('publicSupply', keys[0])
        self.assertTrue('domestic', keys[1])
        self.assertTrue('commercial', keys[2])
        self.assertTrue('industrial', keys[3])
        self.assertTrue('powerGeneration', keys[4])
        self.assertTrue('irrigation', keys[5])
        self.assertTrue('livestock', keys[6])

        cd2_dict = wassi2_dict['countyDisaggregations'][1]
        self.assertEqual("fakehuc2", cd2_dict['huc12'])
        self.assertEqual("fakecounty2", cd2_dict['county'])
        w2 = cd2_dict['surfaceWeights']
        self.assertTrue(isinstance(w1, dict))
        self.assertEqual(1.2, w2['w4'])
        self.assertEqual(3.4, w2['w3'])
        self.assertEqual(5.6, w2['w2'])
        self.assertEqual(7.8, w2['w1'])
        # Ensure order of keys in dict is as expected
        keys = [k for k in w2]
        self.assertTrue('w1', keys[0])
        self.assertTrue('w2', keys[1])
        self.assertTrue('w3', keys[2])
        self.assertTrue('w4', keys[3])
        gw2 = cd2_dict['groundwaterWeights']
        self.assertTrue(isinstance(gw2, dict))
        self.assertEqual(7.7, gw2['publicSupply'])
        self.assertEqual(6.6, gw2['domestic'])
        self.assertEqual(5.5, gw2['commercial'])
        self.assertEqual(4.4, gw2['industrial'])
        self.assertEqual(3.3, gw2['powerGeneration'])
        self.assertEqual(2.2, gw2['irrigation'])
        self.assertEqual(1.1, gw2['livestock'])
        # Ensure order of keys in dict is as expected
        keys = [k for k in gw2]
        self.assertTrue('publicSupply', keys[0])
        self.assertTrue('domestic', keys[1])
        self.assertTrue('commercial', keys[2])
        self.assertTrue('industrial', keys[3])
        self.assertTrue('powerGeneration', keys[4])
        self.assertTrue('irrigation', keys[5])
        self.assertTrue('livestock', keys[6])