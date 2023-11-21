from __future__ import annotations

from abc import ABC, abstractmethod

import models


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> models.Context:
        return self._context

    @context.setter
    def context(self, context: models.Context) -> None:
        self._context = context

    @abstractmethod
    def next(self) -> None:
        pass
