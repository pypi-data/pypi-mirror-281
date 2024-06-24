import re
import time
from typing import List, Optional
import serial
from serial import Serial as Serial
from serial.tools.list_ports_common import ListPortInfo
from serial.tools.list_ports import comports

from ternion_logs import log


"""
Singleton class
"""


class TernionPortUtils:
    __instance = None
    __opened_serial_ports = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_opened_port_objects(self) -> List[Serial]:
        """
        Gets a list of all currently opened serial ports.

        Returns:
            List[serial.Serial]: A list of all currently opened serial ports.
        """

        return list(self.__opened_serial_ports.values())

    def get_opened_port_names(self) -> List[str]:
        """
        Gets a list of all currently opened port names.

        Returns:
            List[str]: A list of all currently opened port names.
        """

        return list(self.__opened_serial_ports.keys())

    def open(self, port_name: str, baud_rate: int = 115200) -> Optional[Serial]:
        """
        Opens a serial port using the given port name and baudrate and returns the opened serial port.

        Args:
            port_name (str): The name of the serial port to open.
            baud_rate (int, optional): The baud rate to use for the serial port. Defaults to 115200.

        Returns:
            Optional[serial.Serial]: The opened serial port, or None if the port could not be opened.
        """

        if port_name in self.__opened_serial_ports:
            log.warn(f"Serial port {port_name} already opened.")
            return self.__opened_serial_ports[port_name]

        sp: Serial = serial.serial_for_url(
            port_name,
            baud_rate,
            rtscts=False,
            dsrdtr=False,
            timeout=0.5,
            do_not_open=True,
        )
        sp.dtr = False
        sp.rts = False
        try:
            sp.open()
            if sp.is_open:
                log.debug(f"Serial port {sp.name} opened successfully.")
                self.__opened_serial_ports[sp.name] = sp
                return sp
            else:
                log.error(f"Failed to open serial port.")
                return None
        except Exception as e:
            log.error(f"Error opening serial port {port_name}: {e}")
            return None

    def close(self, sp: Serial) -> bool:
        """
        Closes a serial port.

        Args:
            sp (Serial): The serial port to close.

        Returns:
            bool: True if the serial port was closed successfully, False otherwise.
        """

        try:
            if sp.is_open:
                sp.flushInput()
                sp.flushOutput()
                del self.__opened_serial_ports[sp.name]
                sp.close()
                log.debug(f"Serial port {sp.name} closed successfully.")
                return True
        except Exception as e:
            log.error(f"Error closing serial port {sp.name}: {e}")
            return False

    def write_bytes(self, sp: Serial, data: bytes, timeout=0.5) -> int:
        """
        Writes bytes to a serial port, then flushes the serial port.

        Args:
            sp (Serial): The serial port to write to.
            data (bytes): The bytes to write to the serial port.
            timeout (float, optional): The timeout for the write operation. Defaults to 0.5.

        Returns:
            int: The number of bytes written to the serial port, or -1 if an error occurred.
        """

        try:
            sp.timeout = timeout
            n = sp.write(data)
            sp.flush()
            if n != len(data):
                log.error(
                    f"Failed to write all {len(data)} bytes to serial port {sp.name}."
                )
            else:
                log.debug(f"Successfully wrote {n} bytes to serial port {sp.name}.")
            return n
        except Exception as e:
            log.error(f"Error writing to serial port {sp.name}: {e}")
            return -1

    def write_string(self, sp: Serial, data: str, timeout=0.5) -> int:
        """
        Writes a string to a serial port, then flushes the serial port.

        Args:
            sp (Serial): The serial port to write to.
            data (str): The string to write to the serial port.
            timeout (float, optional): The timeout for the write operation. Defaults to 0.5.

        Returns:
            int: The number of bytes written to the serial port, or -1 if an error occurred.
        """
        return self.write_bytes(sp, data.encode(), timeout)

    def write_line(self, sp: Serial, data: str, timeout=0.5) -> int:
        """
        Writes a string to a serial port followed by a carriage return and line feed
        character, then flushes the serial port.

        Args:
            sp (Serial): The serial port to write to.
            data (str): The string to write to the serial port.
            timeout (float, optional): The timeout for the write operation. Defaults to 0.5.

        Returns:
            int: The number of bytes written to the serial port, or -1 if an error occurred.
        """
        return self.write_string(sp, data + "\r\n", timeout)

    def read_all(self, sp: Serial, timeout=0.5) -> bytes:
        """
        Reads all available data from a serial port.

        Args:
            sp (Serial): The serial port to read from.
            timeout (float, optional): The timeout for the read operation. Defaults to 0.5.

        Returns:
            bytes: The bytes read from the serial port, or an empty bytes object if an error occurred.
        """

        try:
            sp.timeout = timeout
            data = sp.readall()
            log.debug(f"Successfully read {len(data)} bytes from {sp.name}.")
            return data
        except Exception as e:
            log.error(f"Error reading from {sp.name}: {e}")
            return b""

    def read_bytes(self, sp: Serial, bytes_to_read: int = 128, timeout=0.5) -> bytes:
        """
        Reads a specified number of bytes from a serial port.

        Args:
            sp (Serial): The serial port to read from.
            bytes_to_read (int, optional): The number of bytes to read from the serial port. Defaults to 128.
            timeout (float, optional): The timeout for the read operation. Defaults to 0.5.

        Returns:
            bytes: The bytes read from the serial port, or an empty bytes object if an error occurred.
        """

        try:
            sp.timeout = timeout
            data = sp.read(bytes_to_read)
            if len(data) != bytes_to_read:
                log.error(f"Failed to read all {bytes_to_read} bytes from {sp.name}.")
            else:
                log.debug(f"Successfully read {len(data)} bytes from {sp.name}.")
            return data
        except Exception as e:
            log.error(f"Error reading from {sp.name}: {e}")
            return b""

    def read_line_bytes(self, sp: Serial, timeout=0.5) -> bytes:
        """
        Reads a line of bytes from a serial port.

        A line is considered to be terminated by a carriage return and line feed
        sequence (\r\n).

        Args:
            sp (Serial): The serial port to read from.
            timeout (float, optional): The timeout for the read operation. Defaults to 0.5.

        Returns:
            bytes: The line read from the serial port, or an empty bytes object if an error occurred.
        """

        try:
            sp.timeout = timeout
            data = sp.readline()
            if data.endswith(b"\r\n"):
                log.debug(f"Successfully read line from {sp.name}.")
            else:
                log.debug(f"Timeout while trying to read line from {sp.name}.")
            return data
        except Exception as e:
            log.error(f"Error reading from {sp.name}: {e}")
            return b""

    def read_line_string(self, sp: Serial, timeout=0.5) -> str:
        """
        Reads a line of bytes from a serial port, then decodes the bytes to a string.

        A line is considered to be terminated by a carriage return and line feed
        sequence (\r\n).

        Args:
            sp (Serial): The serial port to read from.
            timeout (float, optional): The timeout for the read operation. Defaults to 0.5.

        Returns:
            str: The line read from the serial port, decoded to a string, or an empty string if an error occurred.
        """

        bytes = self.read_line_bytes(sp, timeout)
        ascii = bytes.decode("ascii", errors="ignore")
        if not "\r\n" in ascii:
            log.warn(f"Read partial line [{ascii}] from {sp.name}.")
        if ascii == "\r\n":
            log.warn(f"Read empty line (CR+LF) from {sp.name}.")
        return ascii

    def set_dtr(self, sp: Serial, state: bool) -> bool:
        """
        Sets the Data Terminal Ready (DTR) pin on a serial port.

        Args:
            sp (Serial): The serial port to set the DTR pin on.
            state (bool): The state of the DTR pin. True sets the DTR pin high, False sets it low.

        Returns:
            bool: True if the DTR pin was successfully set, False otherwise.
        """

        try:
            sp.dtr = state
            return True
        except Exception as e:
            log.error(f"Error setting DTR on serial port {sp.name}: {e}")
            return False

    def set_rts(self, sp: Serial, state: bool) -> bool:
        """
        Sets the Request To Send (RTS) pin on a serial port.

        Args:
            sp (Serial): The serial port to set the RTS pin on.
            state (bool): The state of the RTS pin. True sets the RTS pin high, False sets it low.

        Returns:
            bool: True if the RTS pin was successfully set, False otherwise.
        """
        try:
            sp.rts = state
            return True
        except Exception as e:
            log.error(f"Error setting RTS on serial port {sp.name}: {e}")
            return False

    def clear_buffers(self, sp: Serial) -> bool:
        """
        Clears the input and output buffers of a serial port.

        Args:
            sp (Serial): The serial port to clear the buffers of.

        Returns:
            bool: True if the buffers were successfully cleared, False otherwise.
        """

        try:
            sp.reset_input_buffer()
            sp.reset_output_buffer()
            return True
        except Exception as e:
            log.error(f"Error clearing buffers on serial port {sp.name}: {e}")
            return False

    def get_serial_number(self, lps: ListPortInfo) -> str:
        """
        Gets the serial number of the given list port info.

        Args:
            lps (ListPortInfo): The list port info to get the serial number from.

        Returns:
            str: The serial number of the given list port info. If the list port info does not have a serial number, an empty string is returned.
        """

        return lps.serial_number

    def get_serial_number_from_port_name(self, port_name: str) -> str:
        port_info: ListPortInfo = self.get_port_info_from_port_name(port_name)
        serial_number: str = self.get_serial_number(port_info)
        return serial_number

    def get_all_port_infos(self) -> List[ListPortInfo]:
        """
        Gets a list of all available serial port information.

        Returns:
            list[ListPortInfo]: A list of ListPortInfo objects, each representing the
                information of an available serial port.
        """
        return comports()

    def get_all_port_names(self) -> List[str]:
        """
        Gets a list of names of all serial ports currently available.

        Returns:
            list[str]: A list of strings, each representing the name of an available serial port.
        """
        return [port.device for port in self.get_all_port_infos()]

    def get_port_info_from_port_name(self, port_name: str) -> ListPortInfo:
        """
        Gets the ListPortInfo object for a given serial port name.

        Args:
            port_name (str): The name of the serial port to get the ListPortInfo object for.

        Returns:
            ListPortInfo: The ListPortInfo object for the given serial port name. If no port with the given name is found, an IndexError is raised.
        """
        port_infos = self.get_all_port_infos()
        for pi in port_infos:
            if pi.device == port_name:
                return pi
        log.error(f"No port found with name {port_name}.")
        return None

    def get_port_name_from_port_info(self, lpi: ListPortInfo) -> str:
        """
        Gets the name of a given ListPortInfo object.

        Args:
            lpi (ListPortInfo): The ListPortInfo object to get the name of.

        Returns:
            str: The name of the given ListPortInfo object.
        """
        return lpi.device

    def print_serial_port_properties(self, sp: Serial) -> None:
        """
        Prints the properties of a given serial port object.

        Args:
            sp (Serial): The serial port object to print the properties of.

        Returns:
            None
        """
        print(f"Properties of {sp.name}")
        for attr in dir(sp):
            # Filter out private and protected attributes
            if not attr.startswith("_"):
                try:
                    value = getattr(sp, attr)
                    print(f"{attr}: {value}")
                except Exception as e:
                    log.error(f"{attr}: (error: {e})")

    def print_port_info_properties(self, lpi: ListPortInfo) -> None:
        """
        Prints the properties of a given ListPortInfo object.

        Args:
            lpi (ListPortInfo): The ListPortInfo object to print the properties of.

        Returns:
            None

        This function loops through all the attributes of the given ListPortInfo object and prints them.
        Private and protected attributes are filtered out. If there is an error getting the value of an attribute,
        an error message is printed.
        """
        print(f"Properties of {lpi.device}")
        for attr in dir(lpi):
            # Filter out private and protected attributes
            if not attr.startswith("_"):
                try:
                    value = getattr(lpi, attr)
                    print(f"{attr}: {value}")
                except Exception as e:
                    log(f"{attr}: (error: {e})")


"""
export as tpu
"""
tpu = TernionPortUtils


# usage
if __name__ == "__main__":

    utils = tpu()

    names = utils.get_all_port_names()
    port_name = names[0]

    sp = utils.open(port_name, 115200)
    pi = utils.get_port_info_from_port_name(port_name)

    print(pi)
    print(utils.get_port_name_from_port_info(pi))
    print(utils.get_opened_port_names())
    # tpu.print_serial_sp_properties(sp)
    # tpu.set_dtr(sp, True)
    # tpu.set_rts(sp, True)
    # time.sleep(0.1)
    # tpu.set_dtr(sp, False)
    # tpu.set_rts(sp, False)
    # print(tpu.read_line_string(sp, 10))
    utils.close(sp)
    print(utils.get_opened_port_names())

    # list_info = tpu.list_sp_info()
    # tpu.print_sp_info_properties(list_info[0])

    # list_name = tpu.list_sp_name()

    # tpu.set_dtr(sp, True)
    # print(list_name)
