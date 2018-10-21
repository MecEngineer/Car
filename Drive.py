import Car
import matplotlib.pyplot as plt
from math import *
import copy as cp
from PID import PID

def inclination(x):
    if 200 < x < 1800:
        #path = 50 * cos(pi * (x-1000) / 200) + 50
        tg = -pi * sin(pi * (x-0) / 200) / 16
        inclination_angle = (180/pi)*atan(tg)
        return inclination_angle
    else:
        return 0


audi = Car.Car('car_koleos.conf')
dt = 0.1
time = []
history = []
pid = PID(2.0, 1.5, 0.1, setpoint=100/3.6)
pid.output_limits = (-1, 1)
audi.startOff()
for i in range(2000):
    #audi.inclination = inclination(audi.path)
    #print audi.velocity*3.6
    #gas = pid(audi.velocity)
    #audi.Engine.load = gas

    history.append(cp.deepcopy(audi))
    time.append(i*dt)
    audi.update(dt)


plt.figure(0)
plt.title('Gear vs. time [s]')
plt.plot(time, [car.Gearbox.currentGear for car in history], '-')
plt.figure(1)
plt.title('Engine RPM vs. time [s]')
plt.plot(time, [car.Engine.RPM for car in history], '-')
plt.figure(2)
plt.title('Engine output power [kW] vs. time [s]')
plt.plot(time, [car.Engine.getPower() for car in history], '-')
plt.figure(3)
plt.title('Car velocity [km/h] vs. time [s]')
plt.plot(time, [car.velocity*3.6 for car in history], '-')
plt.figure(4)
plt.title('Resultant force [N] vs. time [s]')
plt.plot(time, [car.getTotalForce() for car in history], '-')
#plt.plot([car.path for car in history], [car.inclination for car in history], '-')
plt.figure(5)
plt.plot(time, [car.Engine.load for car in history], '-')
#plt.show()



# print Engine characteristics
RPMs = range(750, car.Engine.maxRPM, 10)
plt.figure(5)
plt.title('Engine characteristics')
plt.suptitle('Torque [Nm] and Power [kW] vs. Engine speed [RPM]')
for j in range(0,11):
    audi.Engine.load = j/10.0
    torque = []
    power = []
    for i in RPMs:
        audi.Engine.RPM = i
        torque.append(audi.Engine.torque())
        power.append(audi.Engine.getPower())
    plt.plot(RPMs, torque,'b-')
    plt.plot(RPMs, power,'r-')
plt.show()

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