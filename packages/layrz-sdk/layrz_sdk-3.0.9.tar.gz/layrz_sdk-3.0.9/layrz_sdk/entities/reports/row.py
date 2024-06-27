""" Report row """

from typing import List, Self

from .col import ReportCol


class ReportRow:
  """
  Report row definition

  Available attributes
  --------------------
    content (list(ReportCol)): Cols to display
    height (float): Height of the cell, in points (pt)
    compact (bool): Compact mode
  """

  def __init__(
    self: Self,
    content: List[ReportCol],
    height: float = None,
    compact: bool = False,
  ) -> None:
    """ Constructor """
    self.content = content
    self.compact = compact

    if height is not None:
      raise DeprecationWarning('height is deprecated.')

  @property
  def _readable(self: Self) -> str | None | bool:
    """ Readable property """
    return f'ReportRow(content={self.content})'

  def __str__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable

  def __repr__(self: Self) -> str | None | bool:
    """ Readable property """
    return self._readable
