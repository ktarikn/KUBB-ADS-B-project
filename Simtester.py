import Simdemo
inp = input("Enter number: ")
oldVal = int(inp)
while(inp != "q"):
    inp = int(inp)
    newVal= Simdemo.SimulatorInPercent(inp,oldVal,10)
    print("input:" , inp, "\t oldVal: " ,oldVal, "\t newVal:", newVal, "\t offVal: ", inp/10)
    oldVal = newVal
    inp = input("Enter number: ")