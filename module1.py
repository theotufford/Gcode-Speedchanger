Gcodefolderpath = "C:\\Users\\tuffl\\Desktop\\projects\\gcode\\"
txtfilepath =  "C:\\Users\\tuffl\\source\\repos\\CppProject1\\misc\\speedchanger.txt"

choice = input("test type\n - - - - - - \n 1: snaketest       2: widetest       3: othertest\n test:") 
if choice == "1":
    filename = "CFFFP_snaketest"
elif choice == "2":
    print("not calibrated")
else:
    filename = input("input filename: ")
   

gcodefilepath = Gcodefolderpath + filename + ".gcode"
finalfilepath = Gcodefolderpath + filename + "_accelshifted.gcode"
with open(gcodefilepath, "r") as gcode:
    gcodedump = gcode.readlines()
    with open(txtfilepath, "w") as txtfile:
        gcodetotxt = "".join(gcodedump)
        txtfile.write(gcodetotxt)



layerHeight = 0.2
intialLayerHeight = 0.3

heightincrement = int((float(input("Change height: "))*100))
GcodeHeader = []
zheights = []
zlinetable = []
linestoedit = []
accelIncrementTable = []
i=0
with open(txtfilepath, "r") as f:
    lines = f.readlines()
    

  
    #cut out all the lines before the first decleration of accel because they can cause problems
    

    for line in lines:
      if line.find("M204") != -1:
          break
      else:
          i=i+1
    for a in range(i):
        GcodeHeader.append(lines[0])
        lines.pop(0)
    baseacceleration = int(lines[0].split("S")[1])

    for line in lines:
        if line.find(" Z") != -1:
            zlinetable.append(lines.index(line))
            line  = line.split("Z")
            zheights.append(int(float(line[1]) *100)-30)
    i=0
    for height in zheights: 
        if height % heightincrement == 0: 
            linestoedit.append(zlinetable[i])
        i = i+1
    linestoedit.pop(0)
    
    print("accel will be modified ", len(linestoedit), "times, change this value by a \n 1: fixed increment \n 2: per change ")
    
    if input("Choice: ") == "1":
        accelfixedIncrement=int(input("Increment: "))
        i=1
        for line in linestoedit:
            line = line + 1
            AccelShiftStr = "M204 S" + str((accelfixedIncrement*i)+baseacceleration) + "\n"
            GcodeHeader.insert(i, ";" + str(i) + ": " + str((accelfixedIncrement*i)+baseacceleration) + "\n")
            lines.insert(line, AccelShiftStr)
            i = i+1
    else:
        print ("accel value 0: ", str(baseacceleration))
        for a in range(len(linestoedit)):
            accelvalue = input("accel value " + str(a+1) + ": ")
            accelIncrementTable.append(accelvalue)
            
            GcodeHeader.insert(  a+1, ";accel at " + str(((a+1)*layerHeight)+intialLayerHeight) + "mm : " + str(heightincrement*(a+1)) + "\n"  )
        
        i=0
        for line in linestoedit:
            line = line + 1
            AccelShiftStr = "M204 S" + str(accelIncrementTable[i]) + "\n"
            lines.insert(line, AccelShiftStr)
            i = i+1

    for a in range(len(GcodeHeader)):
        lines.insert(a, GcodeHeader[a])

    newgcode = "".join(lines)
with open(finalfilepath, "w") as f:
    f.write(newgcode)

    