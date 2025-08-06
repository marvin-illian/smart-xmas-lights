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

#######################
# Example Trail Movie #
#######################
movie = ldu.generate_moving_led_movie_wrgb_trail(num_leds, (255, 0, 0))
ldu.play_movie(control, movie, frame_delay=0.01, loop=2)

########################
# Apply a single frame #
########################
# Create an alternating color pattern
color1 = (0, 255, 0, 0)
color2 = (0, 0, 255, 0)
color_pattern = ldu.create_alternating_color_pattern(num_leds, color1, color2)
ldu.send_rt_frame(control, color_pattern)
time.sleep(1)

# Turn off
high_control.turn_off()