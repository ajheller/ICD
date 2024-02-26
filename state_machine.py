from enum import Enum
from dataclasses import dataclass
import logging as log
import time
import inspect


class States(Enum):
    UNKNOWN = -1
    STANDBY = 0
    DEPLOY = 1
    MUSTER = 2
    READY = 3
    CAMPAIGN = 4
    SKIRMISH = 5
    REPORT = 6
    DIAGNOSTIC = 7
    RETREAT = 8


@dataclass
class StateMachine:

    state: States = States.UNKNOWN
    next_state = None

    node_set = []

    # internal variables
    is_done: bool = False
    is_ready: bool = False
    is_wait: bool = False
    is_halt: bool = True
    is_halt: bool = False

    quality_of_service: float = 0.0

    is_pass_muster = False
    is_pass_diagnostic = False

    def __init__(self):
        self.set_state(States.STANDBY)
        self.next_state = self.do_standby

    def set_state(self, new_state):
        # check for valid state
        self.state = new_state

    def process(self, count=1):
        for _ in range(count):
            log.debug("Calling -> %s", self.next_state.__name__)
            result = self.next_state()
        return result

    # RPC commands
    def start(self):
        pre_states = (States.STANDBY,)
        if self.state in pre_states:
            self.next_state = self.do_deploy
        else:
            raise (ValueError, f"Wrong state for start(): {self.state}")
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )

    def ready(self):
        pre_states = (States.DEPLOY,)
        if self.state in pre_states:
            self.next_state = self.do_muster
        else:
            raise (ValueError("Invalid command %s in state: %s", "ready", self.state))
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )

    def run(self):
        pre_states = (States.READY,)
        if self.state in pre_states:
            self.next_state = self.do_campaign
        else:
            raise (ValueError("Invalid command %s in state: %s", "run", self.state))

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )

    def wait(self):
        pass

    def done(self):
        self.is_done = True
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )

    def stop(self):
        self.is_stop = True
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    def halt(self):
        self.is_halt = True
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    # state processing

    def do_standby(self):
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    def do_deploy(self):
        self.set_state(States.DEPLOY)
        # cache node state
        # modify mode state

        if self.is_ready:
            self.next_state = self.do_muster

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        return True

    def do_muster(self):
        self.set_state(States.MUSTER)
        # perform environmental assessement
        # time transfer, clock sync
        # calibration
        pass_muster = True

        self.is_stop = False

        if pass_muster:
            self.next_state = self.do_ready
        else:
            self.next_state = self.do_diagnostic

        log.info("%f Mustering, next_state=%s", time.time(), self.next_state.__name__)
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )

        return True

    def do_ready(self):
        self.set_state(States.READY)

        self.is_halt = False

        if self.is_stop:
            self.next_state = self.do_retreat
        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        return True

    def do_campaign(self):
        self.set_state(States.CAMPAIGN)
        if self.is_halt or self.is_stop:
            self.next_state = self.do_report
        else:
            self.next_state = self.do_skirmish

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    def do_skirmish(self):
        self.set_state(States.SKIRMISH)
        self.next_state = self.do_campaign

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    def do_report(self):
        if self.is_stop:  # or self.is_halt:
            self.next_state = self.do_retreat
        else:
            self.next_state = self.do_ready

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass

    def do_diagnostic(self):
        pass_diagnostic = True

        if pass_diagnostic:
            self.next_state = self.do_muster
        else:
            self.next_state = self.retreat

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        return True

    def do_retreat(self):
        # restore node state
        self.next_state = self.do_standby

        log.info(
            "%f %s, next_state=%s",
            time.time(),
            inspect.stack()[0][3],
            self.next_state.__name__,
        )
        pass


def unit_test(log_level=log.INFO):

    log.basicConfig(format="%(levelname)s:%(message)s", level=log_level)

    s = StateMachine()
    s.process()

    s.start()
    s.process()

    s.ready()
    s.process()

    s.process()

    s.run()
    s.process(10)
    s.done()
    s.process()
    s.halt()
    s.process(10)

    s.stop()
    s.process(10)


if __name__ == "__main__":
    unit_test()

    print("bye!")
