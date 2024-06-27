""" Sensor entity """
from typing import Self


class Sensor:
  """
  Sensor entity
  ---
  Attributes
    pk : Sensor ID
    name : Name of the sensor
    slug : Slug of the sensor
  """

  def __init__(self: Self, pk: int, name: str, slug: str) -> None:
    """ Constructor """
    self.pk = pk
    self.name = name
    self.slug = slug

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'Sensor(pk={self.pk}, name={self.name}, slug={self.slug})'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
