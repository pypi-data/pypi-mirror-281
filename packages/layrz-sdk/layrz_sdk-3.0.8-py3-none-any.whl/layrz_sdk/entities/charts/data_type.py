""" Chart Data type """
from enum import Enum
from typing import Self


class ChartDataType(Enum):
  """
  Chart Data Type
  """
  STRING = 'STRING'
  DATETIME = 'DATETIME'
  NUMBER = 'NUMBER'

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'ChartDataType.{self.value}'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
