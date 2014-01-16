import matplotlib.pyplot as plt

motorControlTime = []
motorControlBase = []
motorControlBaseSet = []
motorControlBias = []
motorControlBiasSet = []

def motorControl(line):
    motorControlTime.append(float(line[1]))
    motorControlBase.append(float(line[2]))
    motorControlBaseSet.append(float(line[3]))
    motorControlBias.append(float(line[4]))
    motorControlBiasSet.append(float(line[5]))

turnToTargetTime = []
turnToTargetTheta = []
turnToTargetThetaSet = []
turnToTargetThetaErrInt = []
turnToTargetBias = []

def turnToTarget(line):
    turnToTargetTime.append(float(line[1]))
    turnToTargetTheta.append(float(line[2]))
    turnToTargetThetaSet.append(float(line[3]))
    turnToTargetThetaErrInt.append(float(line[4]))
    turnToTargetBias.append(float(line[5]))

controlPeriodicTime = []
controlPeriodicX = []
controlPeriodicY = []
controlPeriodicTheta = []
controlPeriodicDistErr = []
controlPeriodicSetAngle = []
controlPeriodicAngleErr = []
controlPeriodicState = []

def controlPeriodic(line):
    controlPeriodicTime.append(float(line[1]))
    controlPeriodicX.append(float(line[2]))
    controlPeriodicY.append(float(line[3]))
    controlPeriodicTheta.append(float(line[4]))
    controlPeriodicDistErr.append(float(line[5]))
    controlPeriodicSetAngle.append(float(line[6]))
    controlPeriodicAngleErr.append(float(line[7]))
    controlPeriodicState.append(float(line[8])* 50)

stateEstimationTime = []
stateEstimationX = []
stateEstimationY = []
stateEstimationTheta = []

def stateEstimation(line):
    stateEstimationTime.append(float(line[1]))
    stateEstimationX.append(float(line[2]))
    stateEstimationY.append(float(line[3]))
    stateEstimationTheta.append(float(line[4]))

goToTargetTime = []
goToTargetDistErr = []
goToTargetAngleErr = []
goToTargetAngleErrInt = []
goToTargetBase = []
goToTargetBias = []

def goToTarget(line):
    goToTargetTime.append(float(line[1]))
    goToTargetDistErr.append(float(line[2]))
    goToTargetAngleErr.append(float(line[3]))
    goToTargetAngleErrInt.append(float(line[4]))
    goToTargetBase.append(float(line[5]))
    goToTargetBias.append(float(line[6]))

files = {
    '_motor_control': motorControl,
    '_control_turnToTarget' : turnToTarget,
    'control_periodic' : controlPeriodic,
    'stateEstimation' : stateEstimation,
    '_control_goToTarget':goToTarget
}

def importFile(fName):
    openFiles = {}

    with open(fName) as fileIn:
        for line in fileIn:
            splitLine = line.split(',')
            lineType = splitLine[0]
            func = files[lineType]
            func(splitLine)



if __name__ == '__main__':
    fName = 'stepResponse.txt'
    importFile(fName)

    p1, = plt.plot(motorControlTime, motorControlBase)
    p2, = plt.plot(motorControlTime, motorControlBaseSet)

    plt.legend([p1,p2], ['Base','BaseSet'])

    plt.figure()

    p1, = plt.plot(motorControlTime, motorControlBias)
    p2, = plt.plot(motorControlTime, motorControlBiasSet)
    p3, = plt.plot(controlPeriodicTime, controlPeriodicState)

    plt.legend([p1,p2], ['Bias','BiasSet'])

    plt.figure()

    p1, = plt.plot(turnToTargetTime, turnToTargetTheta)
    p2, = plt.plot(turnToTargetTime, turnToTargetThetaSet)
    p3, = plt.plot(turnToTargetTime, turnToTargetThetaErrInt)
    p4, = plt.plot(turnToTargetTime, turnToTargetBias)

    plt.legend([p1,p2,p3,p4], ['Theta','Set Point','ThetaErrInt','bias'])

    plt.figure()

    p1, = plt.plot(stateEstimationTime, stateEstimationX)
    p2, = plt.plot(stateEstimationTime, stateEstimationY)
    p3, = plt.plot(stateEstimationTime, stateEstimationTheta)

    plt.legend([p1, p2, p3], ['X', 'Y', 'Theta'])

    plt.figure()
    p1, = plt.plot(stateEstimationX, stateEstimationY)

    plt.figure()
    p1, = plt.plot(goToTargetTime, goToTargetDistErr)
    p2, = plt.plot(goToTargetTime, goToTargetAngleErr)
    p3, = plt.plot(goToTargetTime, goToTargetBase)
    p4, = plt.plot(goToTargetTime, goToTargetBias)
    p5, = plt.plot(goToTargetTime, goToTargetAngleErrInt)
    plt.legend([p1,p2,p3,p4, p5], ['DistErr','AngleErr','Base','Bias', 'Angle Error It'])


    plt.show()
    