# rshell -> host side shell emulator using repl over serial
#installing drivers is essential!
import time, machine
# setup webrepl import webrepl_setup 
# variable for controlling GPIO pins
pin = machine.Pin(2, machine.Pin.OUT)

while True:
    pin.on()
    time.sleep_ms(500)
    pin.off()
    time.sleep_ms(500)
    # 3 times ENTER in repl
    #
    #

# there can be files in flash memory 
f = open('data.txt', 'w') # wb/rb - binary open with write
f.write('some data')
# f.read()
f.close()

with open('data.txt','w') as f:
    f.write(str("any string"))

# for filesystem manipulation use
import os
os.listdir()
os.mkdir('henlo')
os.remove('data.txt')

# script execution (if exist):
# > boot.py
# > main.py

# networking
import network
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active() # is on?
ap_if.ifconfig() # read settings ('i.p.a.d.', '255.255.255.0', 'gate.way.ip.add', 'd.n.s.a')
ap_if.active(False) # disable network access point
sta_if.active(True)
sta_if.connect('ESSID', 'PASS')
sta_if.isconnected()
sta_if.ifconfig() # check ip address

# add to boot.py to auto connect
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('<essid>', '<password>')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

### SOCKET PROGRAMMING ###
import socket
addr_info=socket.getaddrinfo("towel.blinkenlights.nl", 23) # resolve address
addr=addr_info[0][-1] # use 1st valid address
s=socket.socket() # create socket
s.connect(addr)

### HTTP GET request ###
def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr=socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data=s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
http_get('http://micropython.org/ks/test.html')

### simple HTTP server ###
import machine
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

### pin control ###
import machine
# only GPIO pins:  0, 2, 4, 5, 12, 13, 14, 15, and 16 can be used
pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
pin.value()
machine.Pin(0, machine.Pin.OUT)
pin.on()
pin.off()
pin.value(1)
pin.value(0)
# interrupts must be short, cannot allocate memory
from machine import Pin
p0 = Pin(0, Pin.IN)
p2 = Pin(2, Pin.IN)
p0.irq(trigger=Pin.IRQ_FALLING, handler=callback)
p2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
# PWM:: pins 0, 2, 4, 5, 12, 13, 14, 15, all share the same frequency 1Hz-1kHz
p12=machine.Pin(12)
pwm12=machine.Pin(12)
pwm12.freq(500)
pwm12.duty(512)
pwm12.deinit()
# pulsing led
led = machine.PWM(machine.Pin(2), freq=1000)
import time, math
def pulse(l, t):
    for i in range(20):
        l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(t)
# servo
servo = machine.PWM(machine.Pin(12), freq=50)
servo.duty(40) # min
servo.duty(115) # max
servo.duty(77) # mid
# ADC pin (1 on esp 8266)
adc = machine.ADC(0)
adc.read() # 10bit, 0-1V input!!!!

### POWER CONTROL ###
machine.freq(160000000) # read / write, by default 80MHz
# deep sleep: jumper GPIO16 -> RST pin
import machine
# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
# set RTC.ALARM0 to fire after 10 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 10000)
# put the device to sleep
machine.deepsleep()
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')
