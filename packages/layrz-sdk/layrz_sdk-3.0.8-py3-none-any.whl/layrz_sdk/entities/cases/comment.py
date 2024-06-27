""" Comment entity """
from datetime import datetime
from typing import Self

from layrz_sdk.entities.general.user import User


class Comment:
  """
  Case comment entity definition
  ---
  Attributes
    - pk : Comment ID
    - content : Comment content
    - user : Operator/User what commented the case
    - submitted_at : Date of comment submission
  """

  def __init__(self: Self, pk: int, content: str, user: User, submitted_at: datetime) -> None:
    """ Constructor """
    self.pk = pk
    self.content = content
    self.user = user
    self.submitted_at = submitted_at

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable """
    return f'Comment(pk={self.pk}, content="{self.content}", user={self.user}, submitted_at={self.submitted_at})'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
