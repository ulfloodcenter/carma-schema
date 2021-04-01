from dataclasses import dataclass
from typing import List
from uuid import UUID

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CropData:
    year: int
    crop_area: float
    crop_area_detail: dict = None


@dataclass_json
@dataclass
class DevelopedArea:
    year: int
    area: float


@dataclass_json
@dataclass
class SurfaceWeightsWaSSI:
    w1: float
    w2: float
    w3: float
    w4: float


@dataclass_json
@dataclass
class CountyDisaggregationWaSSI:
    huc12: str
    county: str
    surfaceWeights: SurfaceWeightsWaSSI


@dataclass_json
@dataclass
class AnalysisWaSSI:
    id: UUID
    cropYear: int
    developedAreaYear: int
    description: str = None
    countyDisaggregations: List[CountyDisaggregationWaSSI] = None
