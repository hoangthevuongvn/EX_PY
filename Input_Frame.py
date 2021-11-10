from tkinter import *
from functools import wraps
from re import match
import tkinter as tk
from tkinter import ttk
from tkinter import Button, Widget, ttk
from tkinter.constants import W
from tkinter.messagebox import showinfo
from typing import Match
import paho.mqtt.client as mqtt
import json

class Input_Frame(ttk.Frame):

    findwhat_var = ""
    replacewith_var = ""
    findwhat = ""
    replacewith = ""
    match_case_var = ""
    wrap_around_var = ""
    oder = ""
    json = {"order":"findnext","match_case":"1","wrap_around": "0", "find_what": "", "replace_with": ""}

    def __init__(self, container):
        super().__init__(container)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)


        self.create_widgets()
        # self.submit()
    

    def create_widgets(self):
        Input_Frame.findwhat_var = StringVar()
        Input_Frame.replacewith_var = StringVar()
    
        Lb = ttk.Label(self, text='Find what:')
        Lb.grid(column=0, row=0, sticky=tk.W)
        
        keyword = ttk.Entry(self, textvariable = Input_Frame.findwhat_var, width=30,)
        keyword.focus()
        keyword.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(self, text='Replace with: ').grid(
                column=0, row=1, sticky=tk.W)
        replacement = ttk.Entry(self,textvariable = Input_Frame.replacewith_var, width=30)
        replacement.grid(column=1, row=1, sticky=tk.W)

        Input_Frame.match_case_var = StringVar()
        match_case_check = ttk.Checkbutton(
            self,
            text='Match case',
            variable=Input_Frame.match_case_var,
            command=lambda: print(Input_Frame.match_case_var.get())
        )
        match_case_check.grid(column=0, row=2, sticky=tk.W)

        Input_Frame.wrap_around_var = StringVar()
        wrap_around_check = ttk.Checkbutton(
            self,
            text='Wrap around',
            variable=Input_Frame.wrap_around_var,
            command=lambda: print(Input_Frame.wrap_around_var.get())
        )
        wrap_around_check.grid(column=0, row=3, sticky=tk.W)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=5)
            # winfo_children()
    
    def submit(oder):
        

        Input_Frame.findwhat = Input_Frame.findwhat_var.get()
        Input_Frame.replacewith = Input_Frame.replacewith_var.get()

        Input_Frame.json["find_what"] = Input_Frame.findwhat_var.get()
        Input_Frame.json["replace_with"] = Input_Frame.replacewith_var.get()
        Input_Frame.json["match_case"] = Input_Frame.match_case_var.get()
        Input_Frame.json["wrap_around"] = Input_Frame.wrap_around_var.get()
        Input_Frame.json["order"] = oder

        print(Input_Frame.json)


        # print("FindWhat is : " + Input_Frame.findwhat)
        # print("Replace is : " + Input_Frame.replacewith)

        # Input_Frame.findwhat_var.set("")
        # Input_Frame.replacewith_var.set("")
class Button_Frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)


        self.create_widgets()
    
    def create_widgets(self):
        # findwhat_var = StringVar()
        ttk.Button(self, text='Find Next', command=lambda: print(Input_Frame.submit("findnext"))).grid(column=0, row=0)
        ttk.Button(self, text='Replace', command=lambda: Input_Frame.submit("Repalce")).grid(column=0, row=1)
        ttk.Button(self, text='Send_MQTT', command=lambda: Mqtt_pub.Send_message(json.dumps(Input_Frame.json))).grid(column=0, row=2)
        ttk.Button(self, text='Cancel', command=self.quit).grid(column=0, row=3)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)

class Mqtt_pub():
    def __init__(self):
        self.Send_message

    def Send_message(self):

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("Parking")

            # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload))

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        # client.connect("mqtt.eclipseprojects.io", 1883, 60)
        client.connect("localhost", 1883, 60)

        client.publish(topic="Parking", payload=self, qos=0, retain=False)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        # client.loop_forever()


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('400x240')
        self.title("Replace")
        self.resizable(False, False)
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # self.attributes('-toolwindow', True)

        self.create_widgets()

    def create_widgets(self):
        input_frame = Input_Frame(self)
        input_frame.grid(column=0, row=0)

        button_frame = Button_Frame(self)
        button_frame.grid(column=1, row=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
        
    
    

