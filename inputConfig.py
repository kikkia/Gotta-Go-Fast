import pyxinput


controllerSet = pyxinput.vController()
controllerRead = pyxinput.rController(1)

def gunIt():
    controllerSet.set_value('TriggerR', 1.0)
    controllerSet.set_value('TriggerL', 0.0)

def slow():
    controllerSet.set_value('TriggerR', 0.3)
    controllerSet.set_value('TriggerL', 0.0)

def hardBrake():
    controllerSet.set_value('TriggerL', 1.0)
    controllerSet.set_value('TriggerR', 0.0)

def lightBrake():
    controllerSet.set_value('TriggerL', 0.3)
    controllerSet.set_value('TriggerR', 0.0)

def straight():
    controllerSet.set_value('AxisLx', 0.0)

def slightRight():

    controllerSet.set_value('AxisLx', 0.1)

def medRight():
    controllerSet.set_value('AxisLx', 0.3)

def hardRight():
    controllerSet.set_value('AxisLx', 0.7)

def crankRight():
    controllerSet.set_value('AxisLx', 1)

def slightLeft():
    controllerSet.set_value('AxisLx', -0.1)

def medLeft():
    controllerSet.set_value('AxisLx', -0.3)

def hardLeft():
    controllerSet.set_value('AxisLx', -0.7)

def crankLeft():
    controllerSet.set_value('AxisLx', -1)