import random

def SimulatorInVal(input,oldVal,offVal):
    
    #constants to be corrected by trial end error
    K = 0.08
    U = 0.3

    delta = input-oldVal
    newVal = oldVal + offVal*K*(random.random()-0.5) + delta*U
    if(newVal < input-offVal):
        newVal = input-offVal
    elif (newVal > input+offVal):
        newVal = input+offVal
    return newVal

def SimulatorInPercent (input,oldVal,offP):
    return SimulatorInVal(input,oldVal,input*offP/100)
