import re
import time
from typing import Optional
import threading
from typing import Callable
from dataclasses import dataclass
from serial import Serial

from core import *


class TernionCommander(lnk):

    def __init__(self, port_id: str | int = None, dont_connect: bool = False):
        super().__init__(port_id)

        if not dont_connect:
            self.connect()

    def __get_indexes(self, indexes: tuple[int, int] | int) -> tuple[int, int]:
        """
        Get the indexes.

        This function gets the indexes from the given value.
        If the given value is an integer, it returns a tuple with the value twice.
        If the given value is a tuple with two integers, it returns the tuple.

        Args:
            indexes (tuple[int, int] | int): The indexes to get.

        Returns:
            tuple[int, int]: The indexes as a tuple.
        """

        if isinstance(indexes, int):
            indexes = (indexes, indexes)
        return indexes

    def __check_min_max(self, val: int, min_val: int, max_val: int) -> bool:
        """
        Check if the given value is within the specified range.

        This function checks if the given value is within the specified range.
        If the value is not within the range, it raises an exception.

        Args:
            val (int): The value to check.
            min_val (int): The minimum value in the range.
            max_val (int): The maximum value in the range.

        Returns:
            bool: True if the value is within the range, False otherwise.

        Raises:
            ValueError: If the value is not within the range.
        """

        return min_val <= val <= max_val

    def __check_index_range(
        self, first_index: int, last_index: int, min_index: int = 0, max_index: int = 3
    ) -> bool:
        """
        Check if the given range is valid.

        This function checks if the given range is valid.
        If the range is not valid, it raises an exception.

        Args:
            first_index (int): The index of the start of the range.
            last_index (int): The index of the end of the range.
            min_index (int, optional): The minimum index in the range. Defaults to 0.
            max_index (int, optional): The maximum index in the range. Defaults to 3.

        Returns:
            bool: True if the range is valid, False otherwise.

        Raises:
            ValueError: If the range is not valid.
        """

        # The last index must be less than or equal to {max_val}
        if last_index > max_index:
            log.error(
                f"The end index {last_index} must be less than or equal to {max_index}."
            )
            return False

        # The start index must be less than or equal to the end index
        if first_index > last_index:
            log.error(
                f"The start index {first_index} must be less than or equal to the end index {last_index}."
            )
            return False

        # The start index and end index must be between {min_val} and {max_val}
        if not self.__check_min_max(first_index, min_index, max_index):
            log.error(
                f"The start index {first_index} must be between {min_index} and {max_index}."
            )
            return False

        # The end index must be between {min_val} and {max_val}
        if not self.__check_min_max(last_index, min_index, max_index):
            log.error(
                f"The end index {last_index} must be between {min_index} and {max_index}."
            )
            return False

        return True

    def led_fade_one_shot(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
    ) -> Optional[str]:
        """
        Sends a fade one shot command to the Ternion board through the serial port and reads the response.

        This function sends a fade one shot command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 3, or an integer between 0 and 3.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to fade.
            head_delay (int): The head delay in milliseconds. Defaults to 0.
            fade_duration (int): The fade duration in milliseconds. Defaults to 500.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The indexes must be a tuple with two integers between 0 and 3
        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        # The head delay must be between 0 and 65000
        if not self.__check_min_max(head_delay, 0, 65000):
            log.error(f"The head delay {head_delay} must be between 0 and 65000.")
            return None

        # The fade duration must be between 0 and 65000
        if not self.__check_min_max(fade_duration, 0, 65000):
            log.error(f"The fade duration {fade_duration} must be between 0 and 65000.")
            return None

        # Sends the command, waits for response and return the response to the caller
        return self.send_command(f"fade o {s}..{e} {head_delay} {fade_duration}")

    def led_fade_continuous(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
        total_duration: int = 1000,
    ) -> Optional[str]:
        """
        Sends a fade continuous command to the Ternion board through the serial port and reads the response.

        This function sends a fade continuous command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 3, or an integer between 0 and 3.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to fade.
            head_delay (int): The head delay in milliseconds. Defaults to 0.
            fade_duration (int): The fade duration in milliseconds. Defaults to 500.
            total_duration (int): The total duration in milliseconds. Defaults to 1000.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The indexes must be a tuple with two integers between 0 and 3
        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        # The head delay must be between 0 and 65000
        if not self.__check_min_max(head_delay, 0, 65000):
            log.error(f"The head delay {head_delay} must be between 0 and 65000.")
            return None

        # The fade duration must be between 0 and 65000
        if not self.__check_min_max(fade_duration, 0, 65000):
            log.error(f"The fade duration {fade_duration} must be between 0 and 65000.")
            return None

        # The total duration must be between 0 and 65000
        if not self.__check_min_max(total_duration, 0, 65000):
            log.error(
                f"The total duration {total_duration} must be between 0 and 65000."
            )
            return None

        # The total duration must be greater than the sum of head delay and fade duration
        if head_delay + fade_duration > total_duration:
            log.error(
                f"The total duration {total_duration} must be greater than the sum of head delay {head_delay} and fade duration {fade_duration}."
            )
            return None

        # Sends the command, waits for response and return the response to the caller
        return self.send_command(
            f"fade c {s}..{e} {head_delay} {fade_duration} {total_duration}"
        )

    def led_fade_repeat(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
        total_duration: int = 1000,
        repeat_count: int = 3,
    ) -> Optional[str]:
        """
        Sends a fade repeat command to the Ternion board through the serial port and reads the response.

        This function sends a fade repeat command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 3, or an integer between 0 and 3.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to fade.
            head_delay (int): The head delay in milliseconds. Defaults to 0.
            fade_duration (int): The fade duration in milliseconds. Defaults to 500.
            total_duration (int): The total duration in milliseconds. Defaults to 1000.
            repeat_count (int): The number of times to repeat the fade. Defaults to 3.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        # The head delay must be between 0 and 65000
        if not self.__check_min_max(head_delay, 0, 65000):
            log.error(f"The head delay {head_delay} must be between 0 and 65000.")
            return None

        # The fade duration must be between 0 and 65000
        if not self.__check_min_max(fade_duration, 0, 65000):
            log.error(f"The fade duration {fade_duration} must be between 0 and 65000.")
            return None

        # The total duration must be between 0 and 65000
        if not self.__check_min_max(total_duration, 0, 65000):
            log.error(
                f"The total duration {total_duration} must be between 0 and 65000."
            )
            return None

        # The repeat count must be between 1 and 65000
        if head_delay + fade_duration > total_duration:
            log.error(
                f"The total duration {total_duration} must be greater than the sum of head delay {head_delay} and fade duration {fade_duration}."
            )
            return None

        # The repeat count must be between 1 and 65000
        if not self.__check_min_max(repeat_count, 1, 65000):
            log.error(f"The repeat count {repeat_count} must be between 1 and 65000.")
            return None

        # Sends the command, waits for response and return the response to the caller
        return self.send_command(
            f"fade r {s}..{e} {head_delay} {fade_duration} {total_duration} {repeat_count}"
        )

    def led_comet(
        self,
        mode: str = "right-swing",
        count: int = 1,
        fade_duration: int = 500,
        shift_duration: int = 100,
        wait_duration: int = 50,
    ) -> Optional[str]:
        """
        Sends a comet command to the Ternion board through the serial port and reads the response.

        This function sends a comet command to the Ternion board through the serial port.
        The command must be a tuple with string mode(right-swing, left-swing, left or right),
        integer count(1 to 65000), integer fade_duration(0 to 65000), integer shift_duration(0 to 65000)
        and integer wait_duration(0 to 65000).
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode to fade.
            count (int): The number of times to fade.
            fade_duration (int): The fade duration in milliseconds.
            shift_duration (int): The shift duration in milliseconds.
            wait_duration (int): The wait duration in milliseconds.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # The count must be between 0 and 65000
        if not self.__check_min_max(count, 0, 65000):
            log.error(f"The head delay {count} must be between 0 and 65000.")
            return None

        # The fade duration must be between 0 and 65000
        if not self.__check_min_max(fade_duration, 0, 65000):
            log.error(f"The head delay {fade_duration} must be between 0 and 65000.")
            return None

        # The shift duration must be between 0 and 65000
        if not self.__check_min_max(shift_duration, 0, 65000):
            log.error(f"The head delay {shift_duration} must be between 0 and 65000.")
            return None

        # The wait duration must be between 0 and 65000
        if not self.__check_min_max(wait_duration, 0, 65000):
            log.error(f"The head delay {wait_duration} must be between 0 and 65000.")
            return None

        # The mode must be right-swing, left-swing, left or right
        mode = mode.lower()
        _mode: str = "rs"
        if mode not in ["right-swing", "rs"]:
            _mode = "rs"
        elif mode not in ["left-swing", "ls"]:
            _mode = "ls"
        elif mode not in ["left", "l"]:
            _mode = "l"
        elif mode not in ["right", "r"]:
            _mode = "r"
        else:
            log.error(
                f"The mode {mode} must be right-swing, left-swing, left or right."
            )
            return None

        # Sends the command, waits for response and return the response to the caller
        return self.send_command(
            f"comet {_mode} {count} {fade_duration} {shift_duration} {wait_duration}"
        )

    def __adc_command(self, mode: str, indexes: tuple[int, int] | int) -> Optional[str]:
        """
        Sends an ADC command to the Ternion board through the serial port and reads the response.

        This function sends an ADC command to the Ternion board through the serial port.
        The command must be a tuple with string mode(r, v, p or i) and tuple indexes(2 int between 0 and 5)
        or int index(an int between 0 and 5).
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as an integer.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode to read.
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[int]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The mode must be r, v, p or i
        if mode not in ["r", "v", "p", "i"]:
            log.error(f"The mode {mode} must be r, v, p or i.")
            return None

        # The indexes must be a tuple with two integers between 0 and 5
        if not self.__check_index_range(s, e, 0, 5):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 5."
            )
            return None

        resp: str = self.send_command(f"adc {mode} {s}..{e}")
        if resp is None:
            return None

        count: int = e - s + 1
        tokens: list[str] = []
        if resp.startswith("ok:") and resp.endswith("\r\n"):
            resp = resp.strip()
            tokens = re.split(r"(\s|:|\.\.)", resp)
            tokens = [tk for tk in tokens if tk.strip()]
            return tokens[-count : len(tokens)]
        else:
            return None

    def adc_read_raw(self, indexes: tuple[int, int] | int) -> Optional[list[int]]:
        """
        Sends an ADC read raw command to the Ternion board through the serial port and reads the response.

        This function sends an ADC read raw command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 5, or an integer between 0 and 5.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a list of integers.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[list[int]]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        tokens: list[str] = self.__adc_command("r", indexes)
        if tokens is None:
            return None
        int_list: list[int] = [int(token) for token in tokens]
        return int_list

    def adc_read_voltage(self, indexes: tuple[int, int] | int) -> Optional[list[float]]:
        """
        Sends an ADC read voltage command to the Ternion board through the serial port and reads the response.

        This function sends an ADC read voltage command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 5, or an integer between 0 and 5.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a float.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[float]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        tokens: list[str] = self.__adc_command("v", indexes)
        if tokens is None:
            return None
        float_list: list[float] = [float(token) for token in tokens]
        return float_list

    def adc_read_percent(self, indexes: tuple[int, int] | int) -> Optional[list[float]]:
        """
        Sends an ADC read percent command to the Ternion board through the serial port and reads the response.

        This function sends an ADC read percent command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 5, or an integer between 0 and 5.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a float.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[float]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        # return self.__adc_command("p", indexes)
        tokens: list[str] = self.__adc_command("p", indexes)
        if tokens is None:
            return None
        float_list: list[float] = [float(token) for token in tokens]
        return float_list

    def adc_read_intensity(
        self, indexes: tuple[int, int] | int
    ) -> Optional[list[float]]:
        """
        Sends an ADC read intensity command to the Ternion board through the serial port and reads the response.

        This function sends an ADC read intensity command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 5, or an integer between 0 and 5.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a float.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[float]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        # return self.__adc_command("i", indexes)
        tokens: list[str] = self.__adc_command("i", indexes)
        if tokens is None:
            return None
        float_list: list[float] = [float(token) for token in tokens]
        return float_list

    def __psw_command(
        self, mode: str, indexes: tuple[int, int] | int
    ) -> Optional[list[str]]:
        """
        Sends a push button switch reading command to the Ternion board through the serial port and reads the response.

        This function sends a push button switch reading command to the Ternion board through the serial port.
        The command must be a tuple with two integers between 0 and 3, or an integer between 0 and 3.
        The mode must be one of 'b' (bits), 's' (states), or 'c' (counters).
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a list of strings.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode of the command, one of 'b' (bits), 's' (states), or 'c' (counters).
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[list[str]]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The mode must be r, v, p or i
        if mode not in ["b", "s", "c"]:
            log.error(f"The mode {mode} must be b, s, or c.")
            return None

        # The indexes must be a tuple with two integers between 0 and 5
        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        resp = self.send_command(f"psw {mode} {s}..{e}")
        # resp -> ok: mcu com psw b 0..3 1 1 1 1
        count: int = e - s + 1
        tokens: list[str] = []
        if resp.startswith("ok:") and resp.endswith("\r\n"):
            resp = resp.strip()
            tokens = re.split(r"(\s|:|\.\.)", resp)
            tokens = [tk for tk in tokens if tk.strip()]
            return tokens[-count : len(tokens)]
        else:
            return None

    def psw_read_bits(self, indexes: tuple[int, int] | int) -> Optional[list[bool]]:
        """
        Reads the state (True/False) of the push button switches and returns a list of booleans representing the state of the switches.

        This function sends a command to the Ternion board to read the state of the push button switches.
        The function returns a list of booleans representing the state of the switches.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[list[bool]]: A list of booleans representing the state of the push button switches, or None if the command is not sent successfully.
        """

        tokens: list[str] = self.__psw_command("b", indexes)
        if tokens is None:
            return None
        # 1 is OFF (False), 0: is ON (True)
        bool_list: list[bool] = [token == "0" for token in tokens]
        return bool_list

    def psw_read_states(self, indexes: tuple[int, int] | int) -> Optional[list[str]]:
        """
        Reads the state (OFF/ON/HOLD/REPEAT) of the push button switches and returns a list of strings representing the state of the switches.

        This function sends a command to the Ternion board to read the state of the push button switches.
        The function returns a list of strings representing the state of the switches.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[list[str]]: A list of strings representing the state of the push button switches, or None if the command is not sent successfully.
        """

        tokens: list[str] = self.__psw_command("s", indexes)
        return tokens

    def psw_read_counters(self, indexes: tuple[int, int] | int) -> Optional[list[int]]:
        """
        Reads the counter values of the push button switches and returns a list of integers representing the counter values.

        This function sends a command to the Ternion board to read the counter values of the push button switches.
        The function returns a list of integers representing the counter values.
        If the command is not sent successfully, the function returns None.

        Args:
            indexes (tuple[int, int] | int): The indexes to read.

        Returns:
            Optional[list[int]]: A list of integers representing the counter values of the push button switches, or None if the command is not sent successfully.
        """
        tokens: list[str] = self.__psw_command("c", indexes)
        if tokens is None:
            return None
        int_list: list[int] = [int(token) for token in tokens]
        return int_list

    def __pwm_command(
        self, mode: str, indexes: tuple[int, int] | int, value: float | int
    ) -> Optional[str]:
        """
        Sends a PWM command to the Ternion board through the serial port and reads the response.

        This function sends a PWM command to the Ternion board through the serial port.
        The command must be a tuple with string mode(f (frequency), p (percent), i (intensity), s (phase-shift), e (enable) or t (operation time)) and tuple indexes(2 int between 0 and 4)
        or int index(an int between 0 and 4).
        The value must be a float or an integer.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode to set the PWM.
            indexes (tuple[int, int] | int): The indexes to set the PWM.
            value (float | int): The value to set the PWM.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The mode must be f, p, i, s, e or t
        if mode not in ["f", "p", "i", "s", "e", "t"]:
            log.error(f"The mode {mode} must be f, p, i, s, e or t.")
            return None

        # The indexes must be a tuple with two integers between 0 and 4
        if not self.__check_index_range(s, e, 0, 4):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 4."
            )
            return None

        if mode in ["f", "t"]:
            if not self.__check_min_max(value, 2, 60000):
                log.error(
                    f"The frequency/operation-time value [{value}] must be between 2 and 60000."
                )
                return None
        if mode in ["p", "i", "s"]:
            if not self.__check_min_max(value, 0, 100):
                log.error(
                    f"The value of percent/intensity/phase-shift [{value}] must be between 0 and 100."
                )
                return None
        if mode in ["e"]:
            if not self.__check_min_max(value, 0, 1):
                log.error(f"The value of enable [{value}] must be between 0 and 1.")
                return None

        v_str: str = f"{value:.3f}"
        if mode in ["e", "t"]:
            v_str = f"{value:.0f}"

        return self.send_command(f"pwm {mode} {s}..{e} {v_str}")

    def pwm_set_frequency(
        self, indexes: tuple[int, int] | int, freq: float
    ) -> Optional[str]:
        """
        Sets the frequency of the PWM outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the PWM outputs.
            freq (float): The frequency (Hz) to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__pwm_command("f", indexes, freq)

    def pwm_set_phase_shift(
        self, indexes: tuple[int, int] | int, phase: float
    ) -> Optional[str]:
        """
        Sets the phase shift (in percent) of the PWM outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the PWM outputs.
            phase (float): The percent of the phase shift to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__pwm_command("p", indexes, phase)

    def pwm_set_intensity(
        self, indexes: tuple[int, int] | int, intensity: float
    ) -> Optional[str]:
        """
        Sets the intensity (in percent) of the PWM outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the PWM outputs.
            intensity (float): The percent of the intensity to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__pwm_command("i", indexes, intensity)

    def pwm_set_operation_time(
        self, indexes: tuple[int, int] | int, time: int
    ) -> Optional[str]:
        """
        Sets the operation time (in milliseconds) of the PWM outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the PWM outputs.
            time (int): The operation time (ms) to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__pwm_command("t", indexes, time)

    def pwm_set_enable(
        self, indexes: tuple[int, int] | int, enable: bool
    ) -> Optional[str]:
        """
        Sets the enable state (True: ON, False: OFF) of the PWM outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the PWM outputs.
            enable (bool): The enable state to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        enb = 1 if enable else 0
        return self.__pwm_command("e", indexes, enb)

    def __led_write_command(
        self, mode: str, indexes: tuple[int, int] | int, value: bool | int
    ) -> Optional[str]:
        """
        Sends a LED write command to the Ternion board through the serial port and reads the response.

        This function sends a LED write command to the Ternion board through the serial port.
        The command must be a tuple with string mode(d(digital) or b(binary)) and tuple indexes(2 int between 0 and 3)
        or int index(an int between 0 and 3).
        The value must be a boolean or integer.
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a string.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode of the command, one of 'd' (digital) or 'b' (binary).
            indexes (tuple[int, int] | int): The indexes to write.
            value (bool | int): The value to write.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The mode must be d or b
        if mode not in ["d", "b"]:
            log.error(f"The mode {mode} must be d or b.")
            return None

        # The indexes must be a tuple with two integers between 0 and 4
        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        s_value: str = ""

        # Binary mode, the value must be between 0 and 1
        if mode == "b":
            if not self.__check_min_max(value, 0, 1):
                log.error(f"The value [{value}] must be between 0 and 1.")
                return None
            else:
                s_value = "1" if value else "0"

        # Decimal mode, the value must be between 0 and 65535
        if mode == "d":
            if not self.__check_min_max(value, 0, 65535):
                log.error(f"The value [{value}] must be between 0 and 65535.")
                return None
            else:
                s_value = value % 16

        return self.send_command(f"led {mode} {s}..{e} {s_value}")

    def led_write_binary(
        self, indexes: tuple[int, int] | int, value: bool
    ) -> Optional[str]:
        """
        Sets the binary value of the allLED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.
            value (bool): The binary value to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__led_write_command("b", indexes, value)

    def led_write_decimal(
        self, indexes: tuple[int, int] | int, value: int
    ) -> Optional[str]:
        """
        Sets the decimal values of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.
            value (int): The decimal value to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__led_write_command("d", indexes, value)

    def led_write_hexadecimal(
        self, indexes: tuple[int, int] | int, value: int
    ) -> Optional[str]:
        """
        Sets the hexadecimal values of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.
            value (int): The hexadecimal value to set.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """
        return self.__led_write_command("d", indexes, value)

    def __led_read_command(
        self, mode: str, indexes: tuple[int, int] | int
    ) -> Optional[str]:
        """
        Sends a LED read command to the Ternion board through the serial port and reads the response.

        This function sends a LED read command to the Ternion board through the serial port.
        The command must be a tuple with string mode(b (bits) or s (states)) and tuple indexes(2 int between 0 and 3)
        or int index(an int between 0 and 3).
        The function sends the command to the Ternion board and waits for a response.
        If the response is received successfully, the function returns the response as a list of strings.
        If the command is not sent successfully, the function returns None.

        Args:
            mode (str): The mode to read the LED.
            indexes (tuple[int, int] | int): The indexes to read the LED.

        Returns:
            Optional[str]: The response from the Ternion board, or None if the command is not sent successfully.
        """

        # Get the indexes
        s, e = self.__get_indexes(indexes)

        # The mode must be r, v, p or i
        if mode not in ["b", "s"]:
            log.error(f"The mode {mode} must be b or s.")
            return None

        # The indexes must be a tuple with two integers between 0 and 5
        if not self.__check_index_range(s, e, 0, 3):
            log.error(
                f"The indexes {indexes} must be a tuple with two integers between 0 and 3."
            )
            return None

        resp: str = self.send_command(f"led {mode} {s}..{e}")
        if resp is None:
            return None

        count: int = e - s + 1
        tokens: list[str] = []
        if resp.startswith("ok:") and resp.endswith("\r\n"):
            resp = resp.strip()
            tokens = re.split(r"(\s|:|\.\.)", resp)
            tokens = [tk for tk in tokens if tk.strip()]
            return tokens[-count : len(tokens)]
        else:
            return None

    def led_read_bits(self, indexes: tuple[int, int] | int) -> Optional[bool]:
        """
        Reads the binary value of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.

        Returns:
            Optional[bool]: The binary values of the LED outputs, or None if the command is not sent successfully.
        """
        tokens: list[str] = self.__led_read_command("b", indexes)
        if tokens is None:
            return None
        bool_list = [token != "0" for token in tokens]
        return bool_list

    def led_read_states(self, indexes: tuple[int, int] | int) -> Optional[str]:
        """
        Reads the state (ON/OFF) of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.

        Returns:
            Optional[str]: The states of the LED outputs, or None if the command is not sent successfully.
        """
        tokens: list[str] = self.__led_read_command("s", indexes)
        return tokens

    def led_read_binary(self, indexes: tuple[int, int] | int) -> Optional[bool]:
        """
        Reads the binary value of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.

        Returns:
            Optional[bool]: The binary values of the LED outputs, or None if the command is not sent successfully.
        """
        return self.led_read_bits(indexes)

    def led_read_decimal(self, indexes: tuple[int, int] | int) -> Optional[int]:
        """
        Reads the decimal value of the LED outputs specified by the indexes.

        Args:
            indexes (tuple[int, int] | int): The indexes of the LED outputs.

        Returns:
            Optional[int]: The decimal value of the LED outputs, or None if the command is not sent successfully.
        """
        tokens: list[str] = self.led_read_bits(indexes)
        if tokens is None:
            return None
        bool_list = [token != "0" for token in tokens]
        binary_string = "".join(["1" if b else "0" for b in bool_list])
        decimal_value = int(binary_string, 2)
        return decimal_value


"""
# Using the ThreadPoolExecutor
"""
# class MultiBoardTestForThreadPoolExecutor:
#     def __init__(self, port_name: str, led_id: int):
#         cmd = TernionCommander(port_name)
#         ser = cmd.connect()
#         try:
#             while True and ser is not None:
#                 time.sleep(1)
#                 cmd.led_fade_one_shot(led_id, 0, 500)
#         except KeyboardInterrupt:
#             TernionPortUtils().close(ser)

# Using the ThreadPoolExecutor
# if __name__ == "__main__":
#     port_names = tbu().get_all_ternion_port_names()
#     with ThreadPoolExecutor() as executor:
#         executor.map(MultiBoardTestForThreadPoolExecutor, port_names, range(len(port_names)))


"""
Simple Solution
"""


class MultiBoardTestSimple:
    def __init__(self, port_name: str, led_id: int):
        self.cmd = TernionCommander(port_name, dont_connect=False)
        # self.ser = self.cmd.connect()


if __name__ == "__main__":
    port_names = tbu().get_all_ternion_port_names()
    units: list[MultiBoardTestSimple] = []
    for id, name in enumerate(port_names):
        u = MultiBoardTestSimple(name, id)
        units.append(u)

    run = True
    try:
        while run:
            time.sleep(0.5)
            for id, u in enumerate(units):
                u.cmd.led_fade_one_shot(id, 0, 250)
    except KeyboardInterrupt:
        for u in units:
            tpu().close(u.ser)
        run = False
