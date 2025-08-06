import xled
import time
import led_device_utils as ldu

###################
# Dict of devices #
###################
devices = {
    "1": {
        "ip": "192.168.91.101",
        "mac": "0c:8b:95:7b:a1:55",
    },
    "2": {
        "ip": "192.168.91.102",
        "mac": "c0:49:ef:3b:72:e5",
    },
    "3": {
        "ip": "192.168.91.103",
        "mac": "c0:49:ef:3d:6d:f1",
    },
    "4": {
        "ip": "192.168.91.107",
        "mac": "94:e6:86:a1:a5:a9",
    },
    "5": {
        "ip": "192.168.91.105",
        "mac": "c0:49:ef:13:d0:29",
    },
    "6": {
        "ip": "192.168.91.106",
        "mac": "94:e6:86:a1:a5:a1",
    },
    "7": {
        "ip": "192.168.91.108",
        "mac": "0c:8b:95:7b:ad:f9",
    },
}

####################
# Setup the device #
####################

h_ctrl = {}
ctrl = {}
for key, value in devices.items():
    h_ctrl[key] = xled.HighControlInterface(value["ip"], value["mac"])
    ctrl[key] = xled.ControlInterface(value["ip"], value["mac"])


def reset():
    for key, value in ctrl.items():
        h_ctrl[key].turn_off()
        h_ctrl[key].turn_on()
        ctrl[key].set_mode('color')

# Convergence effect
# Convergence effect that starts the light from the highest and lowest index lights simultaneously and runs it at such a speed that at the same time the light arrives at the mid-index light for each side of the mid-index so the lower ones and the upper ones only one light or star is turned on respectively and runs the trail effect once. The difficulty is to synchronize them such that they arrive at the same time at the mid-index light.
def convergence(mid_index=400*5, duration=20):
    """
    Creates a convergence effect on LEDs, where lights start from the highest and lowest
    indices and meet at the mid-index synchronously.
    
    :param mid_index: Index where the lights meet (default is 5).
    :param duration: Total duration of the effect in seconds (default is 20).
    """

    # Total number of total LEDs in the setup
    num_leds = sum([ctrl[key].get_device_info()['number_of_led'] for key in ctrl])
    half_duration = duration / 2  # Half duration for each side to converge

    # Calculate delay between each LED activation to synchronise at mid_index
    delay = half_duration / mid_index  # Time delay for turning on each LED

    # Iterate over indices from both ends toward the mid_index
    for step in range(mid_index + 1):
        lower_index = step
        upper_index = num_leds - 1 - step

        # Find ctrl for current lower and upper index
        # Return ctrl objects for the lower and upper index
        def find_ctrl(index):
            # Keep track of the cumulative LED count
            cumulative_count = 0
            for key in sorted(ctrl.keys(), key=lambda x: int(x)):
                device_led_count = ctrl[key].get_device_info()['number_of_led']
                # Check if index falls into this device's LED range
                if index < cumulative_count + device_led_count:
                    # Local index on this device
                    local_index = index - cumulative_count
                    return ctrl[key], local_index
                cumulative_count += device_led_count

            # If index is out of range (should not happen if indexing is correct)
            return None, None
        
        # Find the control interface for the lower and upper index
        lower_ctrl, lower_local_index = find_ctrl(lower_index)
        upper_ctrl, upper_local_index = find_ctrl(upper_index)


        # Set the colour for the lower index LED (warm white: (255,150,85,0)) using send_rt_frame
        if lower_index <= mid_index:
            lower_device_led_count = lower_ctrl.get_device_info()['number_of_led']
            # Create a frame with all LEDs off
            lower_frame = ldu.create_single_color_pattern(lower_device_led_count, (0,0,0,0))
            # Set the desired LED to warm white
            lower_frame[lower_local_index] = (255,150,85,0)  # (W,R,G,B)
            lower_ctrl.send_rt_frame(lower_frame)

        # Set the colour for the upper index LED (blue: (0,0,0,255)) using send_rt_frame
        if upper_index >= mid_index:
            upper_device_led_count = upper_ctrl.get_device_info()['number_of_led']
            # Create a frame with all LEDs off
            upper_frame = ldu.create_single_color_pattern(upper_device_led_count, (0,0,0,0))
            # Set the desired LED to blue
            upper_frame[upper_local_index] = (0,0,0,255)  # (W,R,G,B)
            upper_ctrl.send_rt_frame(upper_frame)

        time.sleep(delay)

    # Leave the LEDs on for the trail effect or reset after the effect
    time.sleep(1)
    reset()
