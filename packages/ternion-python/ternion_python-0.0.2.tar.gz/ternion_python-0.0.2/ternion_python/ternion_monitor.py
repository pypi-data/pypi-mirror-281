
from ternion_commander import *


@dataclass
class TernionSwitchEventData:
    sender: str
    src: str
    dst: str
    tag: str
    id: int
    state: bool
    press_cnt: int
    fire_cnt: int
    hold_cnt: int

    def get_sender(self):
        return self.sender
    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst

    def get_tag(self):
        return self.tag

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def get_press_cnt(self):
        return self.press_cnt

    def get_fire_cnt(self):
        return self.fire_cnt

    def get_hold_cnt(self):
        return self.hold_cnt


@dataclass
class TernionAnalogEventData:
    sender: str
    src: str
    dst: str
    tag: str
    id: int
    raw: int
    volt: float
    percent: float
    delta: int
    delta_v: float
    delta_p: float

    def get_sender(self):
        return self.sender

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst

    def get_tag(self):
        return self.tag

    def get_id(self):
        return self.id

    def get_raw(self):
        return self.raw

    def get_volt(self):
        return self.volt

    def get_percent(self):
        return self.percent

    def get_delta(self):
        return self.delta

    def get_delta_v(self):
        return self.delta_v

    def get_delta_p(self):
        return self.delta_p


class TernionMonitor:
    def __init__(self, link: lnk):
        """Initialize the TernionMonitor."""

        self.link = link

        self.ln_listeners: list[Callable[[str], None]] = []
        self.ev_listeners: list[Callable[[str], None]] = []
        self.ok_listeners: list[Callable[[str], None]] = []
        self.er_listeners: list[Callable[[str], None]] = []
        self.db_listeners: list[Callable[[str], None]] = []

        self.psw_ev_listeners: list[Callable[[TernionSwitchEventData], None]] = []
        self.adc_ev_listeners: list[Callable[[TernionAnalogEventData], None]] = []

        self.running = False
        self.thread = None

        if link is None or self.link.get_serial_port() is None:
            msg: str = f"The lnk is not connected to the Ternion board."
            log.error(msg)
            raise Exception(msg)
        
        # port_name = self.link.get_serial_port().name 
        # port_info = tpu().get_port_info_from_port_name(port_name)
        # self.serial_number: str = tpu().get_serial_number(port_info)

        self.serial_number: str = tpu().get_serial_number_from_port_name(self.link.get_serial_port().name )

    def add_ln_listener(self, callback: Callable[[str], None]):
        """Adds a listener for all lines."""
        self.ln_listeners.append(callback)

    def add_ev_listener(self, callback: Callable[[str], None]):
        """Adds a listener for all events."""
        self.ev_listeners.append(callback)

    def add_ok_listener(self, callback: Callable[[str], None]):
        """Adds a listener for ok events."""
        self.ok_listeners.append(callback)

    def add_er_listener(self, callback: Callable[[str], None]):
        """Adds a listener for error events."""
        self.er_listeners.append(callback)

    def add_db_listener(self, callback: Callable[[str], None]):
        """Adds a listener for database events."""
        self.db_listeners.append(callback)

    def add_psw_ev_listener(self, callback: Callable[[TernionSwitchEventData], None]):
        """Adds a listener for switch events."""
        self.psw_ev_listeners.append(callback)

    def add_adc_ev_listener(self, callback: Callable[[TernionAnalogEventData], None]):
        """Adds a listener for analog events."""
        self.adc_ev_listeners.append(callback)

    def start(self):
        """Starts the serial port reader thread."""
        self.running = True
        self.thread = threading.Thread(target=self.__read_line, daemon=True)
        self.thread.start()

    def stop(self):
        """Stops the thread."""
        self.running = False
        self.thread.join()

    def __read_line(self):
        """
        Reads a line from the serial port and calls the callback functions with the data.
        """
        try:
            sp: Serial = self.link.get_serial_port()
            spu: tpu = tpu()
            while self.running:
                data: bytes = spu.read_line_bytes(sp, 1)
                if len(data) < 2:
                    log.debug(f"No event data received from {sp.name}.")
                    continue
                ascii: str = data.decode("ascii", errors="ignore")
                line: str = ascii.strip()
                self.__process_message(line)

        except KeyboardInterrupt:
            self.stop()

    def __process_message(self, line: str):

        if line.startswith("ev"):
            for callback in self.ev_listeners:
                callback(line)
            self.__process_event_message(line)

        elif line.startswith("ok"):
            for callback in self.ok_listeners:
                callback(line)
            pass

        elif line.startswith("er"):
            for callback in self.er_listeners:
                callback(line)
            pass

        elif line.startswith("db"):
            for callback in self.db_listeners:
                callback(line)
            pass
        else:
            for callback in self.ln_listeners:
                callback(line)
            pass

    def __process_event_message(self, line: str):
        if "adc" in line:
            self.__process_adc_message(line)
        elif "psw" in line:
            self.__process_psw_message(line)

    def __process_psw_message(self, line: str):
        # ev: mcu * psw 2 0 107 117 2
        line = line.strip()
        tokens: list[str] = line.split()
        # Remove empty tokens or tokens that contain whitespace
        tokens = [token for token in tokens if token and not token.isspace()]

        src: str = tokens[1]
        dst: str = tokens[2]
        tag: str = tokens[3]

        numbers_after_psw = re.findall(r"psw\s+([\d\s]+)", line)
        numbers_list = [int(num) for num in numbers_after_psw[0].split()]

        psw_ev_data: TernionSwitchEventData = TernionSwitchEventData(
            sender= self.serial_number,
            src=src,
            dst=dst,
            tag=tag,
            id=numbers_list[0],
            state=True if numbers_list[1] else False,
            press_cnt=numbers_list[2],
            fire_cnt=numbers_list[3],
            hold_cnt=numbers_list[4],
        )

        for callback in self.psw_ev_listeners:
            callback(psw_ev_data)

    def __process_adc_message(self, line: str):
        # ev: mcu * adc 0 237 +101
        line = line.strip()
        tokens: list[str] = line.split()
        # Remove empty tokens or tokens that contain whitespace
        tokens = [token for token in tokens if token and not token.isspace()]
        src: str = tokens[1]
        dst: str = tokens[2]
        tag: str = tokens[3]

        numbers_after_adc = re.findall(r"adc\s+([\d\s+-]+)", line)
        numbers_list = [int(num) for num in numbers_after_adc[0].split()]

        adc_ev_data: TernionAnalogEventData = TernionAnalogEventData(
            sender= self.serial_number,
            src=src,
            dst=dst,
            tag=tag,
            id=numbers_list[0],
            raw=numbers_list[1],
            volt=numbers_list[1] * 3.3 / 100.0,
            percent=numbers_list[1] * 100.0 / 1023.0,
            delta=numbers_list[2],
            delta_v=numbers_list[2] * 3.3 / 100.0,
            delta_p=numbers_list[2] * 100.0 / 1023.0,
        )

        for callback in self.adc_ev_listeners:
            callback(adc_ev_data)

    # def join(self):
    #     sp: Serial = self.link.get_serial_port()
    #     try:
    #         while True and sp is not None:
    #             time.sleep(1)

    #     except KeyboardInterrupt:
    #         self.stop()

class UnitTest:

    def __init__(self, port_id: str | int = None):
        link = lnk(port_id)
        ser = link.connect()
        mon = TernionMonitor(link)
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

