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

def p2t(p, rpm):
    return p * 60 * 1000 / (rpm * 2 * pi)

def map2Function(FileName):
    x, y, z = readDAT_2D(FileName)
    f = interpolate.interp2d(x, y, z, kind='cubic')
    return f

def paramaters2Function(maxTorque, maxPower, rpm_max, type):
    rpm_tmax, tmax = maxTorque
    rpm_pmax, pmax = maxPower
    if type == 'diesel':
        rpm = np.array([-rpm_tmax / 2, rpm_tmax / 2, rpm_tmax, (rpm_tmax + rpm_pmax) / 2, rpm_pmax, rpm_max])
        torque = np.array([0, 0.8 * p2t(pmax, rpm_pmax), tmax, tmax, p2t(pmax, rpm_pmax), p2t(0.7 * pmax, rpm_max)])
    elif type == 'gasoline':
        rpm = np.array([-rpm_tmax / 3, rpm_tmax / 2, rpm_tmax, rpm_pmax, rpm_max])
        kmax = rpm_pmax / float(rpm_max)
        torque = np.array([0, 0.8 * p2t(pmax, rpm_pmax), tmax, p2t(pmax, rpm_pmax), p2t(kmax * pmax, rpm_max)])
    #coefficients = np.polyfit(rpm, torque, 4)
    #torque_function = np.poly1d(coefficients)
    torque_function = interpolate.interp1d(rpm, torque, kind='cubic')
    return torque_function
