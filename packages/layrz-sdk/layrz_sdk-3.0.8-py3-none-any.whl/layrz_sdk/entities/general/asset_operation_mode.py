""" Asset Operation Mode """
from enum import Enum
from typing import Self


class AssetOperationMode(Enum):
  """
  Asset Operation mode definition
  It's an enum of the operation mode of the asset.
  """
  SINGLE = 'SINGLE'
  MULTIPLE = 'MULTIPLE'
  ASSETMULTIPLE = 'ASSETMULTIPLE'
  DISCONNECTED = 'DISCONNECTED'
  STATIC = 'STATIC'
  ZONE = 'ZONE'

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return self.value

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
