import xled
import time
import led_display_utils as ldu

####################
# Setup the device #
####################

# Discover the device
discovered_device = xled.discover.discover()
print('IP:', discovered_device.ip_address)
print('MAC:', discovered_device.hw_address)

# Create control interfaces
high_control = xled.HighControlInterface(discovered_device.ip_address, discovered_device.hw_address)
control = xled.ControlInterface(discovered_device.ip_address, discovered_device.hw_address)

# Number of LEDs
num_leds = control.get_device_info()['number_of_led']
print('Number of LEDs:', num_leds)

# Turn on
high_control.turn_on()
control.set_mode('color')
time.sleep(1)

# Set the device to real-time mode
control.set_mode('rt')
print('Control mode:', control.get_mode()['mode'])

########################
# Apply a single frame #
########################
# Create an alternating color pattern
color1 = (0, 255, 0, 0)
color2 = (0, 0, 255, 0)
color_pattern = ldu.create_alternating_color_pattern(num_leds, color1, color2)
ldu.send_rt_frame(control, color_pattern)
time.sleep(1)

#######################
# Bit pattern example #
#######################
# Bit pattern (10x10 grid)
pattern = [
    "1000000001",  # First row
    "0100000010",  # Second row
    "0010000100",  # Third row
    "0001001000",  # Fourth row
    "0000110000",  # Fifth row
    "0000110000",  # Sixth row
    "0001001000",  # Seventh row
    "0010000100",  # Eighth row
    "0100000010",  # Ninth row
    "1000000001"   # Tenth row
]
led_data = ldu.convert_pattern_to_frame(pattern)
# Send the frame to the device
ldu.send_rt_frame(control, led_data)
time.sleep(1)

####################
# Play a LED movie #
####################
num_frames = 2  # Number of frames in the movie
color1 = (0, 255, 0, 0)
color2 = (1, 255, 255, 255)
movie = ldu.generate_movie_alternating_color(num_leds, num_frames, color1, color2)
ldu.play_movie(control, movie, frame_delay=0.5, loop=3)

#######################
# Example Trail Movie #
#######################
movie = ldu.generate_moving_led_movie_wrgb_trail(num_leds, (255, 0, 0))
ldu.play_movie(control, movie, frame_delay=0.01, loop=2)

######################
# Grid example movie #
######################
grid_width, grid_height = 10, 10
movie = ldu.generate_outward_moving_pattern_zigzag(grid_width, grid_height)
ldu.play_movie(control, movie, frame_delay=0.1, loop=3)
movie = ldu.generate_inward_moving_pattern_zigzag(grid_width, grid_height)
ldu.play_movie(control, movie, frame_delay=0.1, loop=3)

##########################
# Simulate Precipitation #
##########################

# light rain
rain_color = (0, 0, 255, 255)  # Blue for rain
rain_movie = ldu.generate_precipitation_movie(grid_width=10, grid_height=10, color=rain_color, num_frames=50, density=0.05)
ldu.play_movie(control, rain_movie, frame_delay=0.1, loop=1)

# heavy rain
rain_color = (0, 0, 255, 255)  # Blue for rain
rain_movie = ldu.generate_precipitation_movie(grid_width=10, grid_height=10, color=rain_color, num_frames=50, density=0.15)
ldu.play_movie(control, rain_movie, frame_delay=0.1, loop=1)

snow_color = (0, 255, 255, 255)  # White for snow
snow_movie = ldu.generate_precipitation_movie(grid_width=10, grid_height=10, color=snow_color, num_frames=20, density=0.15)
ldu.play_movie(control, snow_movie, frame_delay=0.25, loop=1)

# Turn off
high_control.turn_off()