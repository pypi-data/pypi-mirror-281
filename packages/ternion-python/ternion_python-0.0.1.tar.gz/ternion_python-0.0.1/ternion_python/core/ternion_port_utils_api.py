from ternion_port_utils import *


class TernionPortUtilsApi:

    __instance = None
    __tpu = tpu()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_port_utils(self) -> tpu:
        return self.__tpu

    def get_opened_port_objects(self) -> List[Serial]:
        return self.__tpu.get_opened_port_objects()

    def get_opened_port_names(self) -> List[str]:
        return self.__tpu.get_opened_port_names()

    def open(self, port_name: str, baud_rate: int = 115200) -> Optional[Serial]:
        return self.__tpu.open(port_name, baud_rate)

    def close(self, sp: Serial) -> None:
        self.__tpu.close(sp)

    def write_bytes(self, sp: Serial, data: bytes, timeout=0.5) -> int:
        return self.__tpu.write_bytes(sp, data, timeout)

    def write_string(self, sp: Serial, data: str, timeout=0.5) -> int:
        return self.__tpu.write_string(sp, data, timeout)

    def write_line(self, sp: Serial, data: str, timeout=0.5) -> int:
        return self.__tpu.write_line(sp, data, timeout)

    def read_all(self, sp: Serial, timeout=0.5) -> bytes:
        return self.__tpu.read_all(sp, timeout)

    def read_bytes(self, sp: Serial, bytes_to_read: int = 128, timeout=0.5) -> bytes:
        return self.__tpu.read_bytes(sp, bytes_to_read, timeout)

    def read_line_bytes(self, sp: Serial, timeout=0.5) -> bytes:
        return self.__tpu.read_line_bytes(sp, timeout)

    def read_line_string(
        self, sp: Serial, bytes_to_read: int = 128, timeout=0.5
    ) -> str:
        return self.__tpu.read_line_string(sp, bytes_to_read, timeout)

    def set_dtr(self, sp: Serial, state: bool) -> bool:
        return self.__tpu.set_dtr(sp, state)

    def set_rts(self, sp: Serial, state: bool) -> bool:
        return self.__tpu.set_rts(sp, state)

    def clear_buffers(self, sp: Serial) -> bool:
        return self.__tpu.clear_buffers(sp)

    def get_serial_number(self, lps: ListPortInfo) -> str:
        return self.__tpu.get_serial_number(lps)

    def get_serial_number_from_port_name(self, port_name: str) -> str:
        return self.__tpu.get_serial_number_from_port_name(port_name)

    def get_all_port_infos(self) -> List[ListPortInfo]:
        return self.__tpu.get_all_port_infos()

    def get_all_port_names(self) -> List[str]:
        return self.__tpu.get_all_port_names()

    def get_port_info_from_port_name(self, port_name: str) -> ListPortInfo:
        return self.__tpu.get_port_info_from_port_name(port_name)

    def get_port_name_from_port_info(self, lpi: ListPortInfo) -> str:
        return self.__tpu.get_port_name_from_port_info(lpi)

    def print_serial_port_properties(self, sp: Serial) -> None:
        self.__tpu.print_serial_port_properties(sp)

    def print_port_info_properties(self, lpi: ListPortInfo) -> None:
        self.__tpu.print_port_info_properties(lpi)


# usage
if __name__ == "__main__":
    utils = TernionPortUtilsApi()

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
