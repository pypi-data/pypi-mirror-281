from typing import Literal
from dataclasses import dataclass
from moveread.boxes import Rectangle
from moveread.annotations import ImageMeta

@dataclass
class ImgOutput:
  img: str
  meta: ImageMeta | None = None

@dataclass
class Output:
  original: ImgOutput
  corrected: ImgOutput
  boxes: list[str]

@dataclass
class BaseInput:
  img: str
  model: str

@dataclass
class Uncorrected(BaseInput):
  tag: Literal['uncorrected'] = 'uncorrected'

@dataclass
class BaseCorrected(BaseInput):
  corrected: str

@dataclass
class Corrected(BaseCorrected):
  tag: Literal['corrected'] = 'corrected'

@dataclass
class BaseExtracted(BaseCorrected):
  contours: list
  contoured: str

@dataclass
class Extracted(BaseExtracted):
  tag: Literal['extracted'] = 'extracted'

@dataclass
class Selected(BaseCorrected):
  grid_coords: Rectangle
  tag: Literal['selected'] = 'selected'