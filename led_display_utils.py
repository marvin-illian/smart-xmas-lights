import xled
import time
import io
import random

def send_rt_frame(control, colors):
    """
    Send a real-time frame to the LED device.

    :param control: The ControlInterface object.
    :param colors: The list of colors (WRGB tuples) for each LED.
    """
    frame_data = bytearray()
    for color in colors:
        frame_data.extend(bytearray(color))

    frame = io.BytesIO(frame_data)
    control.set_rt_frame_socket(frame, version=3, leds_number=len(colors))

def play_movie(control, movie, frame_delay, loop=True):
    """
    Play a movie on the LED device.

    :param control: The ControlInterface object.
    :param movie: The list of frames, each frame is a list of WRGB tuples.
    :param frame_delay: Delay between frames in seconds.
    :param loop: If True, play the movie in a continuous loop. If False, play it once.
                 If an integer, play the movie that many times.
    """
    loop_count = 0

    while True:
        for frame in movie:
                (control, frame)
            time.sleep(frame_delay)

        if isinstance(loop, bool):
            if not loop:
                break
        elif isinstance(loop, int):
            loop_count += 1
            if loop_count >= loop:
                break

def generate_movie_alternating_color(num_leds, num_frames, color1, color2):

    """
    Generate a movie for LED lights alternating between two colors.

    :param num_leds: Number of LEDs in the strip.
    :param num_frames: Number of frames in the movie.
    :param color1: First color as an WRGB tuple (e.g., (255, 0, 0) for red).
    :param color2: Second color as an WRGB tuple (e.g., (0, 255, 0) for green).
    :return: List of frames, each frame is a list of WRGB tuples.
    """
    movie = []
    for frame_index in range(num_frames):
        frame = []
        for led_index in range(num_leds):
            if frame_index % 2 == 0:
                frame.append(color1 if led_index % 2 == 0 else color2)
            else:
                frame.append(color2 if led_index % 2 == 0 else color1)
        movie.append(frame)
    return movie

def generate_moving_led_movie_wrgb(num_leds, color, white_value=0):
    """
    Generate a movie where a single LED moves from the first to the last position
    using WRGB pattern.

    :param num_leds: Number of LEDs in the strip.
    :param color: Color of the moving LED as an RGB tuple (e.g., (255, 0, 0) for red).
    :param white_value: White value (0 to 255). 0 = full color, 1 = white only,
                        255 = white mixed with color.
    :return: List of frames, each frame is a list of WRGB tuples.
    """
    off_color = (0, 0, 0, 0)  # Color representing the turned-off state (WRGB)
    on_color = (white_value,) + color  # Active LED color with white component (WRGB)

    movie = []
    for i in range(num_leds):
        frame = [off_color] * num_leds  # Start with all LEDs turned off
        frame[i] = on_color  # Turn on the i-th LED
        movie.append(frame)

    return movie

def generate_moving_led_movie_wrgb_trail(num_leds, color, trail_length=49):
    """
    Generate a movie where a single LED moves from the first to the last position
    using WRGB pattern, with a trail of LEDs following it. The trail goes from 
    full RGB color to full white.

    :param num_leds: Number of LEDs in the strip.
    :param color: Color of the moving LED as an RGB tuple (e.g., (255, 0, 0) for red).
    :param trail_length: Length of the trail following the moving LED.
    :return: List of frames, each frame is a list of WRGB tuples.
    """
    off_color = (0, 0, 0, 0)  # Color representing the turned-off state (WRGB)

    movie = []
    for i in range(num_leds):
        frame = [off_color] * num_leds  # Start with all LEDs turned off

        # Set the color for the moving LED and its trail
        for t in range(trail_length + 1):
            led_position = i - t
            if 0 <= led_position < num_leds:
                if t == 0:
                    # The moving LED
                    frame[led_position] = (0,) + color  # Full color
                else:
                    # Trail LED transitions to white
                    fade_factor = t / trail_length
                    rgb_faded = tuple(int(c * (1 - fade_factor)) for c in color)
                    white_component = int(1 * fade_factor)
                    frame[led_position] = (white_component,) + rgb_faded

        movie.append(frame)

    return movie

def create_alternating_color_pattern(led_count, color1, color2):
    """
    Create an alternating color pattern for the given number of LEDs.

    :param led_count: The number of LEDs.
    :param color1: The first color (WRGB tuple).
    :param color2: The second color (WRGB tuple).
    :return: List of colors for each LED.
    """
    colors = []
    for i in range(led_count):
        if i % 2 == 0:
            colors.append(color1)  # Even-indexed LEDs
        else:
            colors.append(color2)  # Odd-indexed LEDs
    return colors

def create_color_pattern(led_count, pattern):
    """
    Create a color pattern for the given number of LEDs.

    :param led_count: The number of LEDs.
    :param pattern: The color pattern (list of WRGB tuples).
    :return: List of colors for each LED.
    """
    colors = []
    for i in range(led_count):
        colors.append(pattern[i % len(pattern)])
    return colors

def convert_pattern_to_frame(frame, on_color=(1, 255, 255, 255), off_color=(0, 0, 0, 0)):
    """
    Convert a frame into LED data.

    :param frame: List of strings representing the frame.
    :param on_color: RGB tuple representing the color when the LED is on.
    :param off_color: RGB tuple representing the color when the LED is off.
    :return: List of RGB tuples representing the LED data for the frame.
    """
    led_data = []
    for row in frame:
        for char in row:
            if char == '1':
                led_data.append(on_color)  # LED is on
            else:
                led_data.append(off_color)  # LED is off
    return led_data

def generate_inward_moving_pattern_zigzag(grid_width, grid_height, on_color=(0, 255, 255, 255), off_color=(0, 0, 0, 0)):
    """
    Generate a movie where the lit pattern moves inward on a zigzag-wired grid using WRGB.

    :param grid_width: Width of the grid.
    :param grid_height: Height of the grid.
    :param on_color: WRGB tuple for the 'on' state (e.g., (0, 255, 255, 255) for full color).
    :param off_color: WRGB tuple for the 'off' state (e.g., (0, 0, 0, 0) for off).
    :return: List of frames, each frame is a list of WRGB tuples.
    """

    def create_zigzag_row(row_num, inner_border):
        if row_num < inner_border or row_num >= grid_height - inner_border:
            return "1" * grid_width
        else:
            row = "1" * inner_border + "0" * (grid_width - 2 * inner_border) + "1" * inner_border
            return row if row_num % 2 == 0 else row[::-1]

    def convert_to_wrgb(string_frame):
        wrgb_frame = []
        for row in string_frame:
            for char in row:
                wrgb_frame.append(on_color if char == '1' else off_color)
        return wrgb_frame

    frames = []
    max_border = (min(grid_width, grid_height) + 1) // 2
    for border in range(max_border):
        string_frame = [create_zigzag_row(y, border) for y in range(grid_height)]
        wrgb_frame = convert_to_wrgb(string_frame)
        frames.append(wrgb_frame)

    return frames

def generate_outward_moving_pattern_zigzag(grid_width, grid_height, on_color=(0, 255, 255, 255), off_color=(0, 0, 0, 0)):
    """
    Generate a movie where the lit pattern moves outward on a zigzag-wired grid using WRGB.

    :param grid_width: Width of the grid.
    :param grid_height: Height of the grid.
    :param on_color: WRGB tuple for the 'on' state.
    :param off_color: WRGB tuple for the 'off' state.
    :return: List of frames, each frame is a list of WRGB tuples.
    """

    def create_zigzag_row(row_num, inner_border):
        if row_num < inner_border or row_num >= grid_height - inner_border:
            return "0" * grid_width
        else:
            row = "0" * inner_border + "1" * (grid_width - 2 * inner_border) + "0" * inner_border
            return row if row_num % 2 == 0 else row[::-1]

    def convert_to_wrgb(string_frame):
        wrgb_frame = []
        for row in string_frame:
            for char in row:
                wrgb_frame.append(on_color if char == '1' else off_color)
        return wrgb_frame

    frames = []
    max_border = (min(grid_width, grid_height) + 1) // 2
    for border in range(max_border - 1, -1, -1):
        string_frame = [create_zigzag_row(y, border) for y in range(grid_height)]
        wrgb_frame = convert_to_wrgb(string_frame)
        frames.append(wrgb_frame)

    return frames

def generate_precipitation_movie(grid_width, grid_height, color, num_frames=10, density=0.5):
    """
    Generate a movie simulating precipitation.

    :param grid_width: Width of the grid.
    :param grid_height: Height of the grid.
    :param color: WRGB tuple for the precipitation color.
    :param num_frames: Number of frames in the movie.
    :param density: Density of the precipitation (probability of a given LED being on in each frame).
    :return: List of frames, each frame is a list of WRGB tuples.
    """
    frames = []
    # Initialize precipitation state
    precipitation = [[False]*grid_width for _ in range(grid_height)]

    for _ in range(num_frames):
        # Move existing precipitation down
        for row in range(grid_height-1, 0, -1):
            precipitation[row] = list(precipitation[row-1])

        # Create new precipitation in the top row
        precipitation[0] = [random.random() < density for _ in range(grid_width)]

        # Create a frame from the precipitation state
        frame = [color if cell else (0, 0, 0, 0) for row in precipitation for cell in row]
        frames.append(frame)

    return frames

def create_single_color_pattern(led_count, color):
    """
    Create a pattern with all LEDs set to a single colour.

    :param led_count: Number of LEDs.
    :param color: The colour as a WRGB tuple.
    :return: A list of WRGB tuples, one for each LED.
    """
    return [color] * led_count