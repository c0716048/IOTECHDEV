# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:06:18 2013

@author: Hugo Silva

EMG trigger:
In this example, the muscles can be used to turn the led on.
Every time the EMG signal is higher than a defined threshold, the led turns on, otherwise is off.
 
"""
import time

import libardrone
drone = libardrone.ARDrone()
time.sleep(2)

import BITalino #BITalino API
import numpy

#call the BITalino API
device = BITalino.BITalino()

#macAddress= "98:d3:31:b1:84:08" # '/dev/tty.bitalino-DevB-1' # Board Hugo Silva
#macAddress =  "98:D3:31:B0:8E:F1"
macAddress =  '/dev/tty.bitalino-DevB' # "98:D3:31:B2:BB:22" # OrBIT
SamplingRate = 1000
nFrames = 200 #number of samples to read
thOnset = .35 #threshold defined to turn the led on
thEmergency = 0.75 

#connect do BITalino device
device.open(macAddress, SamplingRate = SamplingRate)
time.sleep(2)

#start acquisition on analog channel 0 (EMG)
device.start([0, 1, 2, 3])
time.sleep(2)
print "START"
acquireLoop = 0

airborne = False
onset = False

emergency = False

t0 = 0

try:
    while True:
        #read samples
        dataAcquired = device.read(nFrames)
        
        BTN = numpy.mean(dataAcquired[1,:])
        if BTN < thEmergency:
            if t0 == 0:
                t0 = time.time()
            elif (time.time()-t0) > 5:
                break
        else:
            t0 = 0
        
        if BTN < thEmergency and not emergency:
            drone.at(libardrone.at_ref, False, True)
            time.sleep(.1)
            drone.land()
            print 'emergency toggled'
            emergency = True
            continue
        elif BTN >= thEmergency and emergency:
            emergency = False
            continue
        
        #get EMG signal
        EMG = dataAcquired[-4,:]
        ACCX = dataAcquired[-3, :]
        ACCY = dataAcquired[-2, :]
        ACCZ = dataAcquired[-1, :]
        #center the EMG signal baseline at zero, by subtracting its mean
        #calculate the mean value of the absolute of the EMG signal
        value = numpy.mean(numpy.diff(EMG))
        #print value, stdev
        if value >= thOnset and not onset:
            onset = True
            airborne = not airborne
            print 'takeoff' if airborne else 'land'
            drone.takeoff() if airborne else drone.land()
            #drone.at(libardrone.at_ref, True, True) if airborne else drone.land()
        else:
            onset = False
        
        # Todos os valores para comparação estão antes das mesmas. Agora, o que acontece é o seguinte: caso os valores lidos
        # do acelarómetro estejam acima do threshold, ele detecta e executa a função correspondente. Caso não estejam,
        # (mão na posição inicial de repouso) ele apenas faz hovering, tal como se fosse um joystick.
        
        
        value_z = numpy.mean(ACCZ)
        value_y = numpy.mean(ACCY)
        value_x = numpy.mean(ACCX)
        #print value_x, value_y, value_z
        if value_x < 250 or value_x > 300 or value_y < 220 or value_y > 300:
            if value_y > 300:
                print 'forward'
                drone.move_forward()
            elif value_y < 220: 
                print 'backward'
                drone.move_backward()
                
            if value_x < 250:
                print 'left'
                drone.turn_left()
            elif value_x > 300: 
                print 'right'
                drone.turn_right()
        else:
            pass
            drone.hover()

finally:
    pass

drone.land()
time.sleep(1)
drone.halt()
    
#stop acquisition  
device.stop()
#diconnect device
device.close()

del device
del drone

print "STOP"
        
