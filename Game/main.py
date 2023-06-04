# ---------------------------------------------
# Title: main.py
# Class: CS 30
# Date: 15/05/23
# Version: 1.0
# ---------------------------------------------
"""
Current Assignment: main.py

This file contains important GUI code.
Always run the game from this file.
"""
# Important import statements
from tkinter import *
import connection
import battle
from multiprocessing import Process


# This class contains import GUI code that we need from Tkinter
class GUI:
    # Initializing attributes
    def __init__(self):
        self.mainframe = None
        self.main = Tk()
        self.pipe = None
        self.online = False
        self.op = False
        self.game = False
        self.ip = None
        self.port = None
        self.process1 = None
        self.process2 = None
        self.process3 = None
        self.connect_process = None

    # Defines our variables to connect with others
    def connec(self, ip, port):
        ip = self.ip.get()
        port = self.port.get()
        self.pipe = connection.GameConnection(ip, port)
        self.pipe.make_connection()

    # Defines the variables needed for creating a server
    def makeserver(self, ip, port):
        self.pipe = connection.GameConnection(ip, port)
        self.pipe.create_server()

    def offgame(self):
        self.process2 = Process(target=self.offgame_wrapper())
        self.process2.start()

    def offgame_wrapper(self):
        self.game = battle.LBattle()
        self.game.game_ui()

    # Defines variables that we use to join a hosted game on a server
    def joingame(self):
        ip = self.ip.get()
        port = self.port.get()
        self.pipe = connection.GameConnection(ip, port)
        try:
            self.pipe.connec(ip, port)
        except Exception as e:
            print("Could not connect!")
        self.process1.start()

    def ongame(self):
        ip = self.ip.get()
        port = self.port.get()
        try:
            self.process3 = Process(target=self.pipe.makeserver, args=(ip, port,))
            self.process3.start()
        except Exception as e:
            self.process3.join()
            print("Could not create a new server!")
        self.process3.join()

    # This is the code that we use to design our main title screen that the user sees
    # It includes text, buttons and input areas
    def temp_name(self):
        self.ip = StringVar(self.main)
        self.port = StringVar(self.main)
        self.ip.set("Enter IP Address Here")
        self.port.set("Enter Port Number Here")
        self.main.geometry("600x900")
        self.main.title("Pokémon Battle - Title Screen")
        maintitle = Label(self.main, text="Welcome to the Pokemon Battle!", font=("MS Comic Sans", "18"))
        maintitle.pack(ipadx=20, ipady=10, expand=True)
        choice1 = Label(self.main, text="Join a battle server", font=("MS Comic Sans", "14"))
        choice1.pack(ipadx=20, ipady=20, expand=True)
        ip1 = Entry(self.main, textvariable=self.ip)
        ip1.pack(ipadx=20)
        port1 = Entry(self.main, textvariable=self.port)
        port1.pack(ipadx=20)
        connect1 = Button(self.main, text="Connect!", command=self.joingame)
        connect1.pack()
        choice2 = Label(self.main, text="Create a battle server", font=("MS Comic Sans", "14"))
        choice2.pack(ipadx=20, ipady=20, expand=True)
        ip2 = Entry(self.main, textvariable=self.ip)
        ip2.pack(ipadx=20)
        port2 = Entry(self.main, textvariable=self.port)
        port2.pack(ipadx=20)
        create = Button(self.main, text="Create Server!", command=self.ongame)
        create.pack()
        choice3 = Label(self.main, text="Play an offline bot!", font=("MS Comic Sans", "14"))
        choice3.pack(ipadx=20, ipady=20, expand=True)
        start = Button(self.main, text="Play Bot!", command=self.offgame)
        start.pack()
        credit = Label(self.main, text="This program was made by Calvin, Ebaad and Josh", font=("MS Comic Sans", "10"))
        credit.pack(ipadx=20, ipady=20, expand=True)
        self.main.mainloop()


# We call this once the main file is run
if __name__ == "__main__":
    b = GUI()
    b.temp_name()
