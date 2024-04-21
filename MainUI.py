#!/usr/bin/python3
import sys
import os

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

from ActiveCharacterSheetUI import ActiveCharacterSheetUI
from CharacterSheet import CharacterSheet
from DiceRollUI import DiceRollUI
from EncounterTracker import EncounterTracker
from Popup import EditItem_Option, Popup

class MainUI:
    def __init__(self, master=None, default_cs_loc=None):
        self.default_cs_loc = default_cs_loc

        # build ui
        self.UI = tk.Tk() if master is None else tk.Toplevel(master)
        self.UI.configure(height=200, width=300)
        self.UI.title("D&D Active Character Sheet")
        self.header_label = ttk.Label(self.UI)
        self.header_label.configure(
            anchor="nw",
            compound="center",
            font="TkHeadingFont",
            justify="center",
            text='D&D Active Character Sheet',
            width=35)
        self.header_label.pack(side="top")
        self.sep = ttk.Separator(self.UI)
        self.sep.configure(orient="horizontal")
        self.sep.pack(side="top")
        self.new_char_button = ttk.Button(self.UI)
        self.new_char_button.configure(text='Create Character', width=20)
        self.new_char_button.pack(side="top")
        self.new_char_button.configure(command=self.new_char_action)
        self.load_char_button = ttk.Button(self.UI)
        self.load_char_button.configure(
            takefocus=True, text='Load Character', width=20)
        self.load_char_button.pack(side="top")
        self.load_char_button.configure(command=self.load_char_action)
        self.roll_dice_button = ttk.Button(self.UI)
        self.roll_dice_button.configure(text='Roll Dice', width=20)
        self.roll_dice_button.pack(side="top")
        self.roll_dice_button.configure(command=self.roll_dice_action)
        self.encounter_tracker_button = ttk.Button(self.UI)
        self.encounter_tracker_button.configure(
            text='Encounter Tracker', width=20)
        self.encounter_tracker_button.pack(side="top")
        self.encounter_tracker_button.configure(
            command=self.encounter_tracker_action)
        button6 = ttk.Button(self.UI)
        button6.configure(text='Bestiary', width=20)
        button6.pack(side="top")
        button6.configure(command=self.Bestiary_action)

        # Main widget
        self.mainwindow = self.UI

    def run(self):
        self.mainwindow.mainloop()

    def new_char_action(self):
        # Create a file save dialog
        new_character = {
            "name": "Name",
            "class": "Class",
            "race": "Race"
        }

        # Create a list of editItem_options for the EditItemPopup
        prop_list = []
        for prop in new_character:
            this_itm = EditItem_Option(prop, new_character[prop])
            prop_list.append(this_itm)

        # Add custom rules
        for prop in prop_list:
            if prop.name == "class":
                prop.input_type = "av"
                prop.accepted_values = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
            

        # Create an EditItemPopup to get character information
        Popup.EditItemPopup(self.mainwindow, prop_list, self.new_char_callback)

    def new_char_callback(self, new_character):
        # Ensure that we got something back
        if(new_character is None):
            # If we didn't get anything back, the user either cancelled or deleted the new character
            # For some reason? I don't know why they would do that, but it's possible
            
            # For now, assume the user didn't actually want to create a new character,
            # show a message box to let them know that the new character was cancelled, and return
            Popup.Message("The new character creation was cancelled.")
            return
        
        # If the returned values are exactly the same as the default values, the user didn't change anything
        # Show a message box to let them know that the new character was cancelled, and return
        if new_character == {"name": "Name", "class": "Class", "race": "Race"}:
            Popup.Message("The new character creation was cancelled.")
            return
            
        # Create a new character sheet with the new character information

        # First, create all the other properties that are needed for a character sheet
        new_character["bonus_init"] = 0
        new_character["con"] = 10
        new_character["hp"] = 1
        new_character["hpMax"] = 1
        new_character["speed"] = 30
        new_character["spellAttack"] = 0
        new_character["dex"] = 10
        new_character["currency"] = [0, 0, 0, 0, 0]
        new_character["trackers"] = [{
            "name": "Hit Dice",
            "value": 1,
            "max_value": 1,
            "refresh": ""
        }]
        new_character["spells"] = []
        new_character["cha"] = 10
        new_character["info"] = ""
        new_character["wis"] = 10
        new_character["ac"] = 10
        new_character["lvl"] = 1
        new_character["weaponResource"] = 0
        new_character["spellDC"] = 0
        new_character["prof"] = 1
        new_character["int"] = 10
        new_character["cLevel"] = 0
        new_character["str"] = 10
        new_character["hitDieDR"] = "1d8"
        new_character["background"] = ""
        new_character["xp"] = 0
        new_character["spellSlotRefresh"] = ""
        new_character["spellSlotsLeft"] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        new_character["spellSlotsMax"] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        new_character["alignment"] = ""
        new_character["weapons"] = []
        new_character["abilities"] = {
            "athletics": 0,
            "acrobatics": 0,
            "sleightOfHand": 0,
            "stealth": 0,
            "arcana": 0,
            "history": 0,
            "investigation": 0,
            "nature": 0,
            "religion": 0,
            "animalHandling": 0,
            "insight": 0,
            "medicine": 0,
            "perception": 0,
            "survival": 0,
            "deception": 0,
            "intimidation": 0,
            "performance": 0,
            "persuasion": 0
        }

        # Create a file save dialog, with the default file name set to the character's name
        if(self.default_cs_loc is not None):
            file_path = filedialog.asksaveasfilename(initialdir=self.default_cs_loc, initialfile=new_character["name"] + ".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        else:
            file_path = filedialog.asksaveasfilename(initialdir="..", initialfile=new_character["name"] + ".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        # file_path = "./test_sheet.json"

        # Save the new character sheet to the selected file
        if file_path:
            CharacterSheet.write_json(file_path, new_character)
        else:
            # If the user cancelled the save dialog, show a message box to let them know that the new character was cancelled
            Popup.Message("The new character creation was cancelled.")
            return
        
        # Load the active character sheet ui with the new character sheet
        self.char_sheet = ActiveCharacterSheetUI(file_path)
        self.char_sheet.mainwindow.after(100, self.char_sheet.reload_ui)  # Schedule the reload_ui method to be called after the main loop starts
        self.char_sheet.run()

    def load_char_action(self):
        # Create a file open dialog
        if(self.default_cs_loc is not None):
            file_path = filedialog.askopenfilename(initialdir=self.default_cs_loc, filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        else:
            file_path = filedialog.askopenfilename(initialdir="..", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        # file_path = "./test_sheet.json"

        # Open the selected file
        if file_path:
            # Load the active character sheet ui with the selected file
            self.char_sheet = ActiveCharacterSheetUI(file_path)
            self.char_sheet.mainwindow.after(100, self.char_sheet.reload_ui)  # Schedule the reload_ui method to be called after the main loop starts
            self.char_sheet.run()

    def roll_dice_action(self):
        self.dice_roll = DiceRollUI()
        self.dice_roll.run()

    def encounter_tracker_action(self):
        self.encounter_tracker = EncounterTracker()
        self.encounter_tracker.run()

    def Bestiary_action(self):
        pass


if __name__ == "__main__":
    default_cs_loc = None
    if "--def-cs-loc" in sys.argv:
        index = sys.argv.index("--def-cs-loc")
        if index + 1 < len(sys.argv):
            file_path = sys.argv[index + 1]
            if os.path.exists(file_path):
                default_cs_loc = file_path
            else:
                print(f"Error: File path '{file_path}' does not exist.")
                sys.exit(1)
        else:
            print("Error: Missing file path argument after --def-cs-loc.")
            sys.exit(1)

    app = MainUI(default_cs_loc=default_cs_loc)
    app.run()

