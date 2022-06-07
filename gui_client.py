import socket
from networkHandler import network_handler


from tkinter import *
from tkinter import filedialog as fd
import pyscreeze as pyautogui


def main():
    gui = Gui(8891, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    gui.connection()

    gui.setPanel()
    gui.gui.mainloop()

class Gui:
    state = True
    current_socket = ""
    def __init__(self, port, socket):
        self.gui = Tk()
        self.port = port
        self.socket = socket
        self.net_handler = network_handler(self.socket)

        self.speakerState = {}


    def connection(self):
        self.socket.connect(("127.0.0.1", self.port))
        print("You are connected!")

        connectMSG = "I'm the gui"
        self.net_handler.sendMessage(connectMSG, True)

    def setPanel(self):
        panelHeight, panelWidth = self.buildAPanel(self.gui, "Control Panel")

        #set button 1
        button_1 = Button(self.gui, text="File",bg = "purple", height=panelHeight-770, width=panelWidth-1470, command=self.pickAFile)
        button_1.place(x = (panelWidth / 7), y = (panelHeight / 7))

        # set button 2
        button_2 = Button(self.gui, text="Control", bg = "purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.topControl)
        button_2.place(x = (2.5 * panelWidth / 7), y = (3.5 * panelHeight / 7))

        # set button 3
        button_3 = Button(self.gui, text="Settings", bg = "purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.topSettings)
        button_3.place(x = (4 * panelWidth / 7), y = (panelHeight / 7))

        # set button exit
        button_exit = Button(self.gui, text="Exit", bg="purple", height=panelHeight-775, width=panelWidth-1500,command=self.destroy)
        button_exit.place(relx=1.0, rely=1.0, anchor=SE)


    def destroy(self):
        print("sending destroy")
        self.net_handler.sendMessage("destroy", True)
        print("sent destroy")
        self.gui.destroy()


    def buildAPanel(self,gui, name):
        #width, height = pyautogui.size()
        width, height = 1920, 1080

        # set the window size & color & title
        panelWidth = width - 400
        panleHeight = height - 300
        gui.geometry(f"{panelWidth}x{panleHeight}")
        gui.configure(bg='blueviolet')
        gui.title(name)
        return panleHeight, panelWidth

    def topControl(self):
        top = Toplevel(self.gui)
        panelHeight, panelWidth = self.buildAPanel(top, "Control")

        button_play = Button(top, text="Play", bg="purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.play)
        button_play.place(x = (panelWidth / 7), y = (panelHeight / 7))

        button_pause = Button(top, text="Pause", bg="purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.pause)
        button_pause.place(x = (4 * panelWidth / 7), y = (panelHeight / 7))

        button_raiseVolume = Button(top, text="Raise Volume", bg="purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.raiseVolume)
        button_raiseVolume.place(x=(panelWidth / 7), y=(4 * panelHeight / 7))

        button_lowerVolume = Button(top, text="Lower Volume", bg="purple", height=panelHeight - 770, width=panelWidth - 1470,command=self.lowerVolume)
        button_lowerVolume.place(x=(4 * panelWidth / 7), y=(4 * panelHeight / 7))

        button_exit = Button(top, text="Exit", bg="purple", height=panelHeight-775, width=panelWidth-1500,command=top.destroy)
        button_exit.place(relx=1.0, rely=1.0, anchor=SE)

        top.mainloop()
    def play(self):
        self.net_handler.sendMessage("play", True)
    def pause(self):
        self.net_handler.sendMessage("pause", True)
    def raiseVolume(self):
        self.net_handler.sendMessage("raiseVolume", True)
    def lowerVolume(self):
        self.net_handler.sendMessage("lowerVolume", True)
    def lowerVolumeToZero(self):
        self.net_handler.sendMessage("lowerVolumeToZero", True)
    def raiseVolumeToHalf(self):
        self.net_handler.sendMessage("raiseVolumeToHalf", True)


    def pickAFile(self):
        filePath = fd.askopenfilename()

        print("sending upload")
        self.net_handler.sendMessage("upload", True)
        print ("sending file")
        self.net_handler.sendMessage(filePath, True)
        print("sent everything")

    def topSettings(self):
        top = Toplevel(self.gui)
        panelHeight, panelWidth = self.buildAPanel(top, "Settings")

        self.net_handler.sendMessage("settings", True)
        speakers = str(self.net_handler.receiveMessage(True))

        speakersList = speakers.split("*")

        numX, numY, numcount = 1, 1, 1
        for i in speakersList:
            print(i)
            if(i != ""):
                self.speakerState[i] = True
                button = Button(top, text=("Speaker " + str(numcount)), bg="orange", height=panelHeight-775, width=panelWidth-1500, command=lambda m=i: self.which_button(m))
                button.place(x=(panelWidth / 8 * numX), y=(panelHeight / 8 * numY))

            if numX == 6:
                numY += 1
                numX = 0

            numX += 1
            numcount += 1

        button_exit = Button(top, text="Exit", bg="purple", height=panelHeight-775, width=panelWidth-1500, command=top.destroy)
        button_exit.place(relx=1.0, rely=1.0, anchor=SE)

        top.mainloop()

    def which_button(self, speaker_socket):
        self.switch(speaker_socket)

    def switch(self, speaker_socket):
        if self.speakerState[speaker_socket] == True:
            self.net_handler.sendMessage(speaker_socket, True)
            self.net_handler.sendMessage("lowerVolumeToZero", True)
            self.speakerState[speaker_socket] = False

        else:
            self.net_handler.sendMessage(speaker_socket, True)
            self.net_handler.sendMessage("raiseVolumeToHalf", True)
            self.speakerState[speaker_socket] = True


if __name__ == '__main__':
        main()