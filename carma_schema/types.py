# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

from dataclasses import dataclass, asdict
from typing import List, Tuple
from uuid import UUID

from dataclasses_json import dataclass_json


WELL_SECTORS = [
    "Public Supply",
    "Domestic",
    "Commercial",
    "Industrial",
    "Power Generation",
    "Irrigation",
    "Livestock",
    "Mining"
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

WASSI_SECTOR_ALL = 'All'
WASSI_SECTOR_IRR = 'Irrigation'
WASSI_SECTOR_IND = 'Industrial'
WASSI_SECTOR_PUB = 'Public Supply'
WASSI_SECTOR_PWR = 'Total Thermoelectric Power'
WASSI_SECTOR_DOM = 'Domestic'
WASSI_SECTOR_LVS = 'Livestock'
WASSI_SECTOR_MIN = 'Mining'
WASSI_SOURCE_ALL = 'All'
WASSI_SOURCE_SURF = 'Surface Water'
WASSI_SOURCE_GW = 'Groundwater'
WASSI_SOURCE_ANY = 'Any'


@dataclass_json
@dataclass
class Unit:
    name: str
    primaryDimension: str
    secondaryDimension: str
    tertiaryDimension: str


DEFAULT_USAGE_CONSUMPTION_UNIT = Unit("Mgal/d",
                                      "Million",
                                      "Gallon",
                                      "Day")


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

    def __hash__(self):
        return hash((self.entityType, self.waterSource, self.waterType,
                     self.sector, self.description, self.sourceData,
                     self.year, self.value, str(self.unit), self.huc12, self.county))

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def asdict(self) -> dict:
        """
        Return a dict version of the dataset, with huc12 or county
        attribute removed if None
        :return:
        """
        wud_dict = asdict(self)
        if self.county is None:
            del wud_dict['county']
        if self.huc12 is None:
            del wud_dict['huc12']
        return wud_dict


def get_wateruse_dataset_key(w: WaterUseDataset,
                             override_huc12=None,
                             override_county=None) -> frozenset:
    if override_huc12:
        return frozenset({w.entityType, w.waterSource, w.waterType,
                          w.sector, w.year, override_huc12})
    if override_county:
        return frozenset({w.entityType, w.waterSource, w.waterType,
                          w.sector, w.year, override_county})


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
        source_values = []
        for ws in self.waterSource.split('&'):
            ws = ws.strip()
            if ws in WATER_SOURCE_MAPPING:
                source_values.append(WATER_SOURCE_MAPPING[ws])
            else:
                source_values.append(WATER_SOURCE_MAPPING_NA)
        self.waterSource = source_values

        # Interpret USGS water type values
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
    eiaLongitude: float
    eiaLatitude: float
    consumptionUnit: Unit = DEFAULT_USAGE_CONSUMPTION_UNIT
    withdrawalUnit: Unit = DEFAULT_USAGE_CONSUMPTION_UNIT
    huc12: str = None
    usgsConsumption: List[ConsumptionOrWithdrawalDatum] = None
    usgsWithdrawal: List[ConsumptionOrWithdrawalDatum] = None


@dataclass_json
@dataclass
class SurfaceWeightsWaSSI:
    w1: float
    w2: float
    w3: float
    w4: float

    def __getitem__(self, name):
        return self.__getattribute__(name)


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
    mining: float = 0.0

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
        elif key == WELL_SECTORS[7]:
            self.mining = value
        else:
            super.__setattr__(self, key, value)

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def accum(self, other):
        self.publicSupply += other.publicSupply
        self.domestic += other.domestic
        self.commercial += other.commercial
        self.industrial += other.industrial
        self.powerGeneration += other.powerGeneration
        self.irrigation += other.irrigation
        self.livestock += other.livestock
        self.mining += other.livestock


@dataclass_json
@dataclass
class GroundwaterWeightsWaSSI:
    gw1: GroundwaterWeightWaSSI

    def __getitem__(self, name):
        return self.__getattribute__(name)


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

    @classmethod
    def get_default_factors(cls) -> Tuple:
        return (
            SectorWeightFactorSurfaceWaSSI(WASSI_SECTOR_IRR,
                                           ['w1', 'w2', 'w3']),
            SectorWeightFactorSurfaceWaSSI(WASSI_SECTOR_IND,
                                           ['w1', 'w3', 'w4']),
            SectorWeightFactorSurfaceWaSSI(WASSI_SECTOR_PUB,
                                           ['w1', 'w4']),
            SectorWeightFactorSurfaceWaSSI(WASSI_SECTOR_LVS,
                                           ['w1', 'w2', 'w3']),
            SectorWeightFactorSurfaceWaSSI(WASSI_SECTOR_MIN,
                                           ['w1', 'w3', 'w4'])
        )

@dataclass_json
@dataclass
class SectorWeightFactorGroundwaterWaSSI:
    sector: str
    factors: List[str]

    @classmethod
    def get_default_factors(cls) -> Tuple:
        return (
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_IRR,
                                               ['gw1']),
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_IND,
                                               ['gw1']),
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_PUB,
                                               ['gw1']),
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_DOM,
                                               ['gw1']),
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_LVS,
                                               ['gw1']),
            SectorWeightFactorGroundwaterWaSSI(WASSI_SECTOR_MIN,
                                               ['gw1'])
        )


@dataclass_json
@dataclass
class WassiValue:
    huc12: str
    sector: str
    waterSupplySource: str
    value: float


@dataclass_json
@dataclass
class AnalysisWaSSI:
    id: UUID
    waterUseYear: int
    cropYear: int
    developedAreaYear: int
    groundwaterWellsCompletedYear: int
    sectorWeightFactorsSurface: Tuple[SectorWeightFactorSurfaceWaSSI] = None
    sectorWeightFactorsGroundwater: Tuple[SectorWeightFactorGroundwaterWaSSI] = None
    description: str = None
    countyDisaggregations: List[CountyDisaggregationWaSSI] = None
    wassiValues: List[WassiValue] = None

    def __init__(self, id, waterUseYear, cropYear, developedAreaYear, groundwaterWellsCompletedYear,
                 sectorWeightFactorsSurface=SectorWeightFactorSurfaceWaSSI.get_default_factors(),
                 sectorWeightFactorsGroundwater=SectorWeightFactorGroundwaterWaSSI.get_default_factors(),
                 description=None, countyDisaggregations=None, wassiValues=None):
        self.id = id
        self.waterUseYear = waterUseYear
        self.cropYear = cropYear
        self.developedAreaYear = developedAreaYear
        self.groundwaterWellsCompletedYear = groundwaterWellsCompletedYear
        self.sectorWeightFactorsSurface = sectorWeightFactorsSurface
        self.sectorWeightFactorsGroundwater = sectorWeightFactorsGroundwater
        self.description = description
        self.countyDisaggregations = countyDisaggregations
        self.wassiValues = wassiValues

    def asdict(self) -> dict:
        """
        Return a dict version of the dataset, with optional values
        attribute removed if None
        :return:
        """
        wassi_dict = asdict(self)
        if self.description is None:
            del wassi_dict['description']
        if self.countyDisaggregations is None:
            del wassi_dict['countyDisaggregations']
        if self.wassiValues is None:
            del wassi_dict['wassiValues']
        return wassi_dict
