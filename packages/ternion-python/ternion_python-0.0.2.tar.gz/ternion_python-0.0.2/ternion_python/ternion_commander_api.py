from ternion_commander import *


class TernionCommanderApi(TernionCommander):
    def __init__(self, port_id: str | int = None, dont_connect: bool = False):
        super().__init__(port_id, dont_connect)

    def led_fade_one_shot(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
    ) -> Optional[str]:
        """
        Fade LEDs in a one-shot manner.

        Args:
            - indexes (tuple[int, int] | int): The indexes of the LEDs to fade.
            - head_delay (int, optional): Head delay in milliseconds. Defaults to 0.
            - fade_duration (int, optional): Fade duration in milliseconds. Defaults to 500.

        Returns:
            Optional[str]: The message from the super class if successful, None otherwise.
        """
        return super().led_fade_one_shot(indexes, head_delay, fade_duration)

    def led_fade_continuous(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
        total_duration: int = 1000,
    ) -> Optional[str]:
        return super().led_fade_continuous(
            indexes, head_delay, fade_duration, total_duration
        )

    def led_fade_repeat(
        self,
        indexes: tuple[int, int] | int,
        head_delay: int = 0,
        fade_duration: int = 500,
        total_duration: int = 1000,
        repeat_count: int = 3,
    ) -> Optional[str]:
        return super().led_fade_repeat(
            indexes, head_delay, fade_duration, total_duration, repeat_count
        )

    def led_comet(
        self,
        mode: str = "right-swing",
        count: int = 1,
        fade_duration: int = 500,
        shift_duration: int = 100,
        wait_duration: int = 50,
    ) -> Optional[str]:
        return super().led_comet(
            mode, count, fade_duration, shift_duration, wait_duration
        )

    def adc_read_raw(self, indexes: tuple[int, int] | int) -> Optional[list[int]]:
        return super().adc_read_raw(indexes)

    def adc_read_voltage(self, indexes: tuple[int, int] | int) -> Optional[list[float]]:
        return super().adc_read_voltage(indexes)

    def adc_read_percent(self, indexes: tuple[int, int] | int) -> Optional[list[float]]:
        return super().adc_read_percent(indexes)

    def adc_read_intensity(
        self, indexes: tuple[int, int] | int
    ) -> Optional[list[float]]:
        return super().adc_read_intensity(indexes)

    def psw_read_bits(self, indexes: tuple[int, int] | int) -> Optional[list[bool]]:
        return super().psw_read_bits(indexes)

    def psw_read_states(self, indexes: tuple[int, int] | int) -> Optional[list[str]]:
        return super().psw_read_states(indexes)

    def psw_read_counters(self, indexes: tuple[int, int] | int) -> Optional[list[int]]:
        return super().psw_read_counters(indexes)

    def pwm_set_frequency(
        self, indexes: tuple[int, int] | int, freq: float
    ) -> Optional[str]:
        return super().pwm_set_frequency(indexes, freq)

    def pwm_set_phase_shift(
        self, indexes: tuple[int, int] | int, phase: float
    ) -> Optional[str]:
        return super().pwm_set_phase_shift(indexes, phase)

    def pwm_set_intensity(
        self, indexes: tuple[int, int] | int, intensity: float
    ) -> Optional[str]:
        return super().pwm_set_intensity(indexes, intensity)

    def pwm_set_operation_time(
        self, indexes: tuple[int, int] | int, time: int
    ) -> Optional[str]:
        return super().pwm_set_operation_time(indexes, time)

    def pwm_set_enable(
        self, indexes: tuple[int, int] | int, enable: bool
    ) -> Optional[str]:
        return super().pwm_set_enable(indexes, enable)

    def led_write_binary(
        self, indexes: tuple[int, int] | int, value: bool
    ) -> Optional[str]:
        return super().led_write_binary(indexes, value)

    def led_write_decimal(
        self, indexes: tuple[int, int] | int, value: int
    ) -> Optional[str]:
        return super().led_write_decimal(indexes, value)

    def led_write_hexadecimal(
        self, indexes: tuple[int, int] | int, value: int
    ) -> Optional[str]:
        return super().led_write_hexadecimal(indexes, value)

    def led_read_bits(self, indexes: tuple[int, int] | int) -> Optional[bool]:
        return super().led_read_bits(indexes)

    def led_read_states(self, indexes: tuple[int, int] | int) -> Optional[str]:
        return super().led_read_states(indexes)

    def led_read_binary(self, indexes: tuple[int, int] | int) -> Optional[bool]:
        return super().led_read_binary(indexes)

    def led_read_decimal(self, indexes: tuple[int, int] | int) -> Optional[int]:
        return super().led_read_decimal(indexes)


if __name__ == "__main__":
    port_names = tbu().get_all_ternion_port_names()
    port_name = port_names[0]
    cmd = TernionCommanderApi(port_name)
    # cmd.connect()
    try:
        while True:
            time.sleep(1)
            cmd.led_fade_one_shot(0, 0, 500)
    except KeyboardInterrupt:
        pass
