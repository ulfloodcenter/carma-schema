from dataclasses import dataclass
from typing import List
from uuid import UUID
from decimal import Decimal

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

WATER_SOURCE_MAPPING = {
    'SW': 'Surface Water',
    'GW': 'Groundwater',
    'PD': 'Plant Discharge Water',
    'OT': 'Other',
    '-nr-': 'Not reported',
}
WATER_SOURCE_MAPPING_NA = 'N/A'

WATER_TYPE_MAPPING = {
    'FR': 'Fresh',
    'SA': 'Saline',
    'BR': 'Brackish',
    'BE': 'Reclaimed',
    'OT': 'Other',
    '-nr-': 'Not reported',
}
WATER_TYPE_MAPPING_NA = 'N/A'


@dataclass_json
@dataclass
class Unit:
    name: str
    primaryDimension: str
    secondaryDimension: str
    tertiaryDimension: str


@dataclass_json
@dataclass
class WaterUseDataset:
    entityType: str
    waterSource: str
    waterType: str
    sector: str
    description: str
    sourceData: str
    year: int
    value: float
    unit: dict
    huc12: str = None
    county: str = None


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
class ConsumptionOrWithdrawalDatum:
    year: int
    value: float
    waterSource: List[str]
    waterType: List[str]

    def __post_init__(self):
        # Interpret USGS water source values
        # print(f"waterSource: {self.waterSource}")
        source_values = []
        for ws in self.waterSource.split('&'):
            ws = ws.strip()
            if ws in WATER_SOURCE_MAPPING:
                source_values.append(WATER_SOURCE_MAPPING[ws])
            else:
                source_values.append(WATER_SOURCE_MAPPING_NA)
        self.waterSource = source_values

        # Interpret USGS water type values
        # print(f"waterType: {self.waterType}")
        source_types = []
        for wt in self.waterType.split('&'):
            wt = wt.strip()
            if wt in WATER_TYPE_MAPPING:
                source_types.append(WATER_TYPE_MAPPING[wt])
            else:
                source_types.append(WATER_TYPE_MAPPING_NA)
        self.waterType = source_types


@dataclass_json
@dataclass
class PowerPlantDataset:
    eiaPlantCode: int
    eiaLongitude: Decimal
    eiaLatitude: Decimal
    huc12: str = None
    consumptionUnit: Unit = None
    withdrawalUnit: Unit = None
    usgsConsumption: List[ConsumptionOrWithdrawalDatum] = None
    usgsWithdrawal: List[ConsumptionOrWithdrawalDatum] = None


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
    sectorWeightFactorsSurface: List[SectorWeightFactorSurfaceWaSSI]
    sectorWeightFactorsGroundwater: List[SectorWeightFactorGroundwaterWaSSI]
    description: str = None
    countyDisaggregations: List[CountyDisaggregationWaSSI] = None
