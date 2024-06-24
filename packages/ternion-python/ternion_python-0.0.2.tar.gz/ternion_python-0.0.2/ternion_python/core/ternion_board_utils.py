# import time
# from typing import List
# from serial import Serial
# from serial.tools.list_ports_common import ListPortInfo

# from ternion_logs import log
from ternion_port_utils import *
from ternion_port_utils import tpu

"""
Singleton class
"""


class TernionBoardUtils:
    __instance = None
    __tpu = tpu()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_port_utils(self) -> tpu:
        return self.__tpu

    def get_available_ports(self) -> list[str]:
        """
        Gets names of available serial ports.

        Returns:
            list[str]: A list of strings, each representing the name of an available serial port.
        """
        return self.__tpu.get_available_port_names()

    def check_port(self, sp: Serial) -> bool:
        """
        Checks if the given serial port is open.

        Args:
            port (Serial): The serial port to check.

        Returns:
            bool: True if the serial port is open, False otherwise.
        """
        if sp is None or not sp.is_open:
            log.error("Serial port not open.")
            return False
        else:
            return True

    def get_firmware_info(self, sp: Serial) -> str:
        """
        Gets the firmware information from the given serial port.

        Args:
            port (Serial): The serial port to get the firmware information from.

        Returns:
            str: The firmware information as a string.
        """
        if not self.check_port(sp):
            return ""

        try:
            spu = self.__tpu
            spu.write_line(sp, "ver v 0")
            resp = spu.read_line_string(sp)

            if resp.endswith("\r\n"):
                resp = resp.strip()
                start_pos: int = resp.find("TERNION")
                info: str = resp[start_pos:]
                return info
            else:
                return "Invalid firmware information"
        except Exception as e:
            log.error(f"Error getting firmware info: {e}")

    def get_serial_number(self, lps: ListPortInfo) -> str:
        """
        Gets the serial number from the given serial port.

        Args:
            port (Serial): The serial port to get the serial number from.

        Returns:
            str: The serial number as a string.
        """

        return self.__tpu.get_serial_number(lps)

    def ping_pong(self, sp: Serial) -> bool:
        """
        Sends a ping to the given serial port and checks the response.

        Args:
            port (Serial): The serial port to send the ping.

        Returns:
            bool: True if the ping was successful, False otherwise.
        """
        if not self.check_port(sp):
            return False

        try:
            spu = self.__tpu
            spu.write_line(sp, "!!PinG")
            resp = spu.read_line_string(sp)
            if resp.startswith("ok: PonG\r\n"):
                log.debug(f"Ping-Pong operation on {sp.name} completed.")
                return True
            else:
                return False
        except Exception as e:
            log.error(f"Error Ping-Pong operation at {sp.name}: {e}")
            return False

    def soft_reset(self, sp: Serial) -> bool:
        """
        Sends a soft reset to the given serial port and checks the response.

        Args:
            port (Serial): The serial port to send the soft reset.

        Returns:
            bool: True if the soft reset was successful, False otherwise.
        """
        if not self.check_port(sp):
            return False

        try:
            spu = self.__tpu

            spu.write_line(sp, "!!McLr")
            resp = spu.read_line_string(sp, 2)
            print(resp)
            if resp.endswith("\r\n"):
                log.debug(f"Soft-Reset operation on {sp.name} completed.")
                return True
            else:
                return False
        except Exception as e:
            log.error(f"Error Soft-Reset operation on {sp.name}: {e}")
            return False

    def hard_reset(self, sp: Serial) -> bool:
        """
        Sends a hard reset to the given serial port and checks the response.

        Args:
            sp (Serial): The serial port to send the hard reset.

        Returns:
            bool: True if the hard reset was successful, False otherwise.
        """
        if not self.check_port(sp):
            return False

        try:
            spu = self.__tpu
            spu.set_dtr(sp, True)
            spu.set_rts(sp, True)
            time.sleep(0.1)
            sp.baudrate = 57600
            spu.clear_buffers(sp)
            spu.set_dtr(sp, False)
            spu.set_rts(sp, False)
            resp = spu.read_line_string(sp, 2)
            sp.baudrate = 115200
            if resp.endswith("\r\n"):
                log.debug(f"Hard-Reset operation on {sp.name} completed.")
                return True
            else:
                return False
        except Exception as e:
            log.error(f"Error Hard-Reset operation on {sp.name}: {e}")

    def get_all_ternion_ports(self) -> List[Serial]:
        """
        Gets a list of all currently opened and available Ternion ports.

        Returns:
            List[Serial]: A list of all currently opened and available Ternion ports.
        """
        spu = self.__tpu
        ternion_ports: List[Serial] = []

        # check the currently opened ports
        sp_objects: List[Serial] = spu.get_opened_port_objects()
        for sp in sp_objects:
            try:
                if self.ping_pong(sp):
                    ternion_ports.append(sp)
            except Exception as e:
                log.error(f"Error checking port {sp.name}: {e}")

        # check the not opened ports
        opened_names: List[Serial] = spu.get_opened_port_names()
        all_names: List[str] = spu.get_all_port_names()
        port_names: List[str] = list(set(all_names) - set(opened_names))
        for name in port_names:
            try:
                sp: Serial = spu.open(name)
                if sp is not None:
                    if self.ping_pong(sp):
                        ternion_ports.append(sp)
                    spu.close(sp)
            except Exception as e:
                log.error(f"Error checking port {name}: {e}")

        return ternion_ports

    def get_all_ternion_port_names(self) -> List[str]:
        """
        Gets a list of all currently opened and available Ternion port names.

        Returns:
            List[str]: A list of all currently opened and available Ternion port names.
        """

        port_infos: List[Serial] = self.get_all_ternion_ports()
        port_names: List[str] = [port.name for port in port_infos]
        return port_names

    def get_all_ternion_port_infos(self) -> List[ListPortInfo]:
        """
        Gets a list of all currently opened and available Ternion port infos.

        Returns:
            List[ListPortInfo]: A list of all currently opened and available Ternion port infos.
        """

        spu = self.__tpu
        port_infos: List[ListPortInfo] = spu.get_all_port_infos()
        port_names: List[str] = self.get_all_ternion_port_names()
        target_port_infos: List[ListPortInfo] = []
        for pi in port_infos:
            if pi.device in port_names:
                target_port_infos.append(pi)
        return target_port_infos

    def get_ternion_board_count(self) -> int:
        """
        Gets the number of Ternion boards connected to the computer.

        Returns:
            int: The number of Ternion boards connected to the computer.
        """
        return len(self.get_all_ternion_port_names())


tbu = TernionBoardUtils

if __name__ == "__main__":
    port_utils = tpu()
    board_utils = tbu()
    port_names = board_utils.get_all_ternion_port_names()
    sp = port_utils.open(port_names[0], 115200)
    sp = port_utils.open(port_names[0], 115200)
    print(board_utils.get_all_ternion_port_names())
    # pi = port_utils.list_port_info()[0]
    # (port_utils.ping_pong(port))
    # print(port_utils.get_firmware_info(sp))
    # print(port_utils.get_serial_number(pi))
