from dataclasses import dataclass
from typing import List
from uuid import UUID

from dataclasses_json import dataclass_json


WELL_SECTORS = [
    "Public Supply",
    "Domestic",
    "Commercial",
    "Industrial",
    "Power Generation",
    "Irrigation",
    "Livestock"
]

WELL_STATUS = [
    "Active",
    "Abandoned",
    "Destroyed",
    "Inactive"
]


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
class GroundwaterWell:
    sector: str
    status: str
    yearCompleted: int
    count: int


@dataclass_json
@dataclass
class SurfaceWeightsWaSSI:
    w1: float
    w2: float
    w3: float
    w4: float


@dataclass_json
@dataclass
class GroundwaterWeightsWaSSI:
    publicSupply: float
    domestic: float
    commercial: float
    industrial: float
    powerGeneration: float
    irrigation: float
    livestock: float


@dataclass_json
@dataclass
class CountyDisaggregationWaSSI:
    huc12: str
    county: str
    surfaceWeights: SurfaceWeightsWaSSI
    groundwaterWeights: GroundwaterWeightsWaSSI


@dataclass_json
@dataclass
class AnalysisWaSSI:
    id: UUID
    cropYear: int
    developedAreaYear: int
    description: str = None
    countyDisaggregations: List[CountyDisaggregationWaSSI] = None
