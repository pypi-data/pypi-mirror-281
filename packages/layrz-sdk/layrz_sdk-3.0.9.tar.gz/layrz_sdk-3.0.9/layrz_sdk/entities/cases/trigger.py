""" Trigger entity """
from typing import Self


class Trigger:
  """
  Trigger entity definition
  ---
  Attributes
    - pk : Trigger ID
    - name : Trigger name
    - code : Trigger code
  """

  def __init__(self: Self, pk: int, name: str, code: str) -> None:
    """ Constructor """
    self.pk = pk
    self.name = name
    self.code = code

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'Trigger(pk={self.pk}, name="{self.name}", code="{self.code}")'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
