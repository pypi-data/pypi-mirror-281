from ternion_board_utils import *
from ternion_port_utils_api import *


class TernionBoardUtilsApi:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__tpu = TernionBoardUtils()
        self.port = TernionPortUtilsApi()

    def get_available_ports(self) -> list[str]:
        return self.__tpu.get_available_ports()

    def check_port(self, sp: Serial) -> bool:
        return self.__tpu.check_port(sp)

    def get_firmware_info(self, sp: Serial) -> str:
        return self.__tpu.get_firmware_info(sp)

    def get_serial_number(self, sp: Serial) -> str:
        return self.__tpu.get_serial_number(sp)

    def ping_pong(self, sp: Serial) -> bool:
        return self.__tpu.ping_pong(sp)

    def soft_reset(self, sp: Serial) -> bool:
        return self.__tpu.soft_reset(sp)

    def hard_reset(self, sp: Serial) -> bool:
        return self.__tpu.hard_reset(sp)

    def get_all_ternion_ports(self) -> List[Serial]:
        return self.__tpu.get_all_ternion_ports()

    def get_all_ternion_port_names(self) -> List[str]:
        return self.__tpu.get_all_ternion_port_names()

    def get_all_ternion_port_infos(self) -> List[ListPortInfo]:
        return self.__tpu.get_all_ternion_port_infos()

    def get_ternion_board_count(self) -> int:
        return self.__tpu.get_ternion_board_count()


if __name__ == "__main__":

    api = TernionBoardUtilsApi()
    port_names = api.get_all_ternion_port_names()
    port_name = port_names[0]
    sp = api.port.open(port_name, 115200)

    # print(api.port.set_dtr(sp, True))

    # (api.ping_pong(port))
    print(api.get_firmware_info(sp))
    # print(api.get_serial_number(pi))
    print(api.get_all_ternion_port_names())
