from ternion_board_utils import *


class TernionLink:
    def __init__(self, port_id: str | int = None):
        """
        Initialize a TernionLink object.

        Args:
            port_id (str | int, optional): The ID of the port to connect to. Can be a port name (str) or a port index (int). If None, the first ternion port will be used. Defaults to None.

        Note:
            - If `port_id` is None, the first ternion port will be used.
            - If `port_id` is an int, it will be used as an index to get the corresponding port name.
            - If `port_id` is a string, it will be used as a port name.
        """

        self.port_id = port_id
        self.tpu = tpu()
        self.tbu = tbu()
        self.sp = None

        if self.port_id is None:
            # No port_id is given, use the first ternion port
            self.port_id = self.tbu.get_all_ternion_port_names()[0]
        elif isinstance(self.port_id, int):
            # A port index is given, use the corresponding port name
            port_names = self.tbu.get_all_ternion_port_names()
            index: int = self.port_id
            if index < len(port_names):
                # Get the port name at the given index
                self.port_id = port_names[index]
            else:
                # The given index is out of range, use the last port
                last_idx = len(port_names) - 1
                log.warn(
                    f"The port index can be [0..{last_idx}], the given index {index} is not allowed. The last index [{last_idx}] will be used."
                )
                # Get the port name at the last index
                self.port_id = port_names[last_idx]

    def get_serial_port(self) -> Optional[Serial]:
        """
        Get the serial port object.

        Returns:
            Optional[Serial]: The serial port object. If the TernionLink instance is not connected to any
            serial port, None will be returned.
        """

        return self.sp

    def connect(self) -> Optional[Serial]:
        if self.sp is not None and self.sp.is_open:
            self.disconnect()
        self.sp = self.tpu.open(self.port_id)
        if self.sp is None:
            log.error(f"Failed to connect to {self.port_id}.")
            return self.sp
        else:
            log.info(f"Successfully connected to {self.port_id}.")
            return self.sp

    def disconnect(self) -> None:
        """
        Disconnects the TernionLink from the serial port.

        This function closes the serial port connection.
        After calling this function, the TernionLink instance is no longer connected to any serial port.

        Returns:
            None
        """
        self.tpu.close(self.sp)
        self.sp = None

    def send_command(self, command: str) -> Optional[str]:
        """
        Sends a command to the Ternion board through the serial port and reads the response.

        This function sends a command to the Ternion board through the serial port.
        The command must be a string without line breaks.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            command (str): The command to send to the Ternion board.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        command = command.strip()  # remove leading/trailing whitespace
        length = len(command) + 2
        count: int = self.tpu.write_line(self.sp, command)
        if count != length:
            log.error(f"Failed to send command {command} ({count}/{length}).")
            return None
        line: str = self.tpu.read_line_string(self.sp)
        if line.endswith("\r\n"):
            log.debug(f"Received response: {line.strip()}")
            return line


if __name__ == "__main__":

    board_count = tbu().get_ternion_board_count()

    for i in range(board_count):
        link = TernionLink(i)
        if link.connect():
            line = link.send_command("adc p 0..5")
            print(line)
            time.sleep(1)
            link.disconnect()
