from tkinter import *

def openMic():
    if status.get() == "stopped":
        ##Empezar a grabar
        status.set("processing")
        print("open mic")

def closeMic():
    if status.get() == "processing":
        status.set("stopping")
        ##Parar de grabar
        status.set("stopped")
        print("close mic")

window = Tk()
status = StringVar()
status.set("stopped")
prediction = StringVar()
prediction.set("none")

li = Label(window, text="EMOTION DETECTION")
li.grid(row=0, column=0)


bt = Button(window, command=openMic, text="Open microphone")
bt.grid(row=2, column=0)

bt = Button(window, command=closeMic, text="Close microphone")
bt.grid(row=2, column=1)

li = Label(window, text="Current status:")
li.grid(row=3, column=0)

li = Label(window, textvariable=status)
li.grid(row=3, column=1)

li = Label(window, text="Predicted:")
li.grid(row=5, column=0)

li = Label(window, textvariable=prediction)
li.grid(row=5, column=1)


window.mainloop()

