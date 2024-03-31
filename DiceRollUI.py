#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

from Helpers import Helpers
from Popup import Popup

class DiceRollUI:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        frame6 = ttk.Frame(frame1)
        frame6.configure(height=200, width=200)
        label1 = ttk.Label(frame6)
        label1.configure(font="{sans} 12 {}", text='Number')
        label1.pack(side="top")
        self.number_box = ttk.Entry(frame6)
        self.number_box.configure(
            font="{sans} 14 {}", justify="center", width=4)
        _text_ = '1'
        self.number_box.delete("0", "end")
        self.number_box.insert("0", _text_)
        self.number_box.pack(side="top")
        frame6.grid(column=0, row=0)
        frame13 = ttk.Frame(frame1)
        frame13.configure(height=200, width=200)
        label7 = ttk.Label(frame13)
        label7.configure(font="{sans} 12 {}", text='Sides')
        label7.pack(side="top")
        self.sides_box = ttk.Entry(frame13)
        self.sides_box.configure(
            font="{sans} 14 {}",
            justify="center",
            width=4)
        _text_ = '20'
        self.sides_box.delete("0", "end")
        self.sides_box.insert("0", _text_)
        self.sides_box.pack(side="top")
        frame13.grid(column=1, row=0)
        frame14 = ttk.Frame(frame1)
        frame14.configure(height=200, width=200)
        label8 = ttk.Label(frame14)
        label8.configure(font="{sans} 12 {}", text='Modifier')
        label8.pack(side="top")
        self.mod_box = ttk.Entry(frame14)
        self.mod_box.configure(font="{sans} 14 {}", justify="center", width=4)
        _text_ = '0'
        self.mod_box.delete("0", "end")
        self.mod_box.insert("0", _text_)
        self.mod_box.pack(side="top")
        frame14.grid(column=2, row=0)
        frame15 = ttk.Frame(frame1)
        frame15.configure(height=200, width=200)
        self.roll_button = ttk.Button(frame15)
        self.roll_button.configure(text='Roll', width=20)
        self.roll_button.pack(side="top")
        self.roll_button.configure(command=self.roll_action)
        self.adv_button = ttk.Button(frame15)
        self.adv_button.configure(text='Roll With Advantage', width=20)
        self.adv_button.pack(side="top")
        self.adv_button.configure(command=self.adv_action)
        self.dis_button = ttk.Button(frame15)
        self.dis_button.configure(text='Roll With Disadvantage', width=20)
        self.dis_button.pack(side="top")
        self.dis_button.configure(command=self.dis_action)
        frame15.grid(column=0, columnspan=3, pady=5, row=1)
        frame1.pack(side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def adv_action(self):
        try:
            # Get the text from each box, and try to convert it to an int
            number = int(self.number_box.get())
            sides = int(self.sides_box.get())
            modifier = int(self.mod_box.get())
            
            # Get the result of the two rolls
            roll_list_1, roll_sum_1 = Helpers.roll_multiple_dice(number, sides, 0)
            roll_list_2, roll_sum_2 = Helpers.roll_multiple_dice(number, sides, 0)
            
            # Get the higher of the two rolls
            msg_str = ""
            msg_str = "Roll 1: "
            msg_str += Helpers.roll_list_to_string(roll_list_1)
            msg_str += " (T: " + str(roll_sum_1) + ")"
            msg_str += "\nRoll 2: "
            msg_str += Helpers.roll_list_to_string(roll_list_2)
            msg_str += " (T: " + str(roll_sum_2) + ")"
            msg_str += "\n"
            if(roll_sum_1 > roll_sum_2):
                msg_str += "Roll 1 is higher.\n" + str(roll_sum_1) + " + " + str(modifier) + " = " + str(roll_sum_1 + modifier)
            elif(roll_sum_1 < roll_sum_2):
                msg_str += "Roll 2 is higher.\n" + str(roll_sum_2) + " + " + str(modifier) + " = " + str(roll_sum_2 + modifier)
            else:
                msg_str += "Rolls are the same score, using roll 1.\n" + str(roll_sum_1) + " + " + str(modifier) + " = " + str(roll_sum_1 + modifier)
        
        except ValueError:
            # If there's an error, display a message box with the error
            msg_str = "Please enter a valid number in each box"
        
        # Pass to roll result popup
        Popup.Roll_Result(msg_str)

    def dis_action(self):
        try:
            # Get the text from each box, and try to convert it to an int
            number = int(self.number_box.get())
            sides = int(self.sides_box.get())
            modifier = int(self.mod_box.get())
            
            # Get the result of the two rolls
            roll_list_1, roll_sum_1 = Helpers.roll_multiple_dice(number, sides, 0)
            roll_list_2, roll_sum_2 = Helpers.roll_multiple_dice(number, sides, 0)
            
            # Get the higher of the two rolls
            msg_str = ""
            msg_str = "Roll 1: "
            msg_str += Helpers.roll_list_to_string(roll_list_1)
            msg_str += " (T: " + str(roll_sum_1) + ")"
            msg_str += "\nRoll 2: "
            msg_str += Helpers.roll_list_to_string(roll_list_2)
            msg_str += " (T: " + str(roll_sum_2) + ")"
            msg_str += "\n"
            if(roll_sum_1 < roll_sum_2):
                msg_str += "Roll 1 is lower.\n" + str(roll_sum_1) + " + " + str(modifier) + " = " + str(roll_sum_1 + modifier)
            elif(roll_sum_1 > roll_sum_2):
                msg_str += "Roll 2 is lower.\n" + str(roll_sum_2) + " + " + str(modifier) + " = " + str(roll_sum_2 + modifier)
            else:
                msg_str += "Rolls are the same score, using roll 1.\n" + str(roll_sum_1) + " + " + str(modifier) + " = " + str(roll_sum_1 + modifier)
        
        except ValueError:
            # If there's an error, display a message box with the error
            msg_str = "Please enter a valid number in each box"
        
        # Pass to roll result popup
        Popup.Roll_Result(msg_str)

    def roll_action(self):
        try:
            # Get the text from each box, and try to convert it to an int
            number = int(self.number_box.get())
            sides = int(self.sides_box.get())
            modifier = int(self.mod_box.get())
            
            # Then call the show_dice_roll_message_component from the helpers,
            res_str = Helpers.show_dice_roll_message_component(number, sides, modifier)

        except ValueError:
            # If there's an error, display a message box with the error
            res_str = "Please enter a valid number in each box"
        
        # Pass to roll result popup
        Popup.Roll_Result(res_str)

if __name__ == "__main__":
    app = DiceRollUI()
    app.run()