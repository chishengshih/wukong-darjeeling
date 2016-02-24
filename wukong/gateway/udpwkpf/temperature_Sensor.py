import traceback
import time,sys
from udpwkpf import WuClass, Device
from twisted.internet import reactor
import pyupm_grove 
from math import log

PIN = 0 #Analog pin 0

class Temperature_sensor(WuClass):
    def __init__(self):
        self.ID = 1010
        self.temperature_sensor = pyupm_grove.GroveTemp(PIN)
        reactor.callLater(0.5,self.refresh)
        print "temperature sensor init!"

    def update(self,obj,pID,value):
        pass

    def refresh(self):
        self.celsius = self.temperature_sensor.value()
        print "WKPFUPDATE(Temperature): %d degrees Celsius" %self.celsius
        reactor.callLater(0.5,self.refresh)

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m = Temperature_sensor()
        self.addClass(m,1)
        self.obj_temperature_sensor = self.addObject(m.ID)
    
    def loop(self):
        print "WKPFUPDATE(Temperature): %d degrees Celsius" %self.m.celsius
        self.obj_temperature_sensor.setProperty(0, self.m.celsius)
        reactor.callLater(0.5,self.loop)

if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py 127.0.0.1 3000'
        sys.exit(-1)

d = MyDevice(sys.argv[1],sys.argv[2])

reactor.run()

