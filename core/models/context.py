from __future__ import annotations

from typing import Union

import models


class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    state: Union[None, models.State] = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state: models.State) -> None:
        self.transition_to(state)

    def transition_to(self, state: models.State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self.state = state
        self.state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    def next(self, *args, **kwargs):
        if self.state:
            self.state.next(*args, **kwargs)
        else:
            raise NotImplementedError
