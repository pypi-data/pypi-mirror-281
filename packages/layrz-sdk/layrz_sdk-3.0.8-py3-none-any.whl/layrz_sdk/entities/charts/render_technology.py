""" Chart rendering technology / library """
from enum import Enum
from typing import Self


class ChartRenderTechnology(Enum):
  """
  Chart Alignment
  """
  CANVAS_JS = 'CANVAS_JS'
  GRAPHIC = 'GRAPHIC'
  SYNCFUSION_FLUTTER_CHARTS = 'SYNCFUSION_FLUTTER_CHARTS'
  FLUTTER_MAP = 'FLUTTER_MAP'
  APEX_CHARTS = 'APEX_CHARTS'
  FLUTTER = 'FLUTTER'

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'ChartRenderTechnology.{self.value}'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
