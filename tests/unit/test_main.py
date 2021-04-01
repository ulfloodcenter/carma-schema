import unittest
from collections import OrderedDict
from dataclasses import asdict
import uuid

from carma_schema.types import AnalysisWaSSI, SurfaceWeightsWaSSI, CountyDisaggregationWaSSI
from carma_schema import get_wassi_analysis_by_id


class TestMainModule(unittest.TestCase):
    def test_get_wassi_analysis_by_id(self):
        county_disagg1 = CountyDisaggregationWaSSI("fakehuc1", "fakecounty1",
                                                   SurfaceWeightsWaSSI(1.2, 3.4, 5.6, 7.8))
        county_disagg2 = CountyDisaggregationWaSSI("fakehuc2", "fakecounty2",
                                                   SurfaceWeightsWaSSI(7.8, 5.6, 3.4, 1.2))

        id = uuid.uuid4()
        wassi_orig = AnalysisWaSSI(id, 2019, 2016, description="Test WaSSI analysis 2",
                                   countyDisaggregations=[county_disagg1, county_disagg2])

        document = OrderedDict()
        analyses = OrderedDict()
        document['Analyses'] = [analyses]
        analyses['WaSSI'] = [asdict(wassi_orig)]

        wassi_from_doc = get_wassi_analysis_by_id(document, id)
        self.assertEqual(wassi_orig.id, wassi_from_doc.id)
        self.assertEqual(wassi_orig.cropYear, wassi_from_doc.cropYear)
        self.assertEqual(wassi_orig.developedAreaYear, wassi_from_doc.developedAreaYear)
        for i, cda_orig in enumerate(wassi_orig.countyDisaggregations):
            cda_doc = wassi_from_doc.countyDisaggregations[i]
            self.assertEqual(cda_orig.huc12, cda_doc.huc12)
            self.assertEqual(cda_orig.county, cda_doc.county)
            self.assertEqual(cda_orig.surfaceWeights, cda_doc.surfaceWeights)
