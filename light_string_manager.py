from config import LIGHT_STRINGS
from led_display_utils import LEDDisplay
import time

class LightStringManager:
    def __init__(self):
        """
        Initialize the LightStringManager by creating LEDDisplay instances for each light string.
        """
        self.light_strings = []
        self.initialize_light_strings()

    def initialize_light_strings(self):
        """
        Initialize all LEDDisplay instances based on the configuration.
        """
        for light in LIGHT_STRINGS:
            led_display = LEDDisplay(light['ip_address'], light['mac_address'])
            self.light_strings.append({
                'name': light['name'],
                'position': light.get('position', None),  # Optional position for ordering
                'led_display': led_display
            })

    def turn_on_all(self):
        """
        Turn on all managed LED light strings.
        """
        for light in self.light_strings:
            light['led_display'].turn_on()

    def turn_off_all(self):
        """
        Turn off all managed LED light strings.
        """
        for light in self.light_strings:
            light['led_display'].turn_off()

    def send_frame_to_all(self, colors):
        """
        Send the same real-time frame to all LED light strings.

        :param colors: The list of colors (WRGB tuples) for each LED.
        """
        for light in self.light_strings:
            light['led_display'].send_rt_frame(colors)

    def run_converging_effect(self, target_index, base_brightness=0.5, duration=10, fps=30):
        """
        Start a converging light effect where the light intensities move towards a target light string.

        :param target_index: Index of the target light string in LIGHT_STRINGS.
        :param base_brightness: Base brightness level (between 0 and 1).
        :param duration: Total duration of the effect in seconds.
        :param fps: Frames per second.
        """
        total_steps = int(duration * fps)
        num_devices = len(self.light_strings)
        left_indices = list(range(0, target_index))
        right_indices = list(range(num_devices - 1, target_index, -1))
        brightness_levels = [base_brightness] * num_devices

        for step in range(total_steps):
            progress = step / total_steps

            # Update brightness for left side
            for i in left_indices:
                if len(left_indices) == 0:
                    relative_position = 0
                else:
                    relative_position = (target_index - i) / len(left_indices)
                if progress >= relative_position:
                    brightness_levels[i] = base_brightness + (1.0 - base_brightness) * (
                        (progress - relative_position) / (1.0 - relative_position)
                    )

            # Update brightness for right side
            for i in right_indices:
                if len(right_indices) == 0:
                    relative_position = 0
                else:
                    relative_position = (i - target_index) / len(right_indices)
                if progress >= relative_position:
                    brightness_levels[i] = base_brightness + (1.0 - base_brightness) * (
                        (progress - relative_position) / (1.0 - relative_position)
                    )

            # Ensure target light string stays at full brightness
            brightness_levels[target_index] = 1.0

            # Send brightness levels to each light string
            for i, light in enumerate(self.light_strings):
                frame = self.create_brightness_frame(light['led_display'].num_leds, brightness_levels[i])
                light['led_display'].send_rt_frame(frame)

            time.sleep(1 / fps)

    def create_brightness_frame(self, num_leds, brightness):
        """
        Create a frame with the specified brightness.

        :param num_leds: Number of LEDs in the light string.
        :param brightness: Brightness level between 0 and 1.
        :return: List of WRGB tuples representing the LED colors.
        """
        color = (
            0,  # White component
            int(255 * brightness),  # Red
            int(223 * brightness),  # Green
            int(191 * brightness)   # Blue
        )
        frame = [color] * num_leds
        return frame