from scipy import interpolate
import numpy as np
from math import pi

def readDAT_2D(FileName):
    line = ' '
    x_axis = []
    y_axis = []
    map = []
    f = open(FileName, 'r')
    while line != '':
        line = f.readline()
        line = line.replace('\n','')
        if line == '# y axis':
            line = f.readline()
            args = line.split(' ')
            args = filter(lambda a: a != '', args)
            y_axis = [float(i) for i in args]
            continue
        if line == '# x axis':
            line = f.readline()
            args = line.split(' ')
            args = filter(lambda a: a != '', args)
            x_axis = [float(i) for i in args]
            continue
        if line == '# map':
            break
    while line != '':
        line = f.readline()
        line = line.replace('\n','')
        args = line.split(' ')
        args = filter(lambda a: a != '', args)
        if len(args) > 1:
            map.append([float(i) for i in args])
    f.close()
    return x_axis, y_axis, map

class Function:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self, x, y):
        print x*self.a
        print y*self.b

def map2Function(FileName):
    x, y, z = readDAT_2D(FileName)
    print x
    print z[-1]
    f = interpolate.interp2d(x, y, z, kind='cubic')
    return f

def paramaters2Function(maxTorque, maxPower):
    rpm_tmax, tmax = maxTorque
    rpm_pmax, pmax = maxPower
    rpm = np.array([-rpm_tmax/2, rpm_tmax/2, rpm_tmax, rpm_pmax])
    torque = np.array([0, pmax * 60 * 1000 / (rpm_pmax * 2 * pi), tmax, pmax * 60 * 1000 / (rpm_pmax * 2 * pi)])
    coefficients = np.polyfit(rpm, torque, 4)
    torque_function = np.poly1d(coefficients)
    return torque_function
