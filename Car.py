import interpolation
from math import pi, sin, cos


g = 9.81
airDens = 1.2


class Engine:
    def __init__(self, engineData, startRPM, maxRPM, method='engineMap'):
        if method == 'engineMap':
            engineMapFile = engineData
            self.torqueFunction = interpolation.map2Function(engineMapFile)

        elif method == 'engineParamaters':
            Tmax, Pmax = engineData
            self.torqueFunction = interpolation.paramaters2Function(Tmax, Pmax)

        self.startRPM = startRPM
        self.maxRPM = maxRPM
        self.method = method
        self.RPM = self.startRPM
        self.load = 1.0

    def torque(self):
        if self.load > 0:
            load = self.load
        else:
            load = 0
        if self.method == 'engineMap':
            torque = self.torqueFunction(self.RPM, load)
            return torque.tolist()[0]
        elif self.method == 'engineParamaters':
            torque = self.torqueFunction(self.RPM) * load
            return torque

    def getPower(self):
        power = self.torque() * self.RPM * 2 * pi / 60 / 1000
        return power


class Gearbox:
    def __init__(self, gears, fixedRatio, upshifting, downshifting, shiftTime):
        self.gears = gears
        self.fixedRatio = fixedRatio
        self.upshifting = upshifting
        self.downshifting = downshifting
        self.shiftTime = shiftTime  # should be bigger than dt

        self.autoShifting = True
        self.clutch = 1
        self.currentGear = 1
        self.currentShiftTime = 0

    def shiftUp(self):
        if (self.currentGear + 1) in self.gears:
            self.currentGear += 1
            self.currentShiftTime = self.shiftTime

    def shiftDown(self):
        if (self.currentGear - 1) in self.gears:
            self.currentGear -= 1
            self.currentShiftTime = self.shiftTime

    def getTotalRatio(self):
        return self.fixedRatio * self.gears[self.currentGear]


class Car:
    def __init__(self, configFile):
        config = dict()
        execfile(configFile, config)
        self.mass = config['mass']
        self.crossArea = config['crossArea']
        self.wheelDiameter = config['wheelDiameter']
        self.dragCoefficient = config['dragCoefficient']
        self.rollingResistanceCoefficient = config['rollingResistanceCoefficient']
        self.frictionResistanceCoefficient = config['frictionResistanceCoefficient']

        if config['engineMethod'] == 'engineMap':
            engineData = config['engineMap']
        elif config['engineMethod'] == 'engineParamaters':
            engineData = (config['maxTorque'], config['maxPower'])

        self.Engine = Engine(engineData, config['startRPM'], config['maxRPM'], method=config['engineMethod'])
        self.Gearbox = Gearbox(config['gears'], config['fixedRatio'], config['upshifting'], config['downshifting'], config['shiftTime'])

        self.startTime = 0.5
        self.currentStartTime = 0

        self.inclination = 0 #[deg]
        self.acceleration = 0
        self.velocity = 0
        self.path = 0

    def startOff(self):
        self.currentStartTime = self.startTime
        self.Engine.RPM = self.Engine.startRPM

    def getResistanceForce(self):
        if self.Engine.load < 0:
            brakes = abs(self.Engine.load)
        else:
            brakes = 0
        FBrakeing = cos(self.inclination * pi / 180) * brakes * self.mass * g * self.frictionResistanceCoefficient
        FRollingResistance = self.mass * g * self.rollingResistanceCoefficient
        FDrag = 0.5 * airDens * self.velocity ** 2 * self.crossArea * self.dragCoefficient
        if self.velocity > 0:
            sign = -1
        else:
            sign = +1
        return sign*(FBrakeing + FRollingResistance + FDrag)

    def getDrivingForce(self):
        torque = self.Engine.torque()
        outputTorque = torque * self.Gearbox.getTotalRatio() * self.Gearbox.clutch
        drivingForce = outputTorque / (0.5 * self.wheelDiameter)
        return drivingForce

    def getTotalForce(self):
        FDriving = self.getDrivingForce()
        FResistance = self.getResistanceForce()
        FInclination = sin(self.inclination * pi / 180) * self.mass * -g
        return FDriving + FInclination + FResistance

    def getVelocity(self):
        angularVelocity = self.Engine.RPM * (2 * pi / 60) / self.Gearbox.getTotalRatio()
        return angularVelocity * (0.5 * self.wheelDiameter)

    def update(self, dt):
        self.acceleration = self.getTotalForce() / (self.mass * 1.02)
        self.velocity = self.velocity + self.acceleration * dt
        self.path = self.path + self.velocity * dt

        if self.Gearbox.autoShifting:
            if self.Gearbox.upshifting <= self.Engine.RPM:
                self.Gearbox.shiftUp()
            if self.Gearbox.downshifting >= self.Engine.RPM:
                self.Gearbox.shiftDown()

        angularVelocity = self.velocity / (0.5 * self.wheelDiameter)
        if angularVelocity > 0 and self.currentStartTime <= 0:
            calculatedRPM = angularVelocity * self.Gearbox.getTotalRatio() / (2 * pi / 60)
            if calculatedRPM < self.Engine.maxRPM:
                self.Engine.RPM = calculatedRPM
            else:
                self.Engine.RPM = self.Engine.maxRPM
            self.velocity = self.getVelocity()

        if self.currentStartTime > 0:
            self.currentStartTime -= dt

        if self.Gearbox.currentShiftTime > 0:
            timeNow = self.Gearbox.currentShiftTime
            fullShiftTime = self.Gearbox.shiftTime
            self.Gearbox.clutch = 0.5*cos(pi * timeNow / fullShiftTime) + 0.5
            self.Gearbox.currentShiftTime -= dt
        else:
            self.Gearbox.clutch = 1






