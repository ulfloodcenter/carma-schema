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
class GroundwaterWeightWaSSI:
    publicSupply: float = 0.0
    domestic: float = 0.0
    commercial: float = 0.0
    industrial: float = 0.0
    powerGeneration: float = 0.0
    irrigation: float = 0.0
    livestock: float = 0.0

    def __setitem__(self, key, value):
        if key == WELL_SECTORS[0]:
            self.publicSupply = value
        elif key == WELL_SECTORS[1]:
            self.domestic = value
        elif key == WELL_SECTORS[2]:
            self.commercial = value
        elif key == WELL_SECTORS[3]:
            self.industrial = value
        elif key == WELL_SECTORS[4]:
            self.powerGeneration = value
        elif key == WELL_SECTORS[5]:
            self.irrigation = value
        elif key == WELL_SECTORS[6]:
            self.livestock = value
        else:
            super.__setattr__(self, key, value)

    def accum(self, other):
        self.publicSupply += other.publicSupply
        self.domestic += other.domestic
        self.commercial += other.commercial
        self.industrial += other.industrial
        self.powerGeneration += other.powerGeneration
        self.irrigation += other.irrigation
        self.livestock += other.livestock


@dataclass_json
@dataclass
class GroundwaterWeightsWaSSI:
    gw1: GroundwaterWeightWaSSI


@dataclass_json
@dataclass
class CountyDisaggregationWaSSI:
    huc12: str
    county: str
    surfaceWeights: SurfaceWeightsWaSSI
    groundwaterWeights: GroundwaterWeightsWaSSI


@dataclass_json
@dataclass
class SectorWeightFactorSurfaceWaSSI:
    sector: str
    factors: List[str]


@dataclass_json
@dataclass
class SectorWeightFactorGroundwaterWaSSI:
    sector: str
    factors: List[str]


@dataclass_json
@dataclass
class AnalysisWaSSI:
    id: UUID
    cropYear: int
    developedAreaYear: int
    groundwaterWellsCompletedYear: int
    description: str = None
    sectorWeightFactorsSurface: List[SectorWeightFactorSurfaceWaSSI] = None
    sectorWeightFactorsGroundwater: List[SectorWeightFactorGroundwaterWaSSI] = None
    countyDisaggregations: List[CountyDisaggregationWaSSI] = None