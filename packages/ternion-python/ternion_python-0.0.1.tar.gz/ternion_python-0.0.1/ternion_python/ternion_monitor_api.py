
from ternion_monitor import *

class TernionMonitorApi(TernionMonitor):
    def __init__(self, link: lnk):
        super().__init__(link)

    def add_ln_listener(self, callback: Callable[[str], None]):
        """Adds a listener for all lines."""
        super().add_ln_listener(callback)

    def add_ev_listener(self, callback: Callable[[str], None]):
        """Adds a listener for all events."""
        super().add_ev_listener(callback)

    def add_ok_listener(self, callback: Callable[[str], None]):
        """Adds a listener for ok events."""
        super().add_ok_listener(callback)

    def add_er_listener(self, callback: Callable[[str], None]):
        """Adds a listener for error events."""
        super().add_er_listener(callback)

    def add_db_listener(self, callback: Callable[[str], None]):
        """Adds a listener for database events."""
        super().add_db_listener(callback)

    def add_psw_ev_listener(self, callback: Callable[[TernionSwitchEventData], None]):
        """Adds a listener for switch events."""
        super().add_psw_ev_listener(callback)

    def add_adc_ev_listener(self, callback: Callable[[TernionAnalogEventData], None]):
        """Adds a listener for analog events."""
        super().add_adc_ev_listener(callback)

    def start(self):
        """Starts the serial port reader thread."""
        super().start()

    def stop(self):
        """Stops the thread."""
        super().stop()

class UnitTest:

    def __init__(self, port_id: str | int = None):
        link = lnk(port_id)
        ser = link.connect()
        mon = TernionMonitorApi(link)
        mon.start()
        mon.add_adc_ev_listener(lambda evt: print(f"{evt.get_sender()} - {evt.get_volt()} - {format(evt.get_percent(), ".2f")}%"))
        mon.add_psw_ev_listener(lambda evt: print(f"{evt.get_sender()} - {evt.get_state()} - {evt.get_press_cnt()} - {evt.get_fire_cnt()} times"))

if __name__ == "__main__":
    port_names = tbu().get_all_ternion_port_names()
    units: list[UnitTest] = []
    for name in port_names:
        ut = UnitTest(name)
        units.append(ut)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for ut in units:
            ut.stop()

