from Tkinter import *
from arduinoComms import *
import atexit
import threading
import argparse
import time, sys

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

class ArduinoGUIThread(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.isrunning = True

        print("setupView")
        self.setupView(device)

    def run(self):
        print("starting ...")
        self.tkArd = Tk()
        self.tkArd.protocol("WM_DELETE_WINDOW", self.delete_callback)
        self.tkArd.minsize(width=640, height=200)
        self.tkArd.config(bg = 'yellow')
        self.tkArd.title("Arduino GUI Demo")

        # internal data
        self.f1 = 1
        self.p1 = 0
        self.a1 = 90
        self.f2 = 1
        self.p2 = 0
        self.a2 = 90
        
        self.masterframe = Frame(bg = "yellow")
        self.masterframe.pack()
	
        self.mainScreen()

        self.thread1 = threading.Thread(target = self.readerThread)
        self.thread1.start()

        for i in range(3):
            valReqToArduinoShanghai()
            time.sleep(0.1)
        
        self.tkArd.mainloop()
        
        # while self.isrunning:
        #     print("running")
        #     # recvFromArduino()
        #     time.sleep(1)

    def readerThread(self):
        while self.isrunning:
            onBoardData = recvFromArduino(1.0)
            print("'%s'" % onBoardData)
            # if onBoardData != "<<" or onBoardData != ">>":
            try:
                (f1, p1, a1, f2, p2, a2, ts) = onBoardData.split(",")
                # print(f1, p1, a1, f2, p2, a2, ts)
                self.slider_f1.set(int(f1))
                self.slider_p1.set(int(p1))
                self.slider_a1.set(int(a1))
                self.slider_f2.set(int(f2))
                self.slider_p2.set(int(p2))
                self.slider_a2.set(int(a2))
            except Exception, e:
                print("except", e)
            time.sleep(0.001)

    def delete_callback(self):
        self.isrunning = False
        sys.exit()

    def setupView(self, device):
        # global masterframe
        # self.selectPort()
        self.selectPortStatic(device)

    # def runProgram(self):
    #     print("runProgram")
    #     self.tkArd.mainloop()	

    def selectPortStatic(self, device):
        print("selectPortStatic with %s" % device)
        setupSerial(device)
        
    def selectPort(self):
        global masterframe, radioVar
        for child in self.masterframe.winfo_children():
            child.destroy()
        radioVar = StringVar()

        lst = listSerialPorts()
	
        l1= Label(self.masterframe, width = 5, height = 2, bg = "yellow") 
        l1.pack()

        if len(lst) > 0:
            for n in lst:
                r1 = Radiobutton(self.masterframe, text=n, variable=radioVar, value=n, bg = "yellow")
                r1.config(command = radioPress)
                r1.pack(anchor=W)
        else:
            l2 = Label(self.masterframe, text = "No Serial Port Found")
            l2.pack()

	
    def mainScreen(self):
        # global masterframe
        for child in self.masterframe.winfo_children():
            child.destroy()
		
        # labelA = Label(self.masterframe, width = 5, height = 2, bg = "yellow") 
        # labelB = Label(self.masterframe, width = 5, bg = "yellow") 
        labelC = Label(self.masterframe, width = 10, bg = "yellow") 
	
        # ledAbutton = Button(self.masterframe, text="LedA", fg="white", bg="black")
        # ledAbutton.config(command = lambda: btnA(ledAbutton))
    
        # ledBbutton = Button(self.masterframe, text="LedB", fg="white", bg="black")
        # ledBbutton.config(command = lambda:  btnB(ledBbutton))
	
        self.slider_f1 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_f1.config(command = self.slide_f1, length=180, label="freq 1 (val / 45) * 2 * PI", takefocus=True)
        self.slider_p1 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_p1.config(command = self.slide_p1, length=180, label="phase 1 (val / 180) * 2 * PI")
        self.slider_a1 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_a1.config(command = self.slide_a1, length=180, label="amp 1 (val / 2)")
        self.slider_f2 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_f2.config(command = self.slide_f2, length=180, label="freq 2 (val / 45) * 2 * PI")
        self.slider_p2 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_p2.config(command = self.slide_p2, length=180, label="phase 2 (val / 180) * 2 * PI")
        self.slider_a2 = Scale(self.masterframe, from_=0, to=180, orient=HORIZONTAL)
        self.slider_a2.config(command = self.slide_a2, length=180, label="amp 2 (val / 2)")

        self.sendbut = Button(self.masterframe, text="Send", command = self.sendbut, fg="white", bg="black")
        
        # labelA.grid(row = 0)
        # ledAbutton.grid(row = 1)
        # labelB.grid(row = 1, column = 2)
        # ledBbutton.grid(row = 1, column = 3)

        self.sendbut.grid(row = 1)
        
        labelC.grid(row = 2)
        self.slider_f1.grid(row = 3, column = 1)#, columnspan = 5)
        self.slider_p1.grid(row = 4, column = 1)#, columnspan = 5)
        self.slider_a1.grid(row = 5, column = 1)#, columnspan = 5)
        self.slider_f2.grid(row = 3, column = 3)#, columnspan = 5)
        self.slider_p2.grid(row = 4, column = 3)#, columnspan = 5)
        self.slider_a2.grid(row = 5, column = 3)#, columnspan = 5)

    def sendbut(self):
        valToArduinoShanghai(self.f1, self.p1, self.a1, self.f2, self.p2, self.a2)
	
	
    def btnA(self, btn):
        global ledAstatus, ledBstatus, servoPos
	
        if ledAstatus == 0:
            ledAstatus = 1
            btn.config(bg="white", fg="black")
        else:
            ledAstatus = 0
            btn.config(fg="white", bg="black")
        valToArduino(ledAstatus, ledBstatus, servoPos)

    def btnB(self, btn):
        global ledAstatus, ledBstatus, servoPos
	
        if ledBstatus == 0:
            ledBstatus = 1
            btn.config(bg="white", fg="black")
        else:
            ledBstatus = 0
            btn.config(fg="white", bg="black")
        valToArduino(ledAstatus, ledBstatus, servoPos)


    def slide_f1(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.f1 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def slide_p1(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.p1 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def slide_a1(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.a1 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def slide_f2(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.f2 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def slide_p2(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.p2 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def slide_a2(self, sval):
        # global f1, p1, a1, f2, p2, a2
        self.a2 = sval
        # valToArduino(ledAstatus, ledBstatus, servoPos)
        # print("%s,_%s_,%s,%s / %s") % (f1, p1, a1, f2, p2, a2, sval)
        # valToArduinoShanghai(f1, p1, a1, f2, p2, a2)

    def radioPress(self):
        global radioVar
        setupSerial(radioVar.get())
        mainScreen()

def main(args):
    print("main")
    App = ArduinoGUIThread(args.device)
    App.start()
    while App.isrunning:
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", default="/dev/ttyUSB0")

    args = parser.parse_args()
    main(args)
