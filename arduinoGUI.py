from Tkinter import *
from arduinoComms import *
import atexit

def exit_handler():
    print 'My application is ending!'
    closeSerial()

atexit.register(exit_handler)

# global variables for this module
ledAstatus = 0
ledBstatus = 0
servoPos = 10
f1 = 1
p1 = 0
a1 = 180
f2 = 1
p2 = 0
a2 = 180

tkArd = Tk()
tkArd.minsize(width=640, height=200)
tkArd.config(bg = 'yellow')
tkArd.title("Arduino GUI Demo")

def setupView():
    global masterframe
    masterframe = Frame(bg = "yellow")
    masterframe.pack()
	
    selectPort()

def runProgram():
    # print("blub")
    tkArd.mainloop()	

def selectPort():
    global masterframe, radioVar
    for child in masterframe.winfo_children():
        child.destroy()
    radioVar = StringVar()

    lst = listSerialPorts()
	
    l1= Label(masterframe, width = 5, height = 2, bg = "yellow") 
    l1.pack()

    if len(lst) > 0:
        for n in lst:
            r1 = Radiobutton(masterframe, text=n, variable=radioVar, value=n, bg = "yellow")
            r1.config(command = radioPress)
            r1.pack(anchor=W)
    else:
        l2 = Label(masterframe, text = "No Serial Port Found")
        l2.pack()

	
def mainScreen():
    global masterframe
    for child in masterframe.winfo_children():
        child.destroy()
		
    # labelA = Label(masterframe, width = 5, height = 2, bg = "yellow") 
    # labelB = Label(masterframe, width = 5, bg = "yellow") 
    labelC = Label(masterframe, width = 10, bg = "yellow") 
	
    # ledAbutton = Button(masterframe, text="LedA", fg="white", bg="black")
    # ledAbutton.config(command = lambda: btnA(ledAbutton))
    
    # ledBbutton = Button(masterframe, text="LedB", fg="white", bg="black")
    # ledBbutton.config(command = lambda:  btnB(ledBbutton))
	
    slider_f1 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_f1.config(command = slide_f1, length=180, label="freq 1 (val / 45) * 2 * PI", takefocus=True)
    slider_p1 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_p1.config(command = slide_p1, length=180, label="phase 1 (val / 180) * 2 * PI")
    slider_a1 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_a1.config(command = slide_a1, length=180, label="amp 1 (val / 2)")
    slider_f2 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_f2.config(command = slide_f2, length=180, label="freq 2 (val / 45) * 2 * PI")
    slider_p2 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_p2.config(command = slide_p2, length=180, label="phase 2 (val / 180) * 2 * PI")
    slider_a2 = Scale(masterframe, from_=0, to=180, orient=HORIZONTAL)
    slider_a2.config(command = slide_a2, length=180, label="amp 2 (val / 2)")
    
    # labelA.grid(row = 0)
    # ledAbutton.grid(row = 1)
    # labelB.grid(row = 1, column = 2)
    # ledBbutton.grid(row = 1, column = 3)
    labelC.grid(row = 2)
    slider_f1.grid(row = 3, column = 1)#, columnspan = 5)
    slider_p1.grid(row = 4, column = 1)#, columnspan = 5)
    slider_a1.grid(row = 5, column = 1)#, columnspan = 5)
    slider_f2.grid(row = 3, column = 3)#, columnspan = 5)
    slider_p2.grid(row = 4, column = 3)#, columnspan = 5)
    slider_a2.grid(row = 5, column = 3)#, columnspan = 5)
    print("end mainScreen")
	
	
def btnA(btn):
    global ledAstatus, ledBstatus, servoPos
	
    if ledAstatus == 0:
        ledAstatus = 1
        btn.config(bg="white", fg="black")
    else:
        ledAstatus = 0
        btn.config(fg="white", bg="black")
    valToArduino(ledAstatus, ledBstatus, servoPos)

def btnB(btn):
    global ledAstatus, ledBstatus, servoPos
	
    if ledBstatus == 0:
        ledBstatus = 1
        btn.config(bg="white", fg="black")
    else:
        ledBstatus = 0
        btn.config(fg="white", bg="black")
    valToArduino(ledAstatus, ledBstatus, servoPos)


def slide_f1(sval):
    global f1, p1, a1, f2, p2, a2
    f1 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def slide_p1(sval):
    global f1, p1, a1, f2, p2, a2
    p1 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def slide_a1(sval):
    global f1, p1, a1, f2, p2, a2
    a1 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def slide_f2(sval):
    global f1, p1, a1, f2, p2, a2
    f2 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def slide_p2(sval):
    global f1, p1, a1, f2, p2, a2
    p2 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def slide_a2(sval):
    global f1, p1, a1, f2, p2, a2
    a2 = sval
    # valToArduino(ledAstatus, ledBstatus, servoPos)
    # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
    valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

def radioPress():
    global radioVar
    setupSerial(radioVar.get())
    mainScreen()

setupView()
tkArd.mainloop()	
