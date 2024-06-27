""" Chart exceptions """
from typing import Self


class ChartException(BaseException):
  """
  Chart Exception
  """

  def __init__(self: Self, message: str) -> None:
    """ Constructor """
    self._message = message

  @property
  def message(self: Self) -> str | None | bool:
    """ Message """
    return self._message

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'ChartException: {self._message}'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
