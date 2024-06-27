""" Service entity """
from typing import Self


class OutboundService:
  """
  Outbound service definition
  ---
  Attributes
    - pk : Service ID
    - name : Service Name
  """

  def __init__(self: Self, pk: int, name: str) -> str | None | bool:
    self.pk = pk
    self.name = name

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'OutboundService(pk={self.pk}, name={self.name})'

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
