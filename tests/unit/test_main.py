import unittest
from collections import OrderedDict
from dataclasses import asdict
import uuid

from carma_schema.types import AnalysisWaSSI, SurfaceWeightsWaSSI, GroundwaterWeightsWaSSI, GroundwaterWeightWaSSI, \
    CountyDisaggregationWaSSI
from carma_schema import get_wassi_analysis_by_id, update_wassi_analysis_instance


class TestMainModule(unittest.TestCase):
    def test_get_wassi_analysis_by_id(self):
        county_disagg1 = CountyDisaggregationWaSSI("fakehuc1", "fakecounty1",
                                                   SurfaceWeightsWaSSI(1.2, 3.4, 5.6, 7.8),
                                                   GroundwaterWeightsWaSSI(GroundwaterWeightWaSSI(0,
                                                                                                  0.00196,
                                                                                                  0.00381,
                                                                                                  0.0,
                                                                                                  0.0,
                                                                                                  0.0,
                                                                                                  0.0)))
        county_disagg2 = CountyDisaggregationWaSSI("fakehuc2", "fakecounty2",
                                                   SurfaceWeightsWaSSI(7.8, 5.6, 3.4, 1.2),
                                                   GroundwaterWeightsWaSSI(GroundwaterWeightWaSSI(0,
                                                                                                  0.0,
                                                                                                  0.00381,
                                                                                                  0.0,
                                                                                                  0.00196,
                                                                                                  0.00381,
                                                                                                  0.0)))

        id = uuid.uuid4()
        wassi_orig = AnalysisWaSSI(id, 2015, 2019, 2016, 2019, description='Test WaSSI analysis 2')
        wassi_orig.countyDisaggregations = [county_disagg1, county_disagg2]

        document = OrderedDict()
        analyses = OrderedDict()
        document['Analyses'] = [analyses]
        analyses['WaSSI'] = [asdict(wassi_orig)]

        # Test getting
        wassi_from_doc = get_wassi_analysis_by_id(document, id)
        self.assertEqual(wassi_orig.id, wassi_from_doc.id)
        self.assertEqual(wassi_orig.waterUseYear, wassi_from_doc.waterUseYear)
        self.assertEqual(wassi_orig.cropYear, wassi_from_doc.cropYear)
        self.assertEqual(wassi_orig.developedAreaYear, wassi_from_doc.developedAreaYear)
        self.assertEqual(wassi_orig.groundwaterWellsCompletedYear, wassi_from_doc.groundwaterWellsCompletedYear)
        for i, cda_orig in enumerate(wassi_orig.countyDisaggregations):
            cda_doc = wassi_from_doc.countyDisaggregations[i]
            self.assertEqual(cda_orig.huc12, cda_doc.huc12)
            self.assertEqual(cda_orig.county, cda_doc.county)
            self.assertEqual(cda_orig.surfaceWeights, cda_doc.surfaceWeights)
            self.assertEqual(cda_orig.groundwaterWeights, cda_doc.groundwaterWeights)

        # Test updating
        wassi_from_doc.waterUseYear = 2020
        wassi_from_doc.cropYear = 2020
        wassi_from_doc.developedAreaYear = 2021
        wassi_from_doc.groundwaterWellsCompletedYear = 2021
        wassi_from_doc.description = 'Updated description'
        wassi_from_doc.countyDisaggregations[0].surfaceWeights.w1 = 42.23
        status = update_wassi_analysis_instance(document, wassi_from_doc)
        self.assertTrue(status)
        updated = get_wassi_analysis_by_id(document, id)
        self.assertEqual(2020, updated.waterUseYear)
        self.assertEqual(2020, updated.cropYear)
        self.assertEqual(2021, updated.developedAreaYear)
        self.assertEqual(2021, updated.groundwaterWellsCompletedYear)
        self.assertEqual('Updated description', updated.description)
        self.assertEqual(42.23, updated.countyDisaggregations[0].surfaceWeights.w1)
        self.assertEqual(3.4, updated.countyDisaggregations[0].surfaceWeights.w2)
        self.assertEqual(7.8, updated.countyDisaggregations[1].surfaceWeights.w1)
        self.assertAlmostEqual(0.00196, updated.countyDisaggregations[0].groundwaterWeights.gw1['domestic'])
        self.assertAlmostEqual(0.00381, updated.countyDisaggregations[1].groundwaterWeights.gw1['commercial'])
