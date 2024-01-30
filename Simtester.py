import Simdemo
inp = input("Enter a number: \nPress q to quit\n")
if inp != "q":
    oldVal = int(inp)
    while inp != "q":
        inp = int(inp)
        newVal= Simdemo.SimulatorInPercent(inp,oldVal,10)
        print("input:" , inp, "\t oldVal: " ,oldVal, "\t newVal:", newVal, "\t offVal: ", inp/10)
        oldVal = newVal
        inp = input("Enter number: ")
print("\nProgram ends now.\n")