from enum import Enum, unique

from typing_extensions import Self


class EnumStateBase(Enum):
    def in_state(self: Self, *states: Self):
        return self in states


@unique
class State(EnumStateBase):
    INITIALIZING = 'state.initializing'
    INITIALIZED = 'state.initialized'
    RUNNING = 'state.running'
    PRE_STOPPED = 'state.pre_stopped'
    STOPPED = 'state.stopped'
