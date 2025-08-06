# 1
high_control = xled.HighControlInterface("192.168.91.101", "0c:8b:95:7b:a1:55")
control = xled.ControlInterface("192.168.91.101", "0c:8b:95:7b:a1:55")

# 2
high_control = xled.HighControlInterface("192.168.91.102", "c0:49:ef:3b:72:e5")
control = xled.ControlInterface("192.168.91.102", "c0:49:ef:3b:72:e5")

# 3
high_control = xled.HighControlInterface("192.168.91.103", "c0:49:ef:3d:6d:f1")
control = xled.ControlInterface("192.168.91.103", "c0:49:ef:3d:6d:f1")

# 4 (trafohaus)
high_control = xled.HighControlInterface("192.168.91.151", "e8:31:cd:6b:c6:d5")
control = xled.ControlInterface("192.168.91.151", "e8:31:cd:6b:c6:d5")

# 5
high_control = xled.HighControlInterface("192.168.91.105", "c0:49:ef:13:d0:29")
control = xled.ControlInterface("192.168.91.105", "c0:49:ef:13:d0:29")

# 6
high_control = xled.HighControlInterface("192.168.91.106", "94:e6:86:a1:a5:a1")
control = xled.ControlInterface("192.168.91.106", "94:e6:86:a1:a5:a1")

# 7
high_control = xled.HighControlInterface("192.168.91.107", "94:e6:86:a1:a5:a9")
control = xled.ControlInterface("192.168.91.107", "94:e6:86:a1:a5:a9")

# 8
high_control = xled.HighControlInterface("192.168.91.108", "0c:8b:95:7b:ad:f9")
control = xled.ControlInterface("192.168.91.108", "0c:8b:95:7b:ad:f9")




--

# 1
high_control = xled.HighControlInterface("192.168.91.101", "0c:8b:95:7b:a1:55")
control = xled.ControlInterface("192.168.91.101", "0c:8b:95:7b:a1:55")

# 2
high_control = xled.HighControlInterface("192.168.91.102", "c0:49:ef:3b:72:e5")
control = xled.ControlInterface("192.168.91.102", "c0:49:ef:3b:72:e5")

# 3
high_control = xled.HighControlInterface("192.168.91.103", "c0:49:ef:3d:6d:f1")
control = xled.ControlInterface("192.168.91.103", "c0:49:ef:3d:6d:f1")

# 4 (trafohaus)
high_control = xled.HighControlInterface("192.168.91.151", "e8:31:cd:6b:c6:d5")
control = xled.ControlInterface("192.168.91.151", "e8:31:cd:6b:c6:d5")

# 5
high_control = xled.HighControlInterface("192.168.91.105", "c0:49:ef:13:d0:29")
control = xled.ControlInterface("192.168.91.105", "c0:49:ef:13:d0:29")

# 6
high_control = xled.HighControlInterface("192.168.91.106", "94:e6:86:a1:a5:a1")
control = xled.ControlInterface("192.168.91.106", "94:e6:86:a1:a5:a1")

# 7
high_control = xled.HighControlInterface("192.168.91.107", "94:e6:86:a1:a5:a9")
control = xled.ControlInterface("192.168.91.107", "94:e6:86:a1:a5:a9")

# 8
high_control = xled.HighControlInterface("192.168.91.108", "0c:8b:95:7b:ad:f9")
control = xled.ControlInterface("192.168.91.108", "0c:8b:95:7b:ad:f9")


high_control.turn_off()
high_control.turn_on()
control.set_mode('color')

num_leds = control.get_device_info()['number_of_led']
# Create an alternating color pattern
color1 = (0, 255, 0, 0)
color2 = (0, 0, 255, 0)
color_pattern = ldu.create_alternating_color_pattern(num_leds, color1, color2)
ldu.send_rt_frame(control, color_pattern)
time.sleep(1)
