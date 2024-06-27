import pydantic
from typing import List

class SpectralBand(pydantic.BaseModel):
    description: str
    standard: str
    fwhm_min: float
    fwhm_max: float
    fwhm_ratio: float
    gsd: float

class Sensor(pydantic.BaseModel):
    name: str
    bands: list[SpectralBand]