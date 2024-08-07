import numpy as np
from mrsimulator.utils.abstract_list import AbstractList
from pydantic.v1 import BaseModel

from . import Transition

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


class TransitionList(AbstractList):
    def __init__(self, data: list = []):
        super().__init__([self._check_for_transition_object(item) for item in data])

    @staticmethod
    def _check_for_transition_object(item):
        if isinstance(item, dict):
            return Transition(**item)
        if not isinstance(item, Transition):
            raise ValueError(
                "Expecting a Transition object or an equivalent python dict object, "
                f"instead found {item.__class__.__name__}."
            )
        return item

    def __setitem__(self, index, item):
        self._list[index] = self._check_for_transition_object(item)

    def append(self, item):
        super().append(self._check_for_transition_object(item))

    def filter(self, P=None, PP=None, D=None):
        """Filter a list of transitions to satisfy the filtering criterion.

        Args:
            list P: A list of `N` (m_final - m_initial) values, where `N` is the
                total number of sites within the spin system.
            list D: A list of `N` (m_final^2 - m_initial^2) values, where `N` is the
                total number of sites within the spin system.
        """

        # to think
        # - filter based on transition.
        # - filter based on state.

        if P is PP is D is None:
            return self

        ts = self._list.copy()

        if P is not None:
            ts = TransitionList([item for item in ts if np.allclose(item.P, P)])

        # if PP is not None:
        #     ts = TransitionList([item for item in ts if np.allclose(item.PP, PP)])

        if D is not None:
            ts = TransitionList([item for item in ts if np.allclose(item.D, D)])
        # if transitions is not None:
        #     for transition in transitions:
        #         ts = TransitionList(
        #             [item for item in ts if item == Transition(**transition)]
        #         )
        # if start_state is not None:
        #     ts = [item for item in ts if ts.initial == start_state]
        return ts

        # lst = self._list
        # for i, element in enumerate(search):
        #     if isinstance(element, int):
        #         lst = [item for item in lst if item.delta_m(i) == element]
        #     if isinstance(element, list):
        #         lst = [
        #             item
        #             for item in lst
        #             if (item.initial[i] == element[1] and item.final[i] == element[0])
        #         ]
        # return lst
        #     return TransitionList(
        #         [item for item in self._list if np.all(item.initial == delta_ms)]
        #     )

        # if delta_ms is not None:
        #     return TransitionList(
        #         [item for item in self._list if np.all(item.delta_ms == delta_ms)]
        #     )
        # return TransitionList([item for item in self._list if item.p == p])


class TransitionPathway(TransitionList):
    """Base TransitionPathway class is a list of connected Transitions.

    Example:
        >>> from mrsimulator.transition import TransitionPathway, Transition
        >>> t1 = Transition(initial = [0.5, 0.5], final = [0.5, -0.5])
        >>> t2 = Transition(initial=[0.5, 0.5], final=[-0.5, 0.5])
        >>> path = TransitionPathway([t1, t2])
        >>> path
        |0.5, -0.5⟩⟨0.5, 0.5| ⟶ |-0.5, 0.5⟩⟨0.5, 0.5|, weight=(1+0j)
    """

    def __init__(self, pathway: list = [], weight=(1.0 + 0j)):
        super().__init__(pathway)
        self.weight = weight

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self._list == other._list and self.weight == other.weight

    def __repr__(self):
        path = " ⟶ ".join([repr(item) for item in self._list])
        return path + f", weight={self.weight}"

    def json(self, **kwargs) -> dict:
        """Parse the class object to a JSON compliant Python dictionary object.

        Example:
            >>> pprint(path.json())
            {'pathway': [{'final': [0.5, -0.5], 'initial': [0.5, 0.5]},
                         {'final': [-0.5, 0.5], 'initial': [0.5, 0.5]}],
             'weight': (1+0j)}
        """
        return {
            "pathway": [item.json() for item in self._list],
            "weight": self.weight,
        }

    def tolist(self):
        """Expand TransitionPathway to a Python list.

        Example:
            >>> path.tolist()
            [0.5, 0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5]
        """
        return np.asarray([item.tolist() for item in self._list]).ravel().tolist()


class SymmetryPathway(BaseModel):
    """Base SymmetryPathway class.

    Attributes:
        channels:
            The list of channels
        ch1:
            The symmetry pathway for the channel at index 0.
        ch2:
            The symmetry pathway for the channel at index 1.
        ch3:
            The symmetry pathway for the channel at index 2.
        total:
            The total symmetry pathway.
    """

    channels: list = []
    ch1: list = None
    ch2: list = None
    ch3: list = None

    @property
    def total(self):
        tot = np.zeros(len(self.ch1))
        check_mixing = np.zeros(len(self.ch1))
        chan = ["ch1", "ch2", "ch3"][: len(self.channels)]
        for i in range(len(self.ch1)):
            for ch in chan:
                if getattr(self, ch)[i] is not None:
                    check_mixing[i] = 1
                    tot[i] += sum(getattr(self, ch)[i])

        index = np.where(check_mixing == 0)[0]
        tot[index] = None
        return tot

    def __repr__(self):
        channel_ids = ["ch1", "ch2", "ch3"][: len(self.channels)]
        sp = "    "
        paths = [
            f"{sp}{i}({c.symbol}): " + " ⟶ ".join([str(_) for _ in getattr(self, i)])
            for c, i in zip(self.channels, channel_ids)
        ]
        paths.append(f"{sp}total: " + " ⟶ ".join([str(_) for _ in self.total]))
        return str("SymmetryPathway(\n" + "\n".join(paths) + "\n)")
