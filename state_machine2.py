#
#  New implementation of SRI SAFER State Machine
#  Aaron Heller <aaron.heller@sri.com>
#  29 Feb 2024
#

from enum import Enum
from dataclasses import dataclass
import logging as log
import time
import inspect


class State:
    def __init__(self, cv):
        self.cv = cv

    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"


class Unknown(State):
    def run(self):
        pass


class Standby(State):
    pass


class Deploy(State):
    pass


class Muster(State):
    pass


class Ready(State):
    pass


class Campaign(State):
    pass


class Skirmish(State):
    pass


class Report(State):
    pass


class Diagnostic(State):
    pass


class Retreat(State):
    pass


class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.run()

    def run(self):
        self.current_state = self.current_state.next()
        self.current_state.run()
