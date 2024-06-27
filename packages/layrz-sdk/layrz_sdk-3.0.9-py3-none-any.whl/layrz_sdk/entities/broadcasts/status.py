""" Broadcast result Status """
from enum import Enum
from typing import Self


class BroadcastStatus(Enum):
  """ Broadcast result status """
  OK = 'OK'
  BADREQUEST = 'BADREQUEST'
  INTERNALERROR = 'INTERNALERROR'
  UNAUTHORIZED = 'UNAUTHORIZED'
  UNPROCESSABLE = 'UNPROCESSABLE'
  DISCONNECTED = 'DISCONNECTED'

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'BroadcastStatus.{self.value}'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
