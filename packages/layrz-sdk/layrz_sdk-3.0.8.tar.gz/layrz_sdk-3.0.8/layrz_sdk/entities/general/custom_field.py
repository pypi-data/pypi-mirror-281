""" Custom Field entitiy """
from typing import Self


class CustomField:
  """
  Custom field definition
  ---
  Attributes
    - name : Name of the custom field
    - value : Value of the custom field
  """

  def __init__(self: Self, name: str, value: str) -> None:
    """ Constructor """
    self.name = name
    self.value = value

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'CustomField(name={self.name}, value={self.value})'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
