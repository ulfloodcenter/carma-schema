from dataclasses import dataclass


@dataclass
class CropData:
    year: int
    crop_area: float
    crop_area_detail: dict = None


@dataclass
class DevelopedArea:
    year: int
    area: float


@dataclass
class SurfaceWeightsWaSSI:
    w1: float
    w2: float
    w3: float
    w4: float


@dataclass
class AnalysisWaSSI:
    huc12: str
    county: str
    cropYear: int
    developedAreaYear: int
    surfaceWeights: SurfaceWeightsWaSSI
