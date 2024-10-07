set COM=%1

esptool --chip esp32 --port %COM% erase_flash
esptool --chip esp32 --port %COM% --baud 460800 write_flash -z 0x1000 ../ESP32_GENERIC-20240602-v1.23.0.bin
ampy --port %COM% --delay 1.0 reset
ampy --port %COM% put  .\lib\ lib
ampy --port %COM% put  .\main.py 

echo "listing"
ampy --port %COM% ls 
ampy --port %COM% ls lib
rem ampy --port %COM% run ..\bilTest.py
rem timeout 2
ampy --port %COM% run  .\led_pwm_sine.py