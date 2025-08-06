from config import LIGHT_STRINGS
from led_display_utils import LEDDisplay
import time
from xled.discover import xdiscover

class LightStringManager:
    def __init__(self, discovery_timeout=3):
        """
        Initialize the LightStringManager by creating LEDDisplay instances for each light string.
        :param discovery_timeout: Time in seconds to wait for device discovery (default 10 seconds).
        """
        self.light_strings = []
        self.discovery_timeout = discovery_timeout
        self.initialize_light_strings()

    def initialize_light_strings(self):
        """
        Initialize all LEDDisplay instances based on the configuration.
        Dynamically discover devices and match them with MAC addresses.
        Continues searching upon exceptions until the timeout is reached.
        """
        discovered_devices = []
        start_time = time.time()

        print("Starte Geräteentdeckung...")

        while time.time() - start_time < self.discovery_timeout:
            try:
                # Start discovery
                for response in xdiscover():
                    device = {
                        'ip_address': response.ip_address,
                        'mac_address': response.hw_address.lower(),  # Ensure MAC address is in lowercase
                    }
                    # Avoid duplicates
                    if device not in discovered_devices:
                        discovered_devices.append(device)
                        print(f"Gerät gefunden: {response.hw_address} ({response.ip_address})")
            except Exception as e:
                if str(e) == "Unknown event":
                    pass  # Ignore the exception and continue
                else:
                    print(f"Fehler bei der Geräteentdeckung: {e}")
            # time.sleep(0.5)  # Wait before next discovery attempt

        if not discovered_devices:
            print("Keine Geräte gefunden.")
            return

        # Create a mapping from MAC address to IP address
        mac_to_ip = {device['mac_address']: device['ip_address'] for device in discovered_devices}

        # Initialize LEDDisplay instances based on MAC addresses
        for light in LIGHT_STRINGS:
            mac_address = light['mac_address'].lower()  # Ensure MAC address is in lowercase
            ip_address = mac_to_ip.get(mac_address)

            if ip_address:
                led_display = LEDDisplay(ip_address, mac_address)
                self.light_strings.append({
                    'position': light.get('position', None),
                    'mac_address': mac_address,
                    'led_display': led_display
                })
            else:
                print(f"Gerät mit MAC-Adresse {mac_address} nicht gefunden.")

        # Sort light strings based on position
        self.light_strings.sort(key=lambda x: x['position'])

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