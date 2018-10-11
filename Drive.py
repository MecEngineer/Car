import Car
import matplotlib.pyplot as plt
from math import *
import copy as cp
from PID import PID

def inclination(x):
    if 200 < x < 1000:
        #path = 50 * cos(pi * (x-1000) / 200) + 50
        tg = -pi * sin(pi * (x-0) / 200) / 16
        inclination_angle = (180/pi)*atan(tg)
        return inclination_angle
    else:
        return 0


audi = Car.Car('car.conf')
dt = 0.01
time = []
history = []
pid = PID(2.0, 1.5, 0.1, setpoint=100/3.6)
pid.output_limits = (-1, 1)
audi.startOff()
for i in range(20000):
    audi.inclination = inclination(audi.path)
    print audi.velocity*3.6
    gas = pid(audi.velocity)
    audi.Engine.load = gas

    history.append(cp.deepcopy(audi))
    time.append(i*dt)
    audi.update(dt)


plt.figure(0)
plt.plot(time, [car.Gearbox.currentGear for car in history], '-')
plt.figure(1)
plt.plot(time, [car.Engine.RPM for car in history], '-')
plt.figure(2)
plt.plot(time, [car.Engine.getPower() for car in history], '-')
plt.figure(3)
plt.plot(time, [car.getVelocity()*3.6 for car in history], '-')
plt.plot(time, [car.velocity*3.6 for car in history], '-')
plt.figure(4)
#plt.plot(time, [car.getTotalForce() for car in history], '-')
plt.plot([car.path for car in history], [car.inclination for car in history], '-')
plt.figure(5)
plt.plot(time, [car.Engine.load for car in history], '-')
plt.show()


'''
# print Engine characteristics
RPMs = range(750, car.Engine.maxRPM, 10)
torque = []
power = []
for i in RPMs:
    audi.Engine.RPM = i
    torque.append(audi.Engine.torque())
    power.append(audi.Engine.getPower())
plt.figure(5)
plt.plot(RPMs, torque,'-')
plt.plot(RPMs, power,'-')
plt.show()
#'''
'''

# print GEARBOX characteriscs
RPMs = range(1000, car.Engine.maxRPM, 100)
speeds = []
audi.Gearbox.currentGear = 1
for i in range(8):
    speed = []
    for j in RPMs:
        audi.Engine.RPM = j
        speed.append(audi.getVelocity()*3.6)
    speeds.append(speed)
    audi.Gearbox.shiftUp()

for speed in speeds:
    plt.plot(RPMs, speed, '-')
plt.show()
'''