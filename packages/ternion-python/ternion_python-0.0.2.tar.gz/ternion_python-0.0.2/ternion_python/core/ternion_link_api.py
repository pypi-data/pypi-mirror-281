from ternion_link import *


class TernionLinkApi(TernionLink):
    def __init__(self, port_id: str | int = None):
        super().__init__(port_id)

    def get_serial_port(self) -> Optional[Serial]:
        return super().get_serial_port()

    def connect(self) -> Optional[Serial]:
        return super().connect()

    def disconnect(self) -> None:
        super().disconnect()

    def send_command(self, command: str) -> str:
        return super().send_command(command)
