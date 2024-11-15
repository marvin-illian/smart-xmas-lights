import xled
import time
import io
import random

class LEDDisplay:
    def __init__(self, ip_address, hw_address):
        """
        Initialize the LEDDisplay with control interfaces.

        :param ip_address: IP address of the LED light string.
        :param hw_address: MAC address of the LED light string.
        """
        self.ip_address = ip_address
        self.hw_address = hw_address
        self.control = xled.ControlInterface(ip_address, hw_address)
        self.high_control = xled.HighControlInterface(ip_address, hw_address)
        self.num_leds = self.control.get_device_info()['number_of_led']
        self.current_mode = None

    def turn_on(self):
        """
        Turn on the LED device and set it to real-time mode.
        """
        self.high_control.turn_on()
        self.control.set_mode('rt')
        self.current_mode = 'rt'

    def turn_off(self):
        """
        Turn off the LED device.
        """
        self.high_control.turn_off()
        self.current_mode = None

    def send_rt_frame(self, colors):
        """
        Send a real-time frame to the LED device.

        :param colors: The list of colors (WRGB tuples) for each LED.
        """
        frame_data = bytearray()
        for color in colors:
            frame_data.extend(bytearray(color))
        frame = io.BytesIO(frame_data)
        self.control.set_rt_frame_socket(frame, version=3, leds_number=len(colors))

    def play_movie(self, movie, frame_delay, loop=True):
        """
        Play a movie on the LED device.

        :param movie: The list of frames, each frame is a list of WRGB tuples.
        :param frame_delay: Delay between frames in seconds.
        :param loop: If True, play the movie in a continuous loop. If False, play it once.
                     If an integer, play the movie that many times.
        """
        loop_count = 0

        while True:
            for frame in movie:
                self.send_rt_frame(frame)
                time.sleep(frame_delay)

            if isinstance(loop, bool):
                if not loop:
                    break
            elif isinstance(loop, int):
                loop_count += 1
                if loop_count >= loop:
                    break

    def generate_movie_alternating_color(self, num_frames, color1, color2):
        """
        Generate a movie for LED lights alternating between two colors.

        :param num_frames: Number of frames in the movie.
        :param color1: First color as a WRGB tuple.
        :param color2: Second color as a WRGB tuple.
        :return: List of frames, each frame is a list of WRGB tuples.
        """
        movie = []
        for frame_index in range(num_frames):
            frame = []
            for led_index in range(self.num_leds):
                if frame_index % 2 == 0:
                    frame.append(color1 if led_index % 2 == 0 else color2)
                else:
                    frame.append(color2 if led_index % 2 == 0 else color1)
            movie.append(frame)
        return movie

    def generate_moving_led_movie_wrgb(self, color, white_value=0):
        """
        Generate a movie where a single LED moves from the first to the last position
        using WRGB pattern.

        :param color: Color of the moving LED as an RGB tuple (e.g., (255, 0, 0) for red).
        :param white_value: White value (0 to 255). 0 = full color, 1 = white only,
                            255 = white mixed with color.
        :return: List of frames, each frame is a list of WRGB tuples.
        """
        off_color = (0, 0, 0, 0)  # WRGB off
        on_color = (white_value,) + color  # WRGB on

        movie = []
        for i in range(self.num_leds):
            frame = [off_color] * self.num_leds
            frame[i] = on_color
            movie.append(frame)

        return movie

    def generate_moving_led_movie_wrgb_trail(self, color, trail_length=49):
        """
        Generate a movie where a single LED moves from the first to the last position
        using WRGB pattern, with a trail of LEDs following it. The trail transitions
        from full RGB color to full white.

        :param color: Color of the moving LED as an RGB tuple (e.g., (255, 0, 0) for red).
        :param trail_length: Length of the trail following the moving LED.
        :return: List of frames, each frame is a list of WRGB tuples.
        """
        off_color = (0, 0, 0, 0)  # WRGB off

        movie = []
        for i in range(self.num_leds):
            frame = [off_color] * self.num_leds

            for t in range(trail_length + 1):
                led_position = i - t
                if 0 <= led_position < self.num_leds:
                    if t == 0:
                        frame[led_position] = (0,) + color  # Moving LED
                    else:
                        fade_factor = t / trail_length
                        rgb_faded = tuple(int(c * (1 - fade_factor)) for c in color)
                        white_component = int(1 * fade_factor)
                        frame[led_position] = (white_component,) + rgb_faded

            movie.append(frame)

        return movie

    def create_alternating_color_pattern(self, color1, color2):
        """
        Create an alternating color pattern for the LED strip.

        :param color1: First color as a WRGB tuple.
        :param color2: Second color as a WRGB tuple.
        :return: List of colors for each LED.
        """
        colors = []
        for i in range(self.num_leds):
            if i % 2 == 0:
                colors.append(color1)
            else:
                colors.append(color2)
        return colors

    def create_color_pattern(self, pattern):
        """
        Create a repeating color pattern for the LED strip.

        :param pattern: The color pattern as a list of WRGB tuples.
        :return: List of colors for each LED.
        """
        colors = []
        for i in range(self.num_leds):
            colors.append(pattern[i % len(pattern)])
        return colors