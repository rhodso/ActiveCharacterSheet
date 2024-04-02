#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
import math

from pygubu.widgets.scrolledframe import ScrolledFrame

from CharacterSheet import *
from Helpers import Helpers
from Popup import Popup
from Popup import EditItem_Option

class ActiveCharacterSheetUI:
# ---------------------------------------------------------------------
# Start of UI specific code
# ---------------------------------------------------------------------

    def __init__(self, character_sheet_fp=None):
        self.character = {}
        self.weapons_list = []
        self.spells_list = []
        self.trackers_list = []

        if(not character_sheet_fp is None):
            self.fp = character_sheet_fp

        # build ui
        master = None
        self.UI = tk.Tk() if master is None else tk.Toplevel(master)
        self.UI.configure(height=200, width=200)
        self.UI.title("D&D Active Character Sheet")

        # Header
        self.header_label = ttk.Label(self.UI)
        self.header_label.configure(
            anchor="nw",
            compound="left",
            font="{Sans} 20 {bold}",
            justify="center",
            state="normal",
            text='D&D Active Character Sheet',
            width=25)
        self.header_label.pack(side="top")
        self.acs_tabs_notebook = ttk.Notebook(self.UI)
        self.acs_tabs_notebook.configure(height=500, width=700)

        # Base Info Tab
        self.base_info_frame = ttk.Frame(self.acs_tabs_notebook)
        self.base_info_frame.configure(height=200, width=200)
        self.base_stats_frame = ttk.Labelframe(self.base_info_frame)
        self.base_stats_frame.configure(
            height=200,
            labelanchor="nw",
            text='Base Stats',
            width=300)
        
        # HP Frame
        self.hp_frame = ttk.Frame(self.base_stats_frame)
        self.hp_label = ttk.Label(self.hp_frame)
        self.hp_label.configure(font="{Sans} 14 {}", text='HP')
        self.hp_label.pack(side="top")
        self.hp_val_label = ttk.Label(self.hp_frame)
        self.hp_val_label.configure(font="{Sans} 11 {}")
        self.hp_val_label.pack(side="top")
        self.crhp_update_button = ttk.Button(self.hp_frame)
        self.crhp_update_button.configure(text='CR', width=3)
        self.crhp_update_button.pack(expand=False, side="left")
        self.crhp_update_button.configure(command=self.crhp_update_action)
        self.mxhp_update_button = ttk.Button(self.hp_frame)
        self.mxhp_update_button.configure(text='MX', width=3)
        self.mxhp_update_button.pack(side="right")
        self.mxhp_update_button.configure(command=self.mxhp_update_action)
        self.hp_frame.grid(column=0, row=0)

        # AC Frame
        self.ac_frame = ttk.Frame(self.base_stats_frame)
        self.ac_label = ttk.Label(self.ac_frame)
        self.ac_label.configure(font="{Sans} 14 {}", text='AC')
        self.ac_label.pack(side="top")
        self.ac_val_label = ttk.Label(self.ac_frame)
        self.ac_val_label.configure(font="{Sans} 11 {}", text='999')
        self.ac_val_label.pack(side="top")
        self.ac_update_label = ttk.Button(self.ac_frame)
        self.ac_update_label.configure(text='Update')
        self.ac_update_label.pack(side="top")
        self.ac_update_label.configure(command=self.ac_update_action)
        self.ac_frame.grid(column=1, row=0)

        # Speed Frame
        self.speed_frame = ttk.Frame(self.base_stats_frame)
        self.speed_label = ttk.Label(self.speed_frame)
        self.speed_label.configure(font="{Sans} 14 {}", text='Speed')
        self.speed_label.pack(side="top")
        self.speed_val_label = ttk.Label(self.speed_frame)
        self.speed_val_label.configure(font="{Sans} 11 {}", text='999 ft')
        self.speed_val_label.pack(side="top")
        self.speed_update_label = ttk.Button(self.speed_frame)
        self.speed_update_label.configure(text='Update')
        self.speed_update_label.pack(side="top")
        self.speed_update_label.configure(command=self.speed_update_action)
        self.speed_frame.grid(column=2, row=0)

        # Hit Dice Frame
        self.hit_dice_frame = ttk.Frame(self.base_stats_frame)
        self.hit_die_label = ttk.Label(self.hit_dice_frame)
        self.hit_die_label.configure(font="{Sans} 14 {}", text='Hit Dice')
        self.hit_die_label.pack(side="top")
        self.hit_die_val_label = ttk.Label(self.hit_dice_frame)
        self.hit_die_val_label.configure(font="TkMenuFont", text='1d99+99')
        self.hit_die_val_label.pack(side="top")
        self.hit_die_update_button = ttk.Button(self.hit_dice_frame)
        self.hit_die_update_button.configure(text='Update')
        self.hit_die_update_button.pack(side="top")
        self.hit_die_update_button.configure(command=self.hit_dice_update_action)
        self.hit_dice_frame.grid(column=3, row=0)

        # Proficiency Frame
        self.prof_frame = ttk.Frame(self.base_stats_frame)
        self.prof_label = ttk.Label(self.prof_frame)
        self.prof_label.configure(font="{Sans} 14 {}", text='Prof.')
        self.prof_label.pack(side="top")
        self.prof_val_label = ttk.Label(self.prof_frame)
        self.prof_val_label.configure(font="{Sans} 11 {}", text='+999')
        self.prof_val_label.pack(side="top")
        self.prof_update_button = ttk.Button(self.prof_frame)
        self.prof_update_button.configure(text='Update')
        self.prof_update_button.pack(side="top")
        self.prof_update_button.configure(command=self.prof_update_action)
        self.prof_frame.grid(column=4, row=0)

        # Initiative Frame
        self.initiative_frame = ttk.Frame(self.base_stats_frame)
        self.init_label = ttk.Label(self.initiative_frame)
        self.init_label.configure(font="{Sans} 14 {}", text='Initiative')
        self.init_label.pack(side="top")
        self.init_val_label = ttk.Label(self.initiative_frame)
        self.init_val_label.configure(font="{Sans} 11 {}", text='999')
        self.init_val_label.pack(side="top")
        self.init_update_button = ttk.Button(self.initiative_frame)
        self.init_update_button.configure(text='Update')
        self.init_update_button.pack(side="top")
        self.init_update_button.configure(command=self.init_update_action)
        self.initiative_frame.grid(column=5, row=0)
        self.base_stats_frame.place(anchor="nw", height=100, width=500, x=10, y=10)
        self.base_stats_frame.columnconfigure(0, pad=5)
        self.base_stats_frame.columnconfigure("all", pad=7)

        # Common Actions Frame
        self.common_actions_frame = ttk.Labelframe(self.base_info_frame)
        self.common_actions_frame.configure(text='Common Actions')

        # Short Rest Button
        self.short_rest_button = ttk.Button(self.common_actions_frame)
        self.short_rest_button.configure(text='Short Rest', width=25)
        self.short_rest_button.pack(side="top")
        self.short_rest_button.configure(command=self.short_rest_action)

        # Long Rest Button
        self.long_rest_button = ttk.Button(self.common_actions_frame)
        self.long_rest_button.configure(text='Long Rest', width=25)
        self.long_rest_button.pack(side="top")
        self.long_rest_button.configure(command=self.long_rest_action)

        # Roll Initiative Button
        self.init_roll_button = ttk.Button(self.common_actions_frame)
        self.init_roll_button.configure(text='Roll Initiative!', width=25)
        self.init_roll_button.configure(command=self.init_roll_action)
        self.init_roll_button.pack(side="top")
        self.common_actions_frame.place(
            anchor="ne", height=100, width=175, x=690, y=10)

        # Abilities Frame
        self.abilities_frame = ttk.Labelframe(self.base_info_frame)
        self.abilities_frame.configure(text='Abilities', width=200)
        self.strength_frame = ttk.Labelframe(self.abilities_frame)

        # Strength Frame
        self.strength_frame.configure(text='Strength')
        self.strength_score_header_label = ttk.Label(self.strength_frame)
        self.strength_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.strength_score_header_label.grid(column=0, row=0)
        self.strength_mod_header_label = ttk.Label(self.strength_frame)
        self.strength_mod_header_label.configure(
            font="{Sans} 8 {}", text='Mod')
        self.strength_mod_header_label.grid(column=1, row=0)
        self.strength_save_header_label = ttk.Label(self.strength_frame)
        self.strength_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.strength_save_header_label.grid(column=2, row=0)
        self.strength_score_label = ttk.Label(self.strength_frame)
        self.strength_score_label.configure(
            font="{Sans} 12 {}",
            text='999')
        self.strength_score_label.grid(column=0, row=1)
        self.strength_mod_label = ttk.Label(self.strength_frame)
        self.strength_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.strength_mod_label.grid(column=1, row=1)
        self.strength_save_label = ttk.Label(self.strength_frame)
        self.strength_save_label.configure(font="{Sans} 12 {}", text='+999')
        self.strength_save_label.grid(column=2, row=1)
        self.strength_update_button = ttk.Button(self.strength_frame)
        self.strength_update_button.configure(text='Update')
        self.strength_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.strength_update_button.configure(
            command=self.strength_update_action)
        self.strength_save_button = ttk.Button(self.strength_frame)
        self.strength_save_button.configure(text='Roll Save')
        self.strength_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.strength_save_button.configure(command=self.strength_save_action)
        self.strength_frame.grid(column=0, padx=5, pady=0, row=0)
        self.strength_frame.rowconfigure("all", pad=5)

        # Intelligence Frame
        self.intelligence_panel = ttk.Labelframe(self.abilities_frame)
        self.intelligence_panel.configure(text='Intelligence')
        self.intelligence_score_header_label = ttk.Label(
            self.intelligence_panel)
        self.intelligence_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.intelligence_score_header_label.grid(column=0, row=0)
        self.intelligence_mod_header_label = ttk.Label(self.intelligence_panel)
        self.intelligence_mod_header_label.configure(
            font="{Sans} 8 {}", text='Mod')
        self.intelligence_mod_header_label.grid(column=1, row=0)
        self.intelligence_save_header_label = ttk.Label(
            self.intelligence_panel)
        self.intelligence_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.intelligence_save_header_label.grid(column=2, row=0)
        self.intelligence_score_label = ttk.Label(self.intelligence_panel)
        self.intelligence_score_label.configure(
            font="{Sans} 12 {}",
            text='999')
        self.intelligence_score_label.grid(column=0, row=1)
        self.intelligence_mod_label = ttk.Label(self.intelligence_panel)
        self.intelligence_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.intelligence_mod_label.grid(column=1, row=1)
        self.intelligence_save_label = ttk.Label(self.intelligence_panel)
        self.intelligence_save_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.intelligence_save_label.grid(column=2, row=1)
        self.intelligence_update_button = ttk.Button(self.intelligence_panel)
        self.intelligence_update_button.configure(text='Update')
        self.intelligence_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.intelligence_update_button.configure(
            command=self.intelligence_update_action)
        self.intelligence_save_button = ttk.Button(self.intelligence_panel)
        self.intelligence_save_button.configure(text='Roll Save')
        self.intelligence_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.intelligence_save_button.configure(
            command=self.intelligence_save_action)
        self.intelligence_panel.grid(column=1, padx=5, pady=0, row=0)
        self.intelligence_panel.rowconfigure(0, pad=5)
        self.intelligence_panel.rowconfigure("all", pad=5)

        # Dexterity Frame
        self.dexterity_panel = ttk.Labelframe(self.abilities_frame)
        self.dexterity_panel.configure(text='Dexterity')
        self.dexterity_score_header_label = ttk.Label(self.dexterity_panel)
        self.dexterity_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.dexterity_score_header_label.grid(column=0, row=0)
        self.dexterity_mod_header_label = ttk.Label(self.dexterity_panel)
        self.dexterity_mod_header_label.configure(
            font="{Sans} 8 {}", text='Mod')
        self.dexterity_mod_header_label.grid(column=1, row=0)
        self.dexterity_save_header_label = ttk.Label(self.dexterity_panel)
        self.dexterity_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.dexterity_save_header_label.grid(column=2, row=0)
        self.dexterity_score_label = ttk.Label(self.dexterity_panel)
        self.dexterity_score_label.configure(
            font="{Sans} 12 {}",
            text='999')
        self.dexterity_score_label.grid(column=0, row=1)
        self.dexterity_mod_label = ttk.Label(self.dexterity_panel)
        self.dexterity_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.dexterity_mod_label.grid(column=1, row=1)
        self.dexterity_save_label = ttk.Label(self.dexterity_panel)
        self.dexterity_save_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.dexterity_save_label.grid(column=2, row=1)
        self.dexterity_update_button = ttk.Button(self.dexterity_panel)
        self.dexterity_update_button.configure(text='Update')
        self.dexterity_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.dexterity_update_button.configure(
            command=self.dexterity_update_action)
        self.dexterity_save_button = ttk.Button(self.dexterity_panel)
        self.dexterity_save_button.configure(text='Roll Save')
        self.dexterity_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.dexterity_save_button.configure(
            command=self.dexterity_save_action)
        self.dexterity_panel.grid(column=0, padx=5, pady=0, row=1)
        self.dexterity_panel.rowconfigure(0, pad=5)
        self.dexterity_panel.rowconfigure("all", pad=5)

        # Wisdom Frame
        self.wisdom_panel = ttk.Labelframe(self.abilities_frame)
        self.wisdom_panel.configure(text='Wisdom')
        self.wisdom_score_header_label = ttk.Label(self.wisdom_panel)
        self.wisdom_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.wisdom_score_header_label.grid(column=0, row=0)
        self.wisdom_mod_header_label = ttk.Label(self.wisdom_panel)
        self.wisdom_mod_header_label.configure(font="{Sans} 8 {}", text='Mod')
        self.wisdom_mod_header_label.grid(column=1, row=0)
        self.wisdom_save_header_label = ttk.Label(self.wisdom_panel)
        self.wisdom_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.wisdom_save_header_label.grid(column=2, row=0)
        self.wisdom_score_label = ttk.Label(self.wisdom_panel)
        self.wisdom_score_label.configure(
            font="{Sans} 12 {}",
            text='999')
        self.wisdom_score_label.grid(column=0, row=1)
        self.wisdom_mod_label = ttk.Label(self.wisdom_panel)
        self.wisdom_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.wisdom_mod_label.grid(column=1, row=1)
        self.wisdom_save_label = ttk.Label(self.wisdom_panel)
        self.wisdom_save_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.wisdom_save_label.grid(column=2, row=1)
        self.wisdom_update_button = ttk.Button(self.wisdom_panel)
        self.wisdom_update_button.configure(text='Update')
        self.wisdom_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.wisdom_update_button.configure(command=self.wisdom_update_action)
        self.wisdom_save_button = ttk.Button(self.wisdom_panel)
        self.wisdom_save_button.configure(text='Roll Save')
        self.wisdom_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.wisdom_save_button.configure(command=self.wisdom_save_action)
        self.wisdom_panel.grid(column=1, padx=5, pady=0, row=1)
        self.wisdom_panel.rowconfigure(0, pad=5)
        self.wisdom_panel.rowconfigure("all", pad=5)

        # Constitution Frame
        self.constitution_panel = ttk.Labelframe(self.abilities_frame)
        self.constitution_panel.configure(text='Constitution')
        self.constitution_score_header_label = ttk.Label(
            self.constitution_panel)
        self.constitution_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.constitution_score_header_label.grid(column=0, row=0)
        self.constitution_mod_header_label = ttk.Label(self.constitution_panel)
        self.constitution_mod_header_label.configure(
            font="{Sans} 8 {}", text='Mod')
        self.constitution_mod_header_label.grid(column=1, row=0)
        self.constitution_save_header_label = ttk.Label(
            self.constitution_panel)
        self.constitution_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.constitution_save_header_label.grid(column=2, row=0)
        self.constitution_score_label = ttk.Label(self.constitution_panel)
        self.constitution_score_label.configure(
            font="{Sans} 12 {}", text='999')
        self.constitution_score_label.grid(column=0, row=1)
        self.constitution_mod_label = ttk.Label(self.constitution_panel)
        self.constitution_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.constitution_mod_label.grid(column=1, row=1)
        self.constitution_save_label = ttk.Label(self.constitution_panel)
        self.constitution_save_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.constitution_save_label.grid(column=2, row=1)
        self.constitution_update_button = ttk.Button(self.constitution_panel)
        self.constitution_update_button.configure(text='Update')
        self.constitution_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.constitution_update_button.configure(
            command=self.constitution_update_action)
        self.constitution_save_button = ttk.Button(self.constitution_panel)
        self.constitution_save_button.configure(text='Roll Save')
        self.constitution_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.constitution_save_button.configure(
            command=self.constitution_save_action)
        self.constitution_panel.grid(column=0, padx=5, pady=0, row=2)
        self.constitution_panel.rowconfigure(0, pad=5)
        self.constitution_panel.rowconfigure("all", pad=5)

        # Charisma Frame
        self.charisma_panel = ttk.Labelframe(self.abilities_frame)
        self.charisma_panel.configure(text='Charisma')
        self.charisma_score_header_label = ttk.Label(self.charisma_panel)
        self.charisma_score_header_label.configure(
            font="{sans} 8 {}", text='Score')
        self.charisma_score_header_label.grid(column=0, row=0)
        self.charisma_mod_header_label = ttk.Label(self.charisma_panel)
        self.charisma_mod_header_label.configure(
            font="{Sans} 8 {}", text='Mod')
        self.charisma_mod_header_label.grid(column=1, row=0)
        self.charisma_save_header_label = ttk.Label(self.charisma_panel)
        self.charisma_save_header_label.configure(
            font="{Sans} 8 {}", text='Save')
        self.charisma_save_header_label.grid(column=2, row=0)
        self.charisma_score_label = ttk.Label(self.charisma_panel)
        self.charisma_score_label.configure(
            font="{Sans} 12 {}", text='999')
        self.charisma_score_label.grid(column=0, row=1)
        self.charisma_mod_label = ttk.Label(self.charisma_panel)
        self.charisma_mod_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.charisma_mod_label.grid(column=1, row=1)
        self.charisma_save_label = ttk.Label(self.charisma_panel)
        self.charisma_save_label.configure(
            font="{Sans} 12 {}",
            text='+999')
        self.charisma_save_label.grid(column=2, row=1)
        self.charisma_update_button = ttk.Button(self.charisma_panel)
        self.charisma_update_button.configure(text='Update')
        self.charisma_update_button.grid(column=0, padx=1, pady=1, row=2)
        self.charisma_update_button.configure(
            command=self.charisma_update_action)
        self.charisma_save_button = ttk.Button(self.charisma_panel)
        self.charisma_save_button.configure(text='Roll Save')
        self.charisma_save_button.grid(column=2, padx=1, pady=1, row=2)
        self.charisma_save_button.configure(command=self.charisma_save_action)
        self.charisma_panel.grid(column=1, padx=5, pady=0, row=2)
        self.charisma_panel.rowconfigure(0, pad=5)
        self.charisma_panel.rowconfigure("all", pad=5)
        self.abilities_frame.place(
            anchor="nw", height=380, width=425, x=10, y=115)
        self.abilities_frame.rowconfigure("all", pad=17)

        # Trackers Frame
        self.trackers_frame = ttk.Labelframe(self.base_info_frame)
        self.trackers_frame.configure(height=200, text='Trackers', width=300)

        # Trackers Scroll Frame, updated dynamically with the ui_reload function
        self.trackers_scroll_frame = ScrolledFrame(
            self.trackers_frame, scrolltype="vertical")
        self.trackers_scroll_frame.configure(usemousewheel=False)
        self.trackers_scroll_frame.place(
            anchor="nw", height=325, width=240, x=1, y=1)
        
        # Trackers Update Button
        self.trackers_update_button = ttk.Button(self.trackers_frame)
        self.trackers_update_button.configure(text='Update Trackers', width=25)
        self.trackers_update_button.place(anchor="s", x=125, y=355)
        self.trackers_update_button.configure(
            command=self.trackers_update_action)
        self.trackers_frame.place(
            anchor="ne", height=380, width=250, x=690, y=115)
        self.base_info_frame.pack(fill="both", side="top")

        # Ability Check Tab
        self.acs_tabs_notebook.add(self.base_info_frame, text='Base Info')
        frame2 = ttk.Frame(self.acs_tabs_notebook)
        frame2.configure(height=200, width=200)

        # Strength Ability Check Frame
        self.strength_abchk_frame = ttk.Labelframe(frame2)
        self.strength_abchk_frame.configure(
            height=200, text='Strength Abilities')
        self.strength_ = ttk.Frame(self.strength_abchk_frame)
        self.strength_.configure(height=25, width=240)
        self.strength_abchk_header_label = ttk.Label(self.strength_)
        self.strength_abchk_header_label.configure(text='Strength')
        self.strength_abchk_header_label.place(anchor="w", x=1, y=12)
        self.strength_abchk_value_label = ttk.Label(self.strength_)
        self.strength_abchk_value_label.configure(text='+99')
        self.strength_abchk_value_label.place(anchor="w", x=100, y=12)
        self.str_abchk_button = ttk.Button(self.strength_)
        self.str_abchk_button.configure(text='Roll')
        self.str_abchk_button.place(anchor="e", x=205, y=12)
        self.str_abchk_button.configure(command=lambda: self.abchk_action('str'))
        self.strength_.pack(side="top")
        self.frame81 = ttk.Frame(self.strength_abchk_frame)
        self.frame81.configure(height=25, width=240)
        self.athletics_abchk_header_label = ttk.Label(self.frame81)
        self.athletics_abchk_header_label.configure(text='Athletics')
        self.athletics_abchk_header_label.place(anchor="w", x=1, y=12)
        self.athletics_abchk_value_label = ttk.Label(self.frame81)
        self.athletics_abchk_value_label.configure(text='+99')
        self.athletics_abchk_value_label.place(anchor="w", x=100, y=12)
        self.athletics_abchk_button = ttk.Button(self.frame81)
        self.athletics_abchk_button.configure(text='Roll')
        self.athletics_abchk_button.place(anchor="e", x=205, y=12)
        self.athletics_abchk_button.configure(command=lambda: self.abchk_action('athletics'))
        self.frame81.pack(side="top")
        self.strength_abchk_frame.place(anchor="ne", width=210, x=340, y=10)

        # Dexterity Ability Check Frame
        self.dexterity_abchk_frame = ttk.Labelframe(frame2)
        self.dexterity_abchk_frame.configure(
            height=200, text='Dexterity Abilities', width=200)
        self.frame97 = ttk.Frame(self.dexterity_abchk_frame)
        self.frame97.configure(height=25, width=240)
        self.dex_abchk_header_label = ttk.Label(self.frame97)
        self.dex_abchk_header_label.configure(text='Dexterity')
        self.dex_abchk_header_label.place(anchor="w", x=1, y=12)
        self.dex_abchk_value_label = ttk.Label(self.frame97)
        self.dex_abchk_value_label.configure(text='+99')
        self.dex_abchk_value_label.place(anchor="w", x=100, y=12)
        self.dex_abchk_button = ttk.Button(self.frame97)
        self.dex_abchk_button.configure(text='Roll')
        self.dex_abchk_button.place(anchor="e", x=205, y=12)
        self.dex_abchk_button.configure(command=lambda: self.abchk_action('dex'))
        self.frame97.pack(side="top")
        self.frame98 = ttk.Frame(self.dexterity_abchk_frame)
        self.frame98.configure(height=25, width=240)
        self.acrobatics_abchk_header_label = ttk.Label(self.frame98)
        self.acrobatics_abchk_header_label.configure(text='Acrobatics')
        self.acrobatics_abchk_header_label.place(anchor="w", x=1, y=12)
        self.acrobatics_abchk_value_label = ttk.Label(self.frame98)
        self.acrobatics_abchk_value_label.configure(text='+99')
        self.acrobatics_abchk_value_label.place(anchor="w", x=100, y=12)
        self.acrobatics_abchk_button = ttk.Button(self.frame98)
        self.acrobatics_abchk_button.configure(text='Roll')
        self.acrobatics_abchk_button.place(anchor="e", x=205, y=12)
        self.acrobatics_abchk_button.configure(command=lambda: self.abchk_action('acrobatics'))
        self.frame98.pack(side="top")
        self.frame99 = ttk.Frame(self.dexterity_abchk_frame)
        self.frame99.configure(height=25, width=240)
        self.sleight_of_hand_abchk_header_label = ttk.Label(self.frame99)
        self.sleight_of_hand_abchk_header_label.configure(text='Sleight of Hand')
        self.sleight_of_hand_abchk_header_label.place(anchor="w", x=1, y=12)
        self.sleight_of_hand_abchk_value_label = ttk.Label(self.frame99)
        self.sleight_of_hand_abchk_value_label.configure(text='+99')
        self.sleight_of_hand_abchk_value_label.place(anchor="w", x=100, y=12)
        self.sleight_of_hand_abchk_button = ttk.Button(self.frame99)
        self.sleight_of_hand_abchk_button.configure(text='Roll')
        self.sleight_of_hand_abchk_button.place(anchor="e", x=205, y=12)
        self.sleight_of_hand_abchk_button.configure(command=lambda: self.abchk_action('sleightOfHand'))
        self.frame99.pack(side="top")
        self.frame100 = ttk.Frame(self.dexterity_abchk_frame)
        self.frame100.configure(height=25, width=240)
        self.stealth_abchk_header_label = ttk.Label(self.frame100)
        self.stealth_abchk_header_label.configure(text='Stealth')
        self.stealth_abchk_header_label.place(anchor="w", x=1, y=12)
        self.stealth_abchk_value_label = ttk.Label(self.frame100)
        self.stealth_abchk_value_label.configure(text='+99')
        self.stealth_abchk_value_label.place(anchor="w", x=100, y=12)
        self.stealth_abchk_button = ttk.Button(self.frame100)
        self.stealth_abchk_button.configure(text='Roll')
        self.stealth_abchk_button.place(anchor="e", x=205, y=12)
        self.stealth_abchk_button.configure(command=lambda: self.abchk_action('stealth'))
        self.frame100.pack(side="top")
        self.dexterity_abchk_frame.place(anchor="ne", width=210, x=340, y=90)

        # Intelligence Ability Check Frame
        self.intelligence_abchk_frame = ttk.Labelframe(frame2)
        self.intelligence_abchk_frame.configure(
            height=200, text='Intelligence Abilities', width=200)
        self.frame92 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame92.configure(height=25, width=240)
        self.intelligence_abchk_header_label = ttk.Label(self.frame92)
        self.intelligence_abchk_header_label.configure(text='Intelligence')
        self.intelligence_abchk_header_label.place(anchor="w", x=1, y=12)
        self.intelligence_abchk_value_label = ttk.Label(self.frame92)
        self.intelligence_abchk_value_label.configure(text='+99')
        self.intelligence_abchk_value_label.place(anchor="w", x=100, y=12)
        self.intelligence_abchk_button = ttk.Button(self.frame92)
        self.intelligence_abchk_button.configure(text='Roll')
        self.intelligence_abchk_button.place(anchor="e", x=205, y=12)
        self.intelligence_abchk_button.configure(command=lambda: self.abchk_action('int'))
        self.frame92.pack(side="top")
        self.frame93 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame93.configure(height=25, width=240)
        self.arcana_abchk_header_label = ttk.Label(self.frame93)
        self.arcana_abchk_header_label.configure(text='Arcana')
        self.arcana_abchk_header_label.place(anchor="w", x=1, y=12)
        self.arcana_abchk_value_label = ttk.Label(self.frame93)
        self.arcana_abchk_value_label.configure(text='+99')
        self.arcana_abchk_value_label.place(anchor="w", x=100, y=12)
        self.arcana_abchk_button = ttk.Button(self.frame93)
        self.arcana_abchk_button.configure(text='Roll')
        self.arcana_abchk_button.place(anchor="e", x=205, y=12)
        self.arcana_abchk_button.configure(command=lambda: self.abchk_action('arcana'))
        self.frame93.pack(side="top")
        self.frame94 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame94.configure(height=25, width=240)
        self.history_abchk_header_label = ttk.Label(self.frame94)
        self.history_abchk_header_label.configure(text='History')
        self.history_abchk_header_label.place(anchor="w", x=1, y=12)
        self.history_abchk_value_label = ttk.Label(self.frame94)
        self.history_abchk_value_label.configure(text='+99')
        self.history_abchk_value_label.place(anchor="w", x=100, y=12)
        self.history_abchk_button = ttk.Button(self.frame94)
        self.history_abchk_button.configure(text='Roll')
        self.history_abchk_button.place(anchor="e", x=205, y=12)
        self.history_abchk_button.configure(command=lambda: self.abchk_action('history'))
        self.frame94.pack(side="top")
        self.frame95 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame95.configure(height=25, width=240)
        self.investigation_abchk_header_label = ttk.Label(self.frame95)
        self.investigation_abchk_header_label.configure(text='Investigation')
        self.investigation_abchk_header_label.place(anchor="w", x=1, y=12)
        self.investigation_abchk_value_label = ttk.Label(self.frame95)
        self.investigation_abchk_value_label.configure(text='+99')
        self.investigation_abchk_value_label.place(anchor="w", x=100, y=12)
        self.investigation_abchk_button = ttk.Button(self.frame95)
        self.investigation_abchk_button.configure(text='Roll')
        self.investigation_abchk_button.place(anchor="e", x=205, y=12)
        self.investigation_abchk_button.configure(command=lambda: self.abchk_action('investigation'))
        self.frame95.pack(side="top")
        self.frame96 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame96.configure(height=25, width=240)
        self.nature_abchk_header_label = ttk.Label(self.frame96)
        self.nature_abchk_header_label.configure(text='Nature')
        self.nature_abchk_header_label.place(anchor="w", x=1, y=12)
        self.nature_abchk_value_label = ttk.Label(self.frame96)
        self.nature_abchk_value_label.configure(text='+99')
        self.nature_abchk_value_label.place(anchor="w", x=100, y=12)
        self.nature_abchk_button = ttk.Button(self.frame96)
        self.nature_abchk_button.configure(text='Roll')
        self.nature_abchk_button.place(anchor="e", x=205, y=12)
        self.nature_abchk_button.configure(command=lambda: self.abchk_action('nature'))
        self.frame96.pack(side="top")
        self.frame102 = ttk.Frame(self.intelligence_abchk_frame)
        self.frame102.configure(height=25, width=240)
        self.religion_abchk_header_label = ttk.Label(self.frame102)
        self.religion_abchk_header_label.configure(text='Religion')
        self.religion_abchk_header_label.place(anchor="w", x=1, y=12)
        self.religion_abchk_value_label = ttk.Label(self.frame102)
        self.religion_abchk_value_label.configure(text='+99')
        self.religion_abchk_value_label.place(anchor="w", x=100, y=12)
        self.religion_abchk_button = ttk.Button(self.frame102)
        self.religion_abchk_button.configure(text='Roll')
        self.religion_abchk_button.place(anchor="e", x=205, y=12)
        self.religion_abchk_button.configure(command=lambda: self.abchk_action('religion'))
        self.frame102.pack(side="top")
        self.intelligence_abchk_frame.place(
        anchor="ne", width=210, x=340, y=220)

        # Wisdom Ability Check Frame
        self.wisdom_abchk_frame = ttk.Labelframe(frame2)
        self.wisdom_abchk_frame.configure(text='Wisdom Abilities')
        self.frame87 = ttk.Frame(self.wisdom_abchk_frame)
        self.frame87.configure(height=25, width=240)
        self.wisdom_abchk_header_label = ttk.Label(self.frame87)
        self.wisdom_abchk_header_label.configure(text='Wisdom')
        self.wisdom_abchk_header_label.place(anchor="w", x=1, y=12)
        self.wisdom_abchk_value_label = ttk.Label(self.frame87)
        self.wisdom_abchk_value_label.configure(text='+99')
        self.wisdom_abchk_value_label.place(anchor="w", x=100, y=12)
        self.wis_abchk_button = ttk.Button(self.frame87)
        self.wis_abchk_button.configure(text='Roll')
        self.wis_abchk_button.place(anchor="e", x=205, y=12)
        self.wis_abchk_button.configure(command=lambda: self.abchk_action('wis'))
        self.frame87.pack(side="top")
        self.ah_abchk_frame = ttk.Frame(self.wisdom_abchk_frame)
        self.ah_abchk_frame.configure(height=25, width=240)
        self.animal_handling_abchk_header_label = ttk.Label(self.ah_abchk_frame)
        self.animal_handling_abchk_header_label.configure(text='Animal Handling')
        self.animal_handling_abchk_header_label.place(anchor="w", x=1, y=12)
        self.animal_handling_abchk_value_label = ttk.Label(self.ah_abchk_frame)
        self.animal_handling_abchk_value_label.configure(text='+99')
        self.animal_handling_abchk_value_label.place(anchor="w", x=100, y=12)
        self.animalHandling_abchk_button = ttk.Button(self.ah_abchk_frame)
        self.animalHandling_abchk_button.configure(text='Roll')
        self.animalHandling_abchk_button.place(anchor="e", x=205, y=12)
        self.animalHandling_abchk_button.configure(command=lambda: self.abchk_action('animalHandling'))
        self.ah_abchk_frame.pack(side="top")
        self.frame89 = ttk.Frame(self.wisdom_abchk_frame)
        self.frame89.configure(height=25, width=240)
        self.insight_abchk_header_label = ttk.Label(self.frame89)
        self.insight_abchk_header_label.configure(text='Insight')
        self.insight_abchk_header_label.place(anchor="w", x=1, y=12)
        self.insight_abchk_value_label = ttk.Label(self.frame89)
        self.insight_abchk_value_label.configure(text='+99')
        self.insight_abchk_value_label.place(anchor="w", x=100, y=12)
        self.insight_abchk_button = ttk.Button(self.frame89)
        self.insight_abchk_button.configure(text='Roll')
        self.insight_abchk_button.place(anchor="e", x=205, y=12)
        self.insight_abchk_button.configure(command=lambda: self.abchk_action('insight'))
        self.frame89.pack(side="top")
        self.frame90 = ttk.Frame(self.wisdom_abchk_frame)
        self.frame90.configure(height=25, width=240)
        self.medicine_abchk_header_label = ttk.Label(self.frame90)
        self.medicine_abchk_header_label.configure(text='Medicine')
        self.medicine_abchk_header_label.place(anchor="w", x=1, y=12)
        self.medicine_abchk_value_label = ttk.Label(self.frame90)
        self.medicine_abchk_value_label.configure(text='+99')
        self.medicine_abchk_value_label.place(anchor="w", x=100, y=12)
        self.medicine_abchk_button = ttk.Button(self.frame90)
        self.medicine_abchk_button.configure(text='Roll')
        self.medicine_abchk_button.place(anchor="e", x=205, y=12)
        self.medicine_abchk_button.configure(command=lambda: self.abchk_action('medicine'))
        self.frame90.pack(side="top")
        self.frame91 = ttk.Frame(self.wisdom_abchk_frame)
        self.frame91.configure(height=25, width=240)
        self.perception_abchk_header_label = ttk.Label(self.frame91)
        self.perception_abchk_header_label.configure(text='Perception\t')
        self.perception_abchk_header_label.place(anchor="w", x=1, y=12)
        self.perception_abchk_value_label = ttk.Label(self.frame91)
        self.perception_abchk_value_label.configure(text='+99')
        self.perception_abchk_value_label.place(anchor="w", x=100, y=12)
        self.perception_abchk_button = ttk.Button(self.frame91)
        self.perception_abchk_button.configure(text='Roll')
        self.perception_abchk_button.place(anchor="e", x=205, y=12)
        self.perception_abchk_button.configure(command=lambda: self.abchk_action('perception'))
        self.frame91.pack(side="top")
        self.frame101 = ttk.Frame(self.wisdom_abchk_frame)
        self.frame101.configure(height=25, width=240)
        self.survival_abchk_header_label = ttk.Label(self.frame101)
        self.survival_abchk_header_label.configure(text='Survival')
        self.survival_abchk_header_label.place(anchor="w", x=1, y=12)
        self.survival_abchk_value_label = ttk.Label(self.frame101)
        self.survival_abchk_value_label.configure(text='+99')
        self.survival_abchk_value_label.place(anchor="w", x=100, y=12)
        self.survival_abchk_button = ttk.Button(self.frame101)
        self.survival_abchk_button.configure(text='Roll')
        self.survival_abchk_button.place(anchor="e", x=205, y=12)
        self.survival_abchk_button.configure(command=lambda: self.abchk_action('survival'))
        self.frame101.pack(side="top")
        self.wisdom_abchk_frame.place(anchor="nw", width=210, x=350, y=10)

        # Charisma Ability Check Frame
        self.charisma_abchk_frame = ttk.Labelframe(frame2)
        self.charisma_abchk_frame.configure(
            height=200, text='Charisma Abilities', width=200)
        self.frame82 = ttk.Frame(self.charisma_abchk_frame)
        self.frame82.configure(height=25, width=240)
        self.charisma_abchk_header_label = ttk.Label(self.frame82)
        self.charisma_abchk_header_label.configure(text='Charisma')
        self.charisma_abchk_header_label.place(anchor="w", x=1, y=12)
        self.charisma_abchk_value_label = ttk.Label(self.frame82)
        self.charisma_abchk_value_label.configure(text='+99')
        self.charisma_abchk_value_label.place(anchor="w", x=100, y=12)
        self.charisma_abchk_button = ttk.Button(self.frame82)
        self.charisma_abchk_button.configure(text='Roll')
        self.charisma_abchk_button.place(anchor="e", x=205, y=12)
        self.charisma_abchk_button.configure(command=lambda: self.abchk_action('cha'))
        self.frame82.pack(side="top")
        self.frame83 = ttk.Frame(self.charisma_abchk_frame)
        self.frame83.configure(height=25, width=240)
        self.deception_abchk_header_label = ttk.Label(self.frame83)
        self.deception_abchk_header_label.configure(text='Deception')
        self.deception_abchk_header_label.place(anchor="w", x=1, y=12)
        self.deception_abchk_value_label = ttk.Label(self.frame83)
        self.deception_abchk_value_label.configure(text='+99')
        self.deception_abchk_value_label.place(anchor="w", x=100, y=12)
        self.deception_abchk_button = ttk.Button(self.frame83)
        self.deception_abchk_button.configure(text='Roll')
        self.deception_abchk_button.place(anchor="e", x=205, y=12)
        self.deception_abchk_button.configure(command=lambda: self.abchk_action('deception'))
        self.frame83.pack(side="top")
        self.frame84 = ttk.Frame(self.charisma_abchk_frame)
        self.frame84.configure(height=25, width=240)
        self.intimidation_abchk_header_label = ttk.Label(self.frame84)
        self.intimidation_abchk_header_label.configure(text='Intimidation')
        self.intimidation_abchk_header_label.place(anchor="w", x=1, y=12)
        self.intimidation_abchk_value_label = ttk.Label(self.frame84)
        self.intimidation_abchk_value_label.configure(text='+99')
        self.intimidation_abchk_value_label.place(anchor="w", x=100, y=12)
        self.intimidation_abchk_button = ttk.Button(self.frame84)
        self.intimidation_abchk_button.configure(text='Roll')
        self.intimidation_abchk_button.place(anchor="e", x=205, y=12)
        self.intimidation_abchk_button.configure(command=lambda: self.abchk_action('intimidation'))
        self.frame84.pack(side="top")
        self.frame85 = ttk.Frame(self.charisma_abchk_frame)
        self.frame85.configure(height=25, width=240)
        self.performance_abchk_header_label = ttk.Label(self.frame85)
        self.performance_abchk_header_label.configure(text='Performance')
        self.performance_abchk_header_label.place(anchor="w", x=1, y=12)
        self.performance_abchk_value_label = ttk.Label(self.frame85)
        self.performance_abchk_value_label.configure(text='+99')
        self.performance_abchk_value_label.place(anchor="w", x=100, y=12)
        self.performance_abchk_button = ttk.Button(self.frame85)
        self.performance_abchk_button.configure(text='Roll')
        self.performance_abchk_button.place(anchor="e", x=205, y=12)
        self.performance_abchk_button.configure(command=lambda: self.abchk_action('performance'))
        self.frame85.pack(side="top")
        self.frame86 = ttk.Frame(self.charisma_abchk_frame)
        self.frame86.configure(height=25, width=240)
        self.persuasion_abchk_header_label = ttk.Label(self.frame86)
        self.persuasion_abchk_header_label.configure(text='Persuasion')
        self.persuasion_abchk_header_label.place(anchor="w", x=1, y=12)
        self.persuasion_abchk_value_label = ttk.Label(self.frame86)
        self.persuasion_abchk_value_label.configure(text='+99')
        self.persuasion_abchk_value_label.place(anchor="w", x=100, y=12)
        self.persuasion_abchk_button = ttk.Button(self.frame86)
        self.persuasion_abchk_button.configure(text='Roll')
        self.persuasion_abchk_button.place(anchor="e", x=205, y=12)
        self.persuasion_abchk_button.configure(command=lambda: self.abchk_action('persuasion'))
        self.frame86.pack(side="top")
        self.frame86.pack(side="top")
        self.charisma_abchk_frame.place(anchor="nw", width=210, x=350, y=190)

        # Update abilities button
        self.abilities_update_button = ttk.Button(frame2)
        self.abilities_update_button.configure(
            text='Update Abilities',
            command=self.abilities_update_action)
        self.abilities_update_button.place(anchor="se", x=550, y=455)

        frame2.pack(side="top")
        self.acs_tabs_notebook.add(frame2, text='Abilities')

        # Weapons Tab
        frame3 = ttk.Frame(self.acs_tabs_notebook)
        frame3.configure(height=200, width=200)
        self.weapons_frame = ttk.Frame(frame3)
        self.weapons_frame.configure(height=490, padding=0, width=200)
        self.weapons_update_button = ttk.Button(self.weapons_frame)
        self.weapons_update_button.configure(text='Update List')
        self.weapons_update_button.place(anchor="ne", x=685, y=5)
        self.weapons_update_button.configure(
            command=self.weapons_update_action)
        self.weapons_list_frame = ttk.Labelframe(self.weapons_frame)
        self.weapons_list_frame.configure(
            height=200, text='Weapons List', width=200)
        self.weapons_scroll_frame = ScrolledFrame(
            self.weapons_list_frame, scrolltype="vertical")
        self.weapons_scroll_frame.configure(usemousewheel=False)
        
        # Weapons Scroll Frame, updated dynamically with the ui_reload function
        self.weapons_scroll_display_frame = ttk.Frame(self.weapons_scroll_frame.innerframe)
        self.weapons_scroll_display_frame.configure(height=200, width=200)
        self.weapons_scroll_display_frame.pack(expand=True, fill="both", side="top")
        self.weapons_scroll_frame.pack(expand=True, fill="both", side="top")
        self.weapons_list_frame.place(
            anchor="nw", height=460, width=680, x=0, y=30)
        self.weapons_frame.place(anchor="nw", width=690, x=5, y=5)
        frame3.pack(side="top")
        self.acs_tabs_notebook.add(frame3, text='Weapons')

        # Spells Tab
        frame4 = ttk.Frame(self.acs_tabs_notebook)
        frame4.configure(height=200, width=200)
        self.spells_frame = ttk.Frame(frame4)
        self.spells_frame.configure(height=490, padding=0, width=200)
        
        # Spell slots frame
        self.spell_slot_fram = ttk.Frame(self.spells_frame)
        self.spell_slot_fram.configure(height=200, width=200)

        # Level 1 Spell Slots
        self.lvl1_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl1_frame.configure(height=95, width=70)
        self.lvl1_header_label = ttk.Label(self.lvl1_frame)
        self.lvl1_header_label.configure(text='Level 1')
        self.lvl1_header_label.pack(side="top")
        self.lvl1_add_button = ttk.Button(self.lvl1_frame)
        self.lvl1_add_button.configure(text='+')
        self.lvl1_add_button.pack(side="top")
        self.lvl1_add_button.configure(command=lambda: self.slot_add_action(0))
        self.lvl1_slots_label = ttk.Label(self.lvl1_frame)
        self.lvl1_slots_label.configure(
            font="{Sans} 14 {}",
            justify="left",
            text='99/99')
        self.lvl1_slots_label.pack(side="top")
        self.lvl1_subtract_button = ttk.Button(self.lvl1_frame)
        self.lvl1_subtract_button.configure(text='-')
        self.lvl1_subtract_button.pack(side="top")
        self.lvl1_subtract_button.configure(command=lambda: self.slot_subtract_action(0))
        self.lvl1_frame.grid(column=0, row=0)

        # Level 2 Spell Slots
        self.lvl2_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl2_frame.configure(height=95, width=70)
        self.lvl2_header_label = ttk.Label(self.lvl2_frame)
        self.lvl2_header_label.configure(text='Level 2')
        self.lvl2_header_label.pack(side="top")
        self.lvl2_add_button = ttk.Button(self.lvl2_frame)
        self.lvl2_add_button.configure(text='+')
        self.lvl2_add_button.pack(side="top")
        self.lvl2_add_button.configure(command=lambda: self.slot_add_action(1))
        self.lvl2_slots_label = ttk.Label(self.lvl2_frame)
        self.lvl2_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl2_slots_label.pack(side="top")
        self.lvl2_subtract_button = ttk.Button(self.lvl2_frame)
        self.lvl2_subtract_button.configure(text='-')
        self.lvl2_subtract_button.pack(side="top")
        self.lvl2_subtract_button.configure(command=lambda: self.slot_subtract_action(1))
        self.lvl2_frame.grid(column=1, row=0)

        # Level 3 Spell Slots
        self.lvl3_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl3_frame.configure(height=95, width=70)
        self.lvl3_header_label = ttk.Label(self.lvl3_frame)
        self.lvl3_header_label.configure(text='Level 3')
        self.lvl3_header_label.pack(side="top")
        self.lvl3_add_button = ttk.Button(self.lvl3_frame)
        self.lvl3_add_button.configure(text='+')
        self.lvl3_add_button.pack(side="top")
        self.lvl3_add_button.configure(command=lambda: self.slot_add_action(2))
        self.lvl3_slots_label = ttk.Label(self.lvl3_frame)
        self.lvl3_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl3_slots_label.pack(side="top")
        self.lvl3_subtract_button = ttk.Button(self.lvl3_frame)
        self.lvl3_subtract_button.configure(text='-')
        self.lvl3_subtract_button.pack(side="top")
        self.lvl3_subtract_button.configure(command=lambda: self.slot_subtract_action(2))
        self.lvl3_frame.grid(column=2, row=0)

        # Level 4 Spell Slots
        self.lvl4_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl4_frame.configure(height=95, width=70)
        self.lvl4_header_label = ttk.Label(self.lvl4_frame)
        self.lvl4_header_label.configure(text='Level 4')
        self.lvl4_header_label.pack(side="top")
        self.lvl4_add_button = ttk.Button(self.lvl4_frame)
        self.lvl4_add_button.configure(text='+')
        self.lvl4_add_button.pack(side="top")
        self.lvl4_add_button.configure(command=lambda: self.slot_add_action(3))
        self.lvl4_slots_label = ttk.Label(self.lvl4_frame)
        self.lvl4_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl4_slots_label.pack(side="top")
        self.lvl4_subtract_button = ttk.Button(self.lvl4_frame)
        self.lvl4_subtract_button.configure(text='-')
        self.lvl4_subtract_button.pack(side="top")
        self.lvl4_subtract_button.configure(command=lambda: self.slot_subtract_action(3))
        self.lvl4_frame.grid(column=3, row=0)

        # Level 5 Spell Slots
        self.lvl5_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl5_frame.configure(height=95, width=70)
        self.lvl5_header_label = ttk.Label(self.lvl5_frame)
        self.lvl5_header_label.configure(text='Level 5')
        self.lvl5_header_label.pack(side="top")
        self.lvl5_add_button = ttk.Button(self.lvl5_frame)
        self.lvl5_add_button.configure(text='+')
        self.lvl5_add_button.pack(side="top")
        self.lvl5_add_button.configure(command=lambda: self.slot_add_action(4))
        self.lvl5_slots_label = ttk.Label(self.lvl5_frame)
        self.lvl5_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl5_slots_label.pack(side="top")
        self.lvl5_subtract_button = ttk.Button(self.lvl5_frame)
        self.lvl5_subtract_button.configure(text='-')
        self.lvl5_subtract_button.pack(side="top")
        self.lvl5_subtract_button.configure(command=lambda: self.slot_subtract_action(4))
        self.lvl5_frame.grid(column=4, row=0)

        # Level 6 Spell Slots
        self.lvl6_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl6_frame.configure(height=95, width=70)
        self.lvl6_header_label = ttk.Label(self.lvl6_frame)
        self.lvl6_header_label.configure(text='Level 6')
        self.lvl6_header_label.pack(side="top")
        self.lvl6_add_button = ttk.Button(self.lvl6_frame)
        self.lvl6_add_button.configure(text='+')
        self.lvl6_add_button.pack(side="top")
        self.lvl6_add_button.configure(command=lambda: self.slot_add_action(5))
        self.lvl6_slots_label = ttk.Label(self.lvl6_frame)
        self.lvl6_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl6_slots_label.pack(side="top")
        self.lvl6_subtract_button = ttk.Button(self.lvl6_frame)
        self.lvl6_subtract_button.configure(text='-')
        self.lvl6_subtract_button.pack(side="top")
        self.lvl6_subtract_button.configure(command=lambda: self.slot_subtract_action(5))
        self.lvl6_frame.grid(column=5, row=0)

        # Level 7 Spell Slots
        self.lvl7_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl7_frame.configure(height=95, width=70)
        self.lvl7_header_label = ttk.Label(self.lvl7_frame)
        self.lvl7_header_label.configure(text='Level 7')
        self.lvl7_header_label.pack(side="top")
        self.lvl7_add_button = ttk.Button(self.lvl7_frame)
        self.lvl7_add_button.configure(text='+')
        self.lvl7_add_button.pack(side="top")
        self.lvl7_add_button.configure(command=lambda: self.slot_add_action(6))
        self.lvl7_slots_label = ttk.Label(self.lvl7_frame)
        self.lvl7_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl7_slots_label.pack(side="top")
        self.lvl7_subtract_button = ttk.Button(self.lvl7_frame)
        self.lvl7_subtract_button.configure(text='-')
        self.lvl7_subtract_button.pack(side="top")
        self.lvl7_subtract_button.configure(command=lambda: self.slot_subtract_action(6))
        self.lvl7_frame.grid(column=6, row=0)

        # Level 8 Spell Slots
        self.lvl8_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl8_frame.configure(height=95, width=70)
        self.lvl8_header_label = ttk.Label(self.lvl8_frame)
        self.lvl8_header_label.configure(text='Level 8')
        self.lvl8_header_label.pack(side="top")
        self.lvl8_add_button = ttk.Button(self.lvl8_frame)
        self.lvl8_add_button.configure(text='+')
        self.lvl8_add_button.pack(side="top")
        self.lvl8_add_button.configure(command=lambda: self.slot_add_action(7))
        self.lvl8_slots_label = ttk.Label(self.lvl8_frame)
        self.lvl8_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl8_slots_label.pack(side="top")
        self.lvl8_subtract_button = ttk.Button(self.lvl8_frame)
        self.lvl8_subtract_button.configure(text='-')
        self.lvl8_subtract_button.pack(side="top")
        self.lvl8_subtract_button.configure(command=lambda: self.slot_subtract_action(7))
        self.lvl8_frame.grid(column=7, row=0)

        # Level 9 Spell Slots
        self.lvl9_frame = ttk.Frame(self.spell_slot_fram)
        self.lvl9_frame.configure(height=95, width=70)
        self.lvl9_header_label = ttk.Label(self.lvl9_frame)
        self.lvl9_header_label.configure(text='Level 9')
        self.lvl9_header_label.pack(side="top")
        self.lvl9_add_button = ttk.Button(self.lvl9_frame)
        self.lvl9_add_button.configure(text='+')
        self.lvl9_add_button.pack(side="top")
        self.lvl9_add_button.configure(command=lambda: self.slot_add_action(8))
        self.lvl9_slots_label = ttk.Label(self.lvl9_frame)
        self.lvl9_slots_label.configure(
            font="{Sans} 14 {}",
            text='99/99')
        self.lvl9_slots_label.pack(side="top")
        self.lvl9_subtract_button = ttk.Button(self.lvl9_frame)
        self.lvl9_subtract_button.configure(text='-')
        self.lvl9_subtract_button.pack(side="top")
        self.lvl9_subtract_button.configure(command=lambda: self.slot_subtract_action(8))
        self.lvl9_frame.grid(column=8, row=0)
        self.spell_slot_fram.place(
            anchor="nw", height=100, width=690, x=0, y=0)
        self.spell_slot_max_button = ttk.Button(self.spells_frame)
        self.spell_slot_max_button.configure(text='Update Max Spell Slots')
        self.spell_slot_max_button.place(anchor="nw", x=0, y=95)
        self.spell_slot_max_button.configure(
            command=self.spell_slot_max_action)
        self.spells_update_button = ttk.Button(self.spells_frame)
        self.spells_update_button.configure(text='Update Spells List')
        self.spells_update_button.place(anchor="ne", x=680, y=105)
        self.spells_update_button.configure(command=self.spells_update_action)
        # Spells List Frame
        self.labelframe39 = ttk.Labelframe(self.spells_frame)
        self.labelframe39.configure(height=200, text='Spells List', width=200)

        # Spells Scroll Frame, updated dynamically with the ui_reload function
        scrolledframe3 = ScrolledFrame(self.labelframe39, scrolltype="both")
        scrolledframe3.innerframe.configure(width=690)
        scrolledframe3.configure(usemousewheel=False)
        self.spells_scroll_display_frame = ttk.Frame(scrolledframe3.innerframe)
        self.spells_scroll_display_frame.configure(height=200, width=200)

        self.spells_scroll_display_frame.pack(expand=True, fill="both", side="top")
        scrolledframe3.place(anchor="nw", height=335, width=675, x=0, y=0)
        self.labelframe39.place(anchor="nw", height=360, width=680, x=1, y=130)
        self.spells_frame.place(anchor="nw", height=490, width=690, x=5, y=5)
        frame4.pack(side="top")
        self.acs_tabs_notebook.add(frame4, text='Spells')

        # Other Info Tab
        frame5 = ttk.Frame(self.acs_tabs_notebook)
        frame5.configure(height=200, width=200)
        frame144 = ttk.Frame(frame5)
        frame144.configure(height=110, width=700)
        self.frame147 = ttk.Frame(frame144)
        self.frame147.configure(height=95, width=70)
        self.pp_header_label = ttk.Label(self.frame147)
        self.pp_header_label.configure(text='Platinum')
        self.pp_header_label.pack(side="top")
        self.pp_add_button = ttk.Button(self.frame147)
        self.pp_add_button.configure(text='+')
        self.pp_add_button.pack(side="top")
        self.pp_add_button.configure(command=lambda: self.coin_add_action('p'))
        self.pp_val_label = ttk.Label(self.frame147)
        self.pp_val_label.configure(font="{Sans} 14 {}", text='999')
        self.pp_val_label.pack(side="top")
        self.pp_subtract_button = ttk.Button(self.frame147)
        self.pp_subtract_button.configure(text='-')
        self.pp_subtract_button.pack(side="top")
        self.pp_subtract_button.configure(command=lambda: self.coin_subtract_action('p'))
        self.frame147.grid(column=0, row=0)
        self.frame148 = ttk.Frame(frame144)
        self.frame148.configure(height=95, width=70)
        self.gp_header_label = ttk.Label(self.frame148)
        self.gp_header_label.configure(text='Gold')
        self.gp_header_label.pack(side="top")
        self.gp_add_button = ttk.Button(self.frame148)
        self.gp_add_button.configure(text='+')
        self.gp_add_button.pack(side="top")
        self.gp_add_button.configure(command=lambda: self.coin_add_action('g'))
        self.gp_val_label = ttk.Label(self.frame148)
        self.gp_val_label.configure(font="{Sans} 14 {}", text='999')
        self.gp_val_label.pack(side="top")
        self.gp_subtract_button = ttk.Button(self.frame148)
        self.gp_subtract_button.configure(text='-')
        self.gp_subtract_button.pack(side="top")
        self.gp_subtract_button.configure(command=lambda: self.coin_subtract_action('g'))
        self.frame148.grid(column=1, row=0)
        self.frame149 = ttk.Frame(frame144)
        self.frame149.configure(height=95, width=70)
        self.sp_header_label = ttk.Label(self.frame149)
        self.sp_header_label.configure(text='Silver')
        self.sp_header_label.pack(side="top")
        self.sp_add_button = ttk.Button(self.frame149)
        self.sp_add_button.configure(text='+')
        self.sp_add_button.pack(side="top")
        self.sp_add_button.configure(command=lambda: self.coin_add_action('s'))
        self.sp_val_label = ttk.Label(self.frame149)
        self.sp_val_label.configure(font="{Sans} 14 {}", text='999')
        self.sp_val_label.pack(side="top")
        self.sp_subtract_button = ttk.Button(self.frame149)
        self.sp_subtract_button.configure(text='-')
        self.sp_subtract_button.pack(side="top")
        self.sp_subtract_button.configure(command=lambda: self.coin_subtract_action('s'))
        self.frame149.grid(column=2, row=0)
        self.frame150 = ttk.Frame(frame144)
        self.frame150.configure(height=95, width=70)
        self.cp_header_label = ttk.Label(self.frame150)
        self.cp_header_label.configure(text='Copper')
        self.cp_header_label.pack(side="top")
        self.cp_add_button = ttk.Button(self.frame150)
        self.cp_add_button.configure(text='+')
        self.cp_add_button.pack(side="top")
        self.cp_add_button.configure(command=lambda: self.coin_add_action('c'))
        self.cp_val_label = ttk.Label(self.frame150)
        self.cp_val_label.configure(font="{Sans} 14 {}", text='999')
        self.cp_val_label.pack(side="top")
        self.cp_subtract_button = ttk.Button(self.frame150)
        self.cp_subtract_button.configure(text='-')
        self.cp_subtract_button.pack(side="top")
        self.cp_subtract_button.configure(command=lambda: self.coin_subtract_action('c'))
        self.frame150.grid(column=3, row=0)
        self.frame151 = ttk.Frame(frame144)
        self.frame151.configure(height=95, width=70)
        self.ep_header_label = ttk.Label(self.frame151)
        self.ep_header_label.configure(text='Electrum')
        self.ep_header_label.pack(side="top")
        self.ep_add_button = ttk.Button(self.frame151)
        self.ep_add_button.configure(text='+')
        self.ep_add_button.pack(side="top")
        self.ep_add_button.configure(command=lambda: self.coin_add_action('e'))
        self.ep_val_label = ttk.Label(self.frame151)
        self.ep_val_label.configure(font="{Sans} 14 {}", text='999')
        self.ep_val_label.pack(side="top")
        self.ep_subtract_button = ttk.Button(self.frame151)
        self.ep_subtract_button.configure(text='-')
        self.ep_subtract_button.pack(side="top")
        self.ep_subtract_button.configure(command=lambda: self.coin_subtract_action('e'))
        self.frame151.grid(column=4, row=0)
        frame154 = ttk.Frame(frame144)
        frame154.configure(height=0, width=20)
        frame154.grid(column=6, row=0)
        frame156 = ttk.Frame(frame144)
        frame156.configure(height=200, width=200)
        self.coin_update_button = ttk.Button(frame156)
        self.coin_update_button.configure(text='Update')
        self.coin_update_button.pack(side="top")
        self.coin_update_button.configure(command=self.coin_update_action)
        frame156.grid(column=7, row=0)
        frame157 = ttk.Frame(frame144)
        frame157.configure(height=1, width=20)
        frame157.grid(column=8, row=0)
        level_frame = ttk.Frame(frame144)
        level_frame.configure(height=100, width=100)
        self.level_header_label = ttk.Label(level_frame)
        self.level_header_label.configure(text='Level')
        self.level_header_label.pack(side="top")
        self.level_val_label = ttk.Label(level_frame)
        self.level_val_label.configure(font="{Sans} 14 {}", text='99')
        self.level_val_label.pack(side="top")
        self.level_update_button = ttk.Button(level_frame)
        self.level_update_button.configure(text='Update')
        self.level_update_button.pack(side="top")
        self.level_update_button.configure(command=self.level_update_action)
        level_frame.grid(column=9, row=0)
        frame144.pack(side="top")
        frame146 = ttk.Frame(frame5)
        frame146.configure(height=500, width=700)
        self.other_info_header = ttk.Label(frame146)
        self.other_info_header.configure(text='Other Information:')
        self.other_info_header.place(anchor="nw", x=0, y=0)
        frame152 = ttk.Frame(frame146)
        frame152.configure(height=380, width=200)
        scrollbar2 = ttk.Scrollbar(frame152)
        scrollbar2.configure(orient="vertical")
        scrollbar2.place(anchor="ne", height=380, x=690, y=0)
        frame153 = ttk.Frame(frame152)
        frame153.configure(height=380, width=495)
        self.other_info_box = tk.Text(frame153)
        self.other_info_box.configure(font="{sans} 10 {}", height=10, width=50)
        self.other_info_box.pack(expand=True, fill="both", side="top")
        self.other_info_box.delete("1.0", tk.END)
        # self.other_info_box.insert(tk.END, 'Here\'s some text')
        frame153.place(anchor="nw", height=380, width=670, x=0, y=0)
        frame152.place(anchor="nw", height=380, width=690, x=5, y=22)
        frame146.pack(expand=True, fill="both", side="top")
        frame5.pack(side="top")
        self.acs_tabs_notebook.add(frame5, text='Other Information')
        self.acs_tabs_notebook.pack(side="top")

        # Main widget
        self.mainwindow = self.UI
        self.reload_ui()
    def create_spell_item_entry(self, id, name, level, save, cast_time, s_range, damage, duration, description, is_ritual, is_concentration):
        if(is_ritual):
            cast_time = '(R) ' + cast_time
        
        if(is_concentration):
            duration = '(C) ' + duration

        spell_frame = ttk.Frame(self.spells_scroll_display_frame)
        spell_frame.configure(
            height=80, relief="groove", width=650)
        spell_level_label = ttk.Label(spell_frame)
        spell_level_label.configure(
            relief="flat", text=level)
        spell_level_label.place(anchor="nw", x=5, y=5)
        spell_name_label = ttk.Label(spell_frame)
        spell_name_label.configure(
            text=name)
        spell_name_label.place(anchor="nw", x=30, y=5)
        spell_description_label = ttk.Label(
            spell_frame)
        spell_description_label.configure(
            text=description,
            width=95,
            wraplength=520)
        spell_description_label.place(anchor="nw", x=5, y=25)
        spell_sav_label = ttk.Label(spell_frame)
        spell_sav_label.configure(
            text=save)
        spell_sav_label.place(anchor="ne", x=300, y=5)
        spell_time_label = ttk.Label(spell_frame)
        spell_time_label.configure(
            text=cast_time)
        spell_time_label.place(anchor="nw", x=330, y=5)
        spell_range_label = ttk.Label(spell_frame)
        spell_range_label.configure(
            text=s_range)
        spell_range_label.place(anchor="nw", x=405, y=5)
        spell_duration_label = ttk.Label(spell_frame)
        spell_duration_label.configure(
            text=duration)
        spell_duration_label.place(anchor="ne", x=560, y=5)
        spell_hit_button = ttk.Button(spell_frame)
        spell_hit_button.configure(text='HIT', command=lambda: self.spell_hit_action(id))
        spell_hit_button.place(anchor="ne", height=24, x=648, y=1)
        spell_dmg_button = ttk.Button(spell_frame)
        spell_dmg_button.configure(text='RLL', command=lambda: self.spell_dmg_action(id))
        spell_dmg_button.place(anchor="se", height=24, x=648, y=48)

        return spell_frame
    def create_weapon_item_entry(self, id, name, attributes, ability, w_range, hit, dmg, dmgtype):
        weapon_panel = ttk.Frame(self.weapons_scroll_display_frame)
        weapon_panel.configure(
            borderwidth=1, height=50, relief="groove", width=660)
        weapon_name_label = ttk.Label(weapon_panel)
        weapon_name_label.configure(
            text=name,
            width=55)
        weapon_name_label.place(anchor="nw", x=5, y=5)
        weapon_attributes_label = ttk.Label(
            weapon_panel)
        weapon_attributes_label.configure(
            compound="top",
            text=attributes,
            width=85)
        weapon_attributes_label.place(anchor="sw", x=5, y=45)
        weapon_range_label = ttk.Label(weapon_panel)
        weapon_range_label.configure(
            text=w_range)
        weapon_range_label.place(anchor="ne", x=350, y=5)
        weapon_hit_label = ttk.Label(weapon_panel)
        weapon_hit_label.configure(
            text=hit)
        weapon_hit_label.place(anchor="ne", x=575, y=5)
        weapon_dmg_label = ttk.Label(weapon_panel)
        weapon_dmg_label.configure(
            text=dmg)
        weapon_dmg_label.place(anchor="se", x=575, y=45)
        weapon_dmgtype_label = ttk.Label(weapon_panel)
        weapon_dmgtype_label.configure(
            text=dmgtype)
        weapon_dmgtype_label.place(anchor="ne", x=520, y=5)
        weapon_hit_button = ttk.Button(weapon_panel)
        weapon_hit_button.configure(text='HIT')
        weapon_hit_button.place(anchor="ne", height=24, x=655, y=1)
        weapon_hit_button.configure(command=lambda: self.weapon_hit_action(id))
        weapon_dmg_button = ttk.Button(weapon_panel)
        weapon_dmg_button.configure(text='DMG')
        weapon_dmg_button.place(
            anchor="se", height=24, x=655, y=49)
        weapon_dmg_button.configure(command=lambda: self.weapon_dmg_action(id))
        ability_label = ttk.Label(weapon_panel)
        ability_label.configure(text=ability)
        ability_label.place(anchor="nw", x=375, y=5)

        return weapon_panel
    def create_tracker_item_entry(self, tracker_id, tracker_name, tracker_value):
        tracker_frame = ttk.Frame(
            self.trackers_scroll_frame.innerframe)
        tracker_frame.configure(height=30, width=230)
        tracker_header_label = ttk.Label(
            tracker_frame)
        tracker_name_val = tk.StringVar(value=tracker_name)
        tracker_header_label.configure(
            font="{Sans} 8 {}",
            text=tracker_name)
        tracker_header_label.place(anchor="w", x=1, y=15)
        tracker_val_label = ttk.Label(tracker_frame)
        tracker_val = tk.StringVar(value=tracker_value)
        tracker_val_label.configure(
            font="{sans} 12 {}", text=tracker_value)
        tracker_val_label.place(anchor="w", x=130, y=15)
        tracker_subtract_button = ttk.Button(
            tracker_frame)
        tracker_subtract_button.configure(text='-', width=1, command=lambda: self.tracker_minus_action(tracker_id))
        tracker_subtract_button.place(anchor="e", x=186, y=15)
        tracker_set_button = ttk.Button(
            tracker_frame)
        tracker_set_button.configure(text='Set', width=3, command=lambda: self.tracker_set_action(tracker_id))
        tracker_set_button.place(
            anchor="e", width=27, x=213, y=15)
        tracker_add_button = ttk.Button(
            tracker_frame)
        tracker_add_button.configure(text='+', width=1, command=lambda: self.tracker_add_action(tracker_id))
        tracker_add_button.place(
            anchor="e", width=17, x=230, y=15)
        
        return tracker_frame
    def run(self):
        self.mainwindow.mainloop()
    def set_fp_var(self, fp):
        self.fp = fp
        self.reload_ui()
    def crhp_update_action(self):
        new_hp = self.create_update_value_box("Change the current HP value.\nProceed with a '+' to heal\nProceed with a '-' to damage", self.character["hp"])

        if new_hp is not None:
            # If the value starts with a '+', then it's a heal
            if(new_hp[0] == '+'):
                new_hp = new_hp[1:]
                new_hp = int(new_hp)
                new_hp += self.character["hp"]
            
            # If the value starts with a '-', then it's a damage
            elif(new_hp[0] == '-'):
                new_hp = new_hp[1:]
                new_hp = int(new_hp)
                new_hp = self.character["hp"] - new_hp

            # Otherwise, it's a direct value, so just set it

            # Update the json
            CharacterSheet.update_json(self.fp, {
                "hp": new_hp
                })
            
            # Reload the UI
            self.reload_ui()
    def mxhp_update_action(self):
        new_max_hp = self.create_update_value_box("Change the max HP value", self.character["hpMax"])
        if new_max_hp is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "hpMax": new_max_hp
                })
            
            # Reload the UI
            self.reload_ui()
    def ac_update_action(self):
        new_ac = self.create_update_value_box("Change the AC value", self.character["ac"])
        if new_ac is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "ac": new_ac
                })
            
            # Reload the UI
            self.reload_ui()
    def speed_update_action(self):
        new_speed = self.create_update_value_box("Change the speed value", self.character["speed"])
        if new_speed is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "speed": new_speed
            })
            
            # Reload the UI
            self.reload_ui()
    def hit_dice_update_action(self):
        new_hit_dice = self.create_update_value_box("Change the hit dice value\nWhen rolled, your con mod is added to the roll automatically", self.character["hitDieDR"])
        if new_hit_dice is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "hitDieDR": new_hit_dice
            })
            
            # Reload the UI
            self.reload_ui()
    def prof_update_action(self):
        new_prof = self.create_update_value_box("Change the proficiency value", self.character["prof"])
        if new_prof is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "prof": new_prof
            })
            
            # Reload the UI
            self.reload_ui()
    def init_update_action(self):
        new_init_bns = self.create_update_value_box("Change the bonus initiative value.", self.character["bonus_init"])
        if new_init_bns is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "bonus_init": int(new_init_bns)
            })
            
            # Reload the UI
            self.reload_ui()
    def short_rest_action(self):
        can_heal_flag = False
        have_hit_dice_tracker = False

        # Reset trackers that reset on short rest but also parse the max value
        trackers = self.character["trackers"]
        for t in trackers:
            if(t["name"] == "Hit Dice"):
                have_hit_dice_tracker = True
                if(t["value"] > 0):
                    can_heal_flag = True

            refresh_val = t["refresh"]
            # If the first two characters aren't 'sr', then it doesn't reset on short rest
            if(refresh_val[0:2] == "SR"):
                # If there are no more characters, then it's a simple reset
                if(len(refresh_val) == 2):
                    t["value"] = t["max_value"]
                else:
                    # Otherwise it's resetting a specific value
                    refresh_amount = refresh_val[2:]

                    # If the value is a dice roll, then roll it
                    if("d" in refresh_amount):
                        roll = Helpers.parse_dice_string(refresh_amount)
                        refresh_amount = Helpers.roll_single_dice(roll[1], roll[2])
                    else:
                        if(refresh_amount[0] == '+'):
                            refresh_amount = refresh_amount[1:]
                        refresh_amount = int(refresh_amount)

                    # Add the amount to the current value, to a max of the max value
                    t["value"] += refresh_amount
                    if(t["value"] > t["max_value"]):
                        t["value"] = t["max_value"]

        msg = ""        
        hp_cur = self.character["hp"]

        # Determine if the player can heal
        if(can_heal_flag):
            # Ensure the player has hit dice to roll
            for t in trackers:
                if(t["name"] == "Hit Dice"):
                    if(t["value"] < 1):
                        can_heal_flag = False
                    break
        
        if(can_heal_flag):
            # A short rest rolls the hit die and adds the constitution modifier
            hit_die = self.character["hitDieDR"]
            con_mod = Helpers.calculate_modifier(self.character["con"])

            # Convert the hit die into a list roll
            roll = Helpers.parse_dice_string(hit_die)
            if(con_mod[0] == '+'):
                con_mod = con_mod[1:]
            try:
                con_mod = int(con_mod)
            except ValueError:
                raise ValueError
            
            # Do the roll
            roll[2] = con_mod
            hp_gain = Helpers.roll_single_dice(roll[1], roll[2])
            
            # Add this to the current hit points, to a max of maximum
            hp_cur = self.character["hp"]
            hp_max = self.character["hpMax"]
            hp_cur += hp_gain
            if(hp_cur > hp_max):
                hp_cur = hp_max
            
            hp_gain_actual = hp_cur - self.character["hp"]
            if(hp_gain_actual < 0):
                hp_gain_actual = 0

            if(hp_gain_actual == 0):
                msg = "You were already at full health, so you didn't gain any hit points"
            else:
                msg = "Rolling your hit die gave you " + str(hp_gain) + " hit points"
                # Reduce the hit dice tracker by 1
                for t in trackers:
                    if(t["name"] == "Hit Dice"):
                        t["value"] -= 1
                        break

        # Determine if the player can regain spell slots
        spell_slots_left = self.character["spellSlotsLeft"]
        if(self.character["spellSlotRefresh"] == "SR"):
            # If the player gets their spell slots back on a short rest, then reset them
            spell_slots_max = self.character["spellSlotsMax"]
            spell_slots_left = spell_slots_max

        # Update JSON, show message
        CharacterSheet.update_json(self.fp, {
            "hp": int(hp_cur),
            "trackers": trackers,
            "spellSlotsLeft": spell_slots_left
        })
        
        if(not have_hit_dice_tracker):
            msg = "You don't have a hit dice tracker, so you need to manually roll your hit dice to heal"

        if(msg == ""):
            msg = "You were out of hit dice to roll, so you didn't gain any hit points"
        Popup.Roll_Result(msg)
        
        # Reload UI
        self.reload_ui()
    def long_rest_action(self):
        # Reset health to max, increase hit dice tracker by level/2, reset spell slots to max, refresh trackers that reset on long or short rest
        hp_cur = self.character["hp"]
        hp_max = self.character["hpMax"]
        trackers = self.character["trackers"]
        spell_slots_left = self.character["spellSlotsLeft"]
        spell_slots_max = self.character["spellSlotsMax"]
        level = self.character["lvl"]

        # Reset health
        hp_cur = hp_max

        # Reset spell slots
        if(self.character["spellSlotRefresh"] == "LR" or self.character["spellSlotRefresh"] == "SR"):
            # If the player gets their spell slots back on a long or short rest, then reset them
            spell_slots_max = self.character["spellSlotsMax"]
            spell_slots_left = spell_slots_max

        # Reset trackers 
        for t in trackers:
            # Hit dice specific mechanics
            if(t["name"] == "Hit Dice"):
                # Half the level rounded down hit dice come back on a long rest
                t["value"] += int(level/2)
                if(t["value"] > t["max_value"]):
                    t["value"] = t["max_value"]
                continue

            cur_val = t["value"]
            max_val = t["max_value"]
            refresh_val = t["refresh"]

            # Remove the first two characters from the refresh value, 
            # since things that refresh on a short rest also refresh on a long rest
            refresh_val = refresh_val[2:]

            # If there's nothing left, then it's a simple reset
            if(len(refresh_val) == 0):
                cur_val = max_val
            else:
                # Otherwise it's resetting a specific value
                # If the value is a dice roll, then roll it
                if("d" in refresh_val):
                    roll = Helpers.parse_dice_string(refresh_val)
                    refresh_val = Helpers.roll_single_dice(roll[1], roll[2])
                else:
                    if(refresh_val[0] == '+'):
                        refresh_val = refresh_val[1:]
                    refresh_val = int(refresh_val)

                # Add the amount to the current value, to a max of the max value
                cur_val += refresh_val
                if(cur_val > max_val):
                    cur_val = max_val

            # Write the new value back to the tracker
            t["value"] = cur_val

        # Update JSON, show message
        CharacterSheet.update_json(self.fp, {
            "hp": hp_cur,
            "trackers": trackers,
            "spellSlotsLeft": spell_slots_left
        })

        self.reload_ui()
    def init_roll_action(self):
        # Get the dex modifier and add any bonuses
        dex_mod = Helpers.calculate_modifier(self.character["dex"])
        if(dex_mod[0] == '+'):
            dex_mod = dex_mod[1:]
        dex_mod = int(dex_mod)
        init_bns = self.character["bonus_init"]
        self.roll_dialogue(1, 20, dex_mod + init_bns)
    def strength_update_action(self):
        new_strength = self.create_update_value_box("Change the strength value", self.character["str"])
        if new_strength is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "str": new_strength
            })
            
            # Reload the UI
            self.reload_ui()
    def strength_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["str"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def intelligence_update_action(self):
            new_intelligence = self.create_update_value_box("Change the intelligence value", self.character["int"])
            if new_intelligence is not None:
                # Update the json
                CharacterSheet.update_json(self.fp, {
                    "int": new_intelligence
                })
                
                # Reload the UI
                self.reload_ui()
    def intelligence_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["int"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def dexterity_update_action(self):
        new_dexterity = self.create_update_value_box("Change the dexterity value", self.character["dex"])
        if new_dexterity is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "dex": new_dexterity
            })
            
            # Reload the UI
            self.reload_ui()
    def dexterity_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["dex"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def wisdom_update_action(self):
        new_wisdom = self.create_update_value_box("Change the wisdom value", self.character["wis"])
        if new_wisdom is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "wis": new_wisdom
            })
            
            # Reload the UI
            self.reload_ui()
    def wisdom_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["wis"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def constitution_update_action(self):
        new_constitution = self.create_update_value_box("Change the constitution value", self.character["con"])
        if new_constitution is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "con": new_constitution
            })
            
            # Reload the UI
            self.reload_ui()
    def constitution_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["con"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def charisma_update_action(self):
        new_charisma = self.create_update_value_box("Change the charisma value", self.character["cha"])
        if new_charisma is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "cha": new_charisma
            })
            
            # Reload the UI
            self.reload_ui()
    def charisma_save_action(self):
        # Caluculate the save value, then roll it
        save = Helpers.calculate_save(self.character["cha"], self.character["class"])
        self.roll_dialogue(1, 20, save)
    def tracker_minus_action(self, tracker_id):
        # Find the tracker instance from the id
        t = Tracker()
        for tr in self.trackers_list:
            if tr.id == tracker_id:
                t = tr
                break
        
        tracker_value = int(t.value) -1
        self.character["trackers"][tracker_id]["value"] = tracker_value
        CharacterSheet.update_json(self.fp, {
            "trackers": self.character["trackers"]
        })
        self.reload_ui()
    def tracker_set_action(self, tracker_id):
        # Find the tracker instance from the id
        t = Tracker()
        for tr in self.trackers_list:
            if tr.id == tracker_id:
                t = tr
                break
        
        cur_val = int(t.value)
        new_val = int(self.create_update_value_box("Set the value of the tracker", cur_val) or 0)
        trackers = self.character["trackers"]
        trackers[tracker_id]["value"] = new_val
        CharacterSheet.update_json(self.fp, {
            "trackers": self.character["trackers"]
        })
        self.reload_ui()
    def tracker_add_action(self, tracker_id):
        # Find the tracker instance from the id
        t = Tracker()
        for tr in self.trackers_list:
            if tr.id == tracker_id:
                t = tr
                break
        
        tracker_value = int(t.value) +1
        self.character["trackers"][tracker_id]["value"] = tracker_value
        CharacterSheet.update_json(self.fp, {
            "trackers": self.character["trackers"]
        })
        self.reload_ui()
    def abchk_action(self, ability):
        # Look up the ability check value, then roll it
        abchk = Helpers.calculate_abchk(ability, self.character)
        self.roll_dialogue(1, 20, abchk)
    def weapon_hit_action(self, weapon_id):
        # Find the weapon instance from the id
        w = Weapon()
        for wp in self.weapons_list:
            if wp.id == weapon_id:
                w = wp
                break

        # Get the weapon's ability modifier, and if the user has proficiency with the weapon
        ability = self.character[w.ability]
        proficiency = w.is_proficient
        
        mod = Helpers.calculate_modifier(ability)
        if(mod[0] == '+'):
            mod = int(mod[1:])
        else:
            mod = int(mod)
        if proficiency:
            mod += int(self.character["prof"])

        # Roll the hit
        self.roll_dialogue(1, 20, mod)
    def weapon_dmg_action(self, weapon_id):
        # Find the weapon instance from the id
        w = Weapon()
        for wp in self.weapons_list:
            if wp.id == weapon_id:
                w = wp
                break

        # Get the weapon's damage dice and type, then roll it
        dmg = w.damage
        self.roll_dialogue_string(dmg)
    def slot_add_action(self, slot_lvl):
        count = self.character["spellSlotsLeft"][slot_lvl] +1
        spell_slots_left = self.character["spellSlotsLeft"]
        spell_slots_left[slot_lvl] = count
        CharacterSheet.update_json(self.fp, {
            "spellSlotsLeft": spell_slots_left
        })
        self.reload_ui()
    def slot_subtract_action(self, slot_lvl):
        count = self.character["spellSlotsLeft"][slot_lvl] -1
        spell_slots_left = self.character["spellSlotsLeft"]
        spell_slots_left[slot_lvl] = count
        CharacterSheet.update_json(self.fp, {
            "spellSlotsLeft": spell_slots_left
        })
        self.reload_ui()
    def spell_slot_max_action(self):
        spell_slots_max = self.character["spellSlotsMax"]
        spell_slot_refresh = self.character["spellSlotRefresh"]

        # Encode the spell slots as a map of slot levels to values
        spell_slots_map = {
            "Level 1": spell_slots_max[0],
            "Level 2": spell_slots_max[1],
            "Level 3": spell_slots_max[2],
            "Level 4": spell_slots_max[3],
            "Level 5": spell_slots_max[4],
            "Level 6": spell_slots_max[5],
            "Level 7": spell_slots_max[6],
            "Level 8": spell_slots_max[7],
            "Level 9": spell_slots_max[8],
            "Spell Slot Refresh": spell_slot_refresh
        }
        
        # Create a list of editItem_options for each property
        prop_list = []
        for key in spell_slots_map:
            this_itm = EditItem_Option(key, spell_slots_map[key], "+ve_int")

            # Add custom rules
            if(key == "Spell Slot Refresh"):
                this_itm.input_type = "av"
                this_itm.accepted_values = ["", "SR", "LR"]
            
            prop_list.append(this_itm)

        # Create a dialogue box to edit the item
        Popup.EditItemPopup("Edit Spell Slots", prop_list, self.ssm_update_callback)  
    def spell_hit_action(self, spell_id):
        # Get the character's spell attack modifier
        ability = Helpers.get_spellcasting_ability(self.character["class"])
        ability_mod = Helpers.calculate_modifier(self.character[ability])
        prof = self.character["prof"]
        if(ability_mod[0] == '+'):
            ability_mod = int(ability_mod[1:])
        else:   
            ability_mod = int(ability_mod)
        
        # Roll the hit
        mod = ability_mod + prof
        self.roll_dialogue(1, 20, mod)
    def spell_dmg_action(self, spell_id):
        # Find the tracker instance from the id
        s = Spell()
        for sp in self.spells_list:
            if sp.id == spell_id:
                s = sp
                break
        
        # Get the spell's damage dice and type, then roll it
        dmg = s.damage
        if(dmg != ""):
            self.roll_dialogue_string(dmg)
    def coin_add_action(self, coin_name):
        currency_index = ['p', 'g', 's', 'c', 'e'].index(coin_name)
        currency_lst = self.character["currency"]
        currency_lst[currency_index] += 1
        CharacterSheet.update_json(self.fp, {
            "currency": currency_lst
        })
        self.reload_ui()
    def coin_subtract_action(self, coin_name):
        currency_index = ['p', 'g', 's', 'c', 'e'].index(coin_name)
        currency_lst = self.character["currency"]
        currency_lst[currency_index] -= 1
        CharacterSheet.update_json(self.fp, {
            "currency": currency_lst
        })
        self.reload_ui()
    def trackers_update_action(self):
        # Get a list of all the trackers
        trackers = self.character["trackers"]
        trackers_list = []
        trackers_list.append("New Tracker")
        for t in trackers:
            trackers_list.append(t["name"])
        
        # Create a dialogue box to select which tracker to update
        Popup.ComboBoxChoice("Select a tracker to update", trackers_list, self.tracker_choice_callback)       
    def abilities_update_action(self):
        # Create a list of editItem_options for each property
        prop_list = []
        for key in self.character["abilities"]:
            acc_vals = ["Normal", "Proficient (+prof)", "Expertise (+2x prof)"]
            curr_val = acc_vals[self.character["abilities"][key]]
            this_itm = EditItem_Option(key, curr_val, "av", acc_vals)
            prop_list.append(this_itm)

        # Create a dialogue box to edit the item
        Popup.EditItemPopup("Edit Abilities", prop_list, self.abilities_update_callback)
    def weapons_update_action(self):
        # Get a list of all the weapons
        weapons = self.character["weapons"]
        weapons_list = []
        weapons_list.append("New Weapon")
        for w in weapons:
            weapons_list.append(w["name"])
        
        # Create a dialogue box to select which tracker to update
        Popup.ComboBoxChoice("Select a weapon to update", weapons_list, self.weapon_choice_callback)
    def spells_update_action(self):
        # Get a list of all the spells
        spells = self.character["spells"]
        spells_list = []
        spells_list.append("New Spell")
        for w in spells:
            spells_list.append(w["name"])
        
        # Create a dialogue box to select which tracker to update
        Popup.ComboBoxChoice("Select a spell to update", spells_list, self.spell_choice_callback)
    def coin_update_action(self):
        current_currency = self.character["currency"]

        # Encode the currency as a map of coin names to values
        currency_map = {
            "platinum": current_currency[0],
            "gold": current_currency[1],
            "silver": current_currency[2],
            "copper": current_currency[3],
            "electrum": current_currency[4]
        }

        # Create a list of editItem_options for each property
        prop_list = []
        for key in currency_map:
            this_itm = EditItem_Option(key, currency_map[key], "+ve_int")
            prop_list.append(this_itm)

        # Create a dialogue box to edit the item
        Popup.EditItemPopup("Edit Currency", prop_list, self.coin_update_callback)
    def level_update_action(self):
        new_level = self.create_update_value_box("Change the level value", self.character["lvl"])
        if new_level is not None:
            # Update the json
            CharacterSheet.update_json(self.fp, {
                "lvl": new_level
            })
            
            # Reload the UI
            self.reload_ui()
    def other_info_update_action(self):
        pass
    
    # Callbacks that actually do the work
    def tracker_choice_callback(self, tracker_name):
        if(tracker_name == "New Tracker"):
            # Create a new tracker and add it to the character sheet object
            tracker_item = {
                "name": "New Tracker",
                "value": 0,
                "max_value": 0,
                "refresh": ""
            }

            # Add this to the list of trackers
            trackers = self.character["trackers"]
            trackers.append(tracker_item)

            # Now we can proceed to edit the tracker as normal

        # Get the tracker object from the character sheet object
        tracker = {}
        for t in self.character["trackers"]:
            if(t["name"] == tracker_name):
                tracker = t
                break
        
        # Remove this tracker from the list of trackers
        self.character["trackers"].remove(tracker)

        # Create a list of editItem_options for each property
        prop_list = []
        for key in tracker:
            this_itm = EditItem_Option(key, tracker[key])
            prop_list.append(this_itm)

        # Add custom rules
        for prop in prop_list:
            # Modify the "value" property to use custom rules
            if(prop.name == "value"):
                prop.input_type = "+ve_int"
            
            # Modify the "max_value" property to use custom rules
            if(prop.name == "max_value"):
                prop.input_type = "+ve_int"

        # Create a dialogue box to edit the item
        Popup.EditItemPopup("Edit Tracker", prop_list, self.tracker_update_callback)
    def weapon_choice_callback(self, weapon_name):
        if(weapon_name == "New Weapon"):
            weapon_item = {
                "name": "New Weapon",
                "attributes": "",
                "ability": "str",
                "damageType": "Slashing",
                "isProficient": "true",
                "range": "Melee",
                "damage": "1d8",
                "hit_bns": 0
            }

            weapons = self.character["weapons"]
            weapons.append(weapon_item)
        
        weapon = {}
        for w in self.character["weapons"]:
            if(w["name"] == weapon_name):
                weapon = w
                break
        
        self.character["weapons"].remove(weapon)

        # Create a list of editItem_options for each property
        prop_list = []
        for key in weapon:
            this_itm = EditItem_Option(key, weapon[key])
            prop_list.append(this_itm)

        # Add custom rules
        for prop in prop_list:
            # Modify the "hit_bns" property to use custom rules
            if(prop.name == "hit_bns"):
                prop.input_type = "+ve_int"

            # Modify the damageType property to use custom rules
            if(prop.name == "damageType"):
                prop.input_type = "av"
                prop.accepted_values = ["", "Magical", "Slashing", "Piercing", "Bludgeoning", "Fire", "Cold", "Lightning", "Thunder", "Poison", "Acid", "Psychic", "Necrotic", "Radiant", "Force"]
            
            # Modify the "isProficient" property to use custom rules
            if(prop.name == "isProficient"):
                prop.input_type = "b"
                
            # Modify the "ability" property to use custom rules
            if(prop.name == "ability"):
                prop.input_type = "av"
                prop.accepted_values = ["str", "dex", "con", "int", "wis", "cha"]

        Popup.EditItemPopup("Edit Weapon", prop_list, self.weapon_update_callback)
    def spell_choice_callback(self, spell_name):
       
        if(spell_name == "New Spell"):
            spell_item = {
                "level": 0,
                "name": "New Spell",
                "save": "",
                "cast_time": "1 action",
                "range": "120 feet",
                "damage": "0",
                "duration": "1 min",
                "description": "",
                "ritual": "false",
                "concentration": "false"
            }

            spells = self.character["spells"]
            spells.append(spell_item)
        
        spell = {}
        for w in self.character["spells"]:
            if(w["name"] == spell_name):
                spell = w
                break
        
        self.character["spells"].remove(spell)

        # Create a list of editItem_options for each property
        prop_list = []

        for key in spell:
            this_itm = EditItem_Option(key, spell[key])
            prop_list.append(this_itm)

        # Add custom rules
        for prop in prop_list:
            # Modify the "level" property to use custom rules
            if(prop.name == "level"):
                prop.input_type = "av"
                prop.accepted_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            # Modify the "ritual" property to use custom rules
            if(prop.name == "ritual"):
                prop.input_type = "b"

            # Modify the "concentration" property to use custom rules
            if(prop.name == "concentration"):
                prop.input_type = "b"

        Popup.EditItemPopup("Edit Spell", prop_list, self.spell_update_callback)
    def tracker_update_callback(self, tracker_item):
        # Ensure that we got something back
        if(tracker_item is None):
            # If we didn't get anything back, then the user deleted the tracker
            # Update the JSON, reload the UI and return
            trackers = self.character["trackers"]
            CharacterSheet.update_json(self.fp, {
                "trackers": trackers
            })
            self.reload_ui()
            return

        # Now we've got the edited tracker, add it back to the list and update the json
        trackers = self.character["trackers"]
        trackers.append(tracker_item)

        # Sort the trackers by name
        trackers = sorted(trackers, key=lambda k: k['name'])

        # Put the "Hit Dice" tracker at the top, if it exists
        hit_dice_tracker = None
        for t in trackers:
            if(t["name"] == "Hit Dice"):
                hit_dice_tracker = t
                trackers.remove(t)
                break
        
        if(hit_dice_tracker is not None):
            trackers.insert(0, hit_dice_tracker)
        
        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "trackers": trackers
        })
        self.reload_ui()
    def weapon_update_callback(self, weapon_item):
        # Ensure that we got something back
        if(weapon_item is None):
            # If we didn't get anything back, then the user deleted the tracker
            # Update the JSON, reload the UI and return
            weapons = self.character["weapons"]
            CharacterSheet.update_json(self.fp, {
                "weapons": weapons
            })
            self.reload_ui()
            return
        
        # Ensure that the correct types are set
        weapon_item["isProficient"] = bool(weapon_item["isProficient"])
        weapon_item["hit_bns"] = int(weapon_item["hit_bns"])

        # Now we've got the edited weapon, add it back to the list and update the json
        weapons = self.character["weapons"]
        weapons.append(weapon_item)

        # Sort the weapons by name
        weapons = sorted(weapons, key=lambda k: k['name'])

        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "weapons" : weapons
        })
        self.reload_ui()
    def spell_update_callback(self, spell_item):
        # Ensure that we got something back
        if(spell_item is None):
            # If we didn't get anything back, then the user deleted the tracker
            # Update the JSON, reload the UI and return
            spells = self.character["spells"]
            CharacterSheet.update_json(self.fp, {
                "spells": spells
            })
            self.reload_ui()
            return
        
        # Ensure that the correct types are set
        spell_item["level"] = int(spell_item["level"])
        spell_item["ritual"] = bool(spell_item["ritual"])
        spell_item["concentration"] = bool(spell_item["concentration"])

        # Now we've got the edited spell, add it back to the list and update the json
        spells = self.character["spells"]
        spells.append(spell_item)

        # Sort the spells by name
        spells = sorted(spells, key=lambda k: k['name'])

        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "spells" : spells
        })
        self.reload_ui()
    def coin_update_callback(self, coin_map):
        if(coin_map == None):
            # If the new values are None, then the user tried to delete the abilities
            # In this case, we don't want to do anything, except tell the user they can't delete the abilities
            Popup.Message("You can't delete this section, as it's required for the character sheet")
            self.reload_ui()
            return
        
        # Translate the coin array back into the currency list
        # p, g, s, c, e
        currency = [0, 0, 0, 0, 0]
        currency[0] = coin_map["platinum"]
        currency[1] = coin_map["gold"]
        currency[2] = coin_map["silver"]
        currency[3] = coin_map["copper"]
        currency[4] = coin_map["electrum"]

        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "currency": currency
        })
        self.reload_ui()
    def ssm_update_callback(self, new_values):
        if(new_values == None):
            # If the new values are None, then the user tried to delete the abilities
            # In this case, we don't want to do anything, except tell the user they can't delete the abilities
            Popup.Message("You can't delete this section, as it's required for the character sheet")
            self.reload_ui()
            return
        
        # Translate the spell slots array back into the spell slots list
        spell_slots = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        spell_slots[0] = new_values["Level 1"]
        spell_slots[1] = new_values["Level 2"]
        spell_slots[2] = new_values["Level 3"]
        spell_slots[3] = new_values["Level 4"]
        spell_slots[4] = new_values["Level 5"]
        spell_slots[5] = new_values["Level 6"]
        spell_slots[6] = new_values["Level 7"]
        spell_slots[7] = new_values["Level 8"]
        spell_slots[8] = new_values["Level 9"]

        spell_slot_refresh = new_values["Spell Slot Refresh"]

        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "spellSlotsMax": spell_slots,
            "spellSlotRefresh": spell_slot_refresh
        })
        self.reload_ui()        
    def abilities_update_callback(self, new_values):
        if(new_values == None):
            # If the new values are None, then the user tried to delete the abilities
            # In this case, we don't want to do anything, except tell the user they can't delete the abilities
            Popup.Message("You can't delete this section, as it's required for the character sheet")
            self.reload_ui()
            return
        
        for key in new_values:
            if(new_values[key] == "Normal"):
                new_values[key] = 0
            elif(new_values[key] == "Proficient (+prof)"):
                new_values[key] = 1
            elif(new_values[key] == "Expertise (+2x prof)"):
                new_values[key] = 2

        # Update the json, reload the ui
        CharacterSheet.update_json(self.fp, {
            "abilities": new_values
        })
        self.reload_ui()

# ---------------------------------------------------------------------
# End of UI specific code
# ---------------------------------------------------------------------

    def reload_ui(self):
        # Get the character sheet object from the character sheet class
        self.character = CharacterSheet.read_json(self.fp)
        
        # Get the health and max heatlh values of the character, then get the percentage of health remaining rounded to the lowest 10%, as an integer between 0 and 10
        hp = str(self.character["hp"])
        hpMax = str(self.character["hpMax"])
        health_percentage = int(math.floor((int(hp) / int(hpMax)) * 10))

        initiative = Helpers.calculate_modifier(self.character["dex"])
        if(initiative[0] == '+'):
            initiative = int(initiative[1:]) + self.character["bonus_init"]
        else:
            initiative = int(initiative) + self.character["bonus_init"]
        
        # Change the color of the health value based on the percentage of health remaining
        """
        0 < 20% = red
        20% < 40% = orange
        40% < 50% = yellow
        default = black
        """
        # I'd do this with a switch statement, but python doesn't have fallthrough, so it'd be cringe
        if health_percentage < 2:
            self.hp_val_label.configure(foreground="red")
        elif health_percentage < 4:
            self.hp_val_label.configure(foreground="orange")
        elif health_percentage < 5:
            self.hp_val_label.configure(foreground="yellow")
        else:
            self.hp_val_label.configure(foreground="black")
        
        # tmp
        self.hp_val_label.configure(text=hp + "/" + hpMax)
        
        # Take all the aspects of the UI and populate them with the data from the character sheet object
        self.hp_val_label.configure(text=hp + "/" + hpMax)
        self.ac_val_label.configure(text=str(self.character["ac"]))
        self.speed_val_label.configure(text=str(self.character["speed"]))
        self.hit_die_val_label.configure(text=str(self.character["hitDieDR"]))
        self.prof_val_label.configure(text=str(self.character["prof"]))
        self.init_val_label.configure(text=str(initiative))
        self.strength_score_label.configure(text=str(self.character["str"]))
        self.strength_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["str"])))
        self.strength_save_label.configure(text=str(Helpers.calculate_save(self.character["str"], self.character["class"])))
        self.intelligence_score_label.configure(text=str(self.character["int"]))
        self.intelligence_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["int"])))
        self.intelligence_save_label.configure(text=str(Helpers.calculate_save(self.character["int"], self.character["class"])))
        self.dexterity_score_label.configure(text=str(self.character["dex"]))
        self.dexterity_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["dex"])))
        self.dexterity_save_label.configure(text=str(Helpers.calculate_save(self.character["dex"], self.character["class"])))
        self.wisdom_score_label.configure(text=str(self.character["wis"]))
        self.wisdom_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["wis"])))
        self.wisdom_save_label.configure(text=str(Helpers.calculate_save(self.character["wis"], self.character["class"])))
        self.constitution_score_label.configure(text=str(self.character["con"]))
        self.constitution_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["con"])))
        self.constitution_save_label.configure(text=str(Helpers.calculate_save(self.character["con"], self.character["class"])))
        self.charisma_score_label.configure(text=str(self.character["cha"]))
        self.charisma_mod_label.configure(text=str(Helpers.calculate_modifier(self.character["cha"])))
        self.charisma_save_label.configure(text=str(Helpers.calculate_save(self.character["cha"], self.character["class"])))
        
        self.strength_abchk_value_label.configure(text=Helpers.calculate_abchk("str", self.character))
        self.athletics_abchk_value_label.configure(text=Helpers.calculate_abchk("athletics", self.character))
        self.dex_abchk_value_label.configure(text=Helpers.calculate_abchk("dex", self.character))
        self.acrobatics_abchk_value_label.configure(text=Helpers.calculate_abchk("acrobatics", self.character))
        self.sleight_of_hand_abchk_value_label.configure(text=Helpers.calculate_abchk("sleightOfHand", self.character))
        self.stealth_abchk_value_label.configure(text=Helpers.calculate_abchk("stealth", self.character))
        self.intelligence_abchk_value_label.configure(text=Helpers.calculate_abchk("int", self.character))
        self.arcana_abchk_value_label.configure(text=Helpers.calculate_abchk("arcana", self.character))
        self.history_abchk_value_label.configure(text=Helpers.calculate_abchk("history", self.character))
        self.investigation_abchk_value_label.configure(text=Helpers.calculate_abchk("investigation", self.character))
        self.nature_abchk_value_label.configure(text=Helpers.calculate_abchk("nature", self.character))
        self.religion_abchk_value_label.configure(text=Helpers.calculate_abchk("religion", self.character))
        self.wisdom_abchk_value_label.configure(text=Helpers.calculate_abchk("wis", self.character))
        self.animal_handling_abchk_value_label.configure(text=Helpers.calculate_abchk("animalHandling", self.character))
        self.insight_abchk_value_label.configure(text=Helpers.calculate_abchk("insight", self.character))
        self.medicine_abchk_value_label.configure(text=Helpers.calculate_abchk("medicine", self.character))
        self.perception_abchk_value_label.configure(text=Helpers.calculate_abchk("perception", self.character))
        self.survival_abchk_value_label.configure(text=Helpers.calculate_abchk("survival", self.character))
        self.charisma_abchk_value_label.configure(text=Helpers.calculate_abchk("cha", self.character))
        self.deception_abchk_value_label.configure(text=Helpers.calculate_abchk("deception", self.character))
        self.intimidation_abchk_value_label.configure(text=Helpers.calculate_abchk("intimidation", self.character))
        self.performance_abchk_value_label.configure(text=Helpers.calculate_abchk("performance", self.character))
        self.persuasion_abchk_value_label.configure(text=Helpers.calculate_abchk("persuasion", self.character))
        
        self.lvl1_slots_label.configure(text=str(self.character["spellSlotsLeft"][0]) + "/" + str(self.character["spellSlotsMax"][0]))
        self.lvl2_slots_label.configure(text=str(self.character["spellSlotsLeft"][1]) + "/" + str(self.character["spellSlotsMax"][1]))
        self.lvl3_slots_label.configure(text=str(self.character["spellSlotsLeft"][2]) + "/" + str(self.character["spellSlotsMax"][2]))
        self.lvl4_slots_label.configure(text=str(self.character["spellSlotsLeft"][3]) + "/" + str(self.character["spellSlotsMax"][3]))
        self.lvl5_slots_label.configure(text=str(self.character["spellSlotsLeft"][4]) + "/" + str(self.character["spellSlotsMax"][4]))
        self.lvl6_slots_label.configure(text=str(self.character["spellSlotsLeft"][5]) + "/" + str(self.character["spellSlotsMax"][5]))
        self.lvl7_slots_label.configure(text=str(self.character["spellSlotsLeft"][6]) + "/" + str(self.character["spellSlotsMax"][6]))
        self.lvl8_slots_label.configure(text=str(self.character["spellSlotsLeft"][7]) + "/" + str(self.character["spellSlotsMax"][7]))
        self.lvl9_slots_label.configure(text=str(self.character["spellSlotsLeft"][8]) + "/" + str(self.character["spellSlotsMax"][8]))

        self.pp_val_label.configure(text=self.character["currency"][0])
        self.gp_val_label.configure(text=self.character["currency"][1])
        self.sp_val_label.configure(text=self.character["currency"][2])
        self.cp_val_label.configure(text=self.character["currency"][3])
        self.ep_val_label.configure(text=self.character["currency"][4])

        self.level_val_label.configure(text=str(self.character["lvl"]))
        
        # Get the text from the other info box, so we don't overwrite it
        self.character["info"] = self.other_info_box.get("1.0", tk.END)
        self.other_info_box.delete("1.0", tk.END)
        self.other_info_box.insert(tk.END, self.character["info"])
        
        # 
        # Trackers
        # 

        # Clear the existing trackers
        for child in self.trackers_scroll_frame.innerframe.winfo_children():
            child.destroy()
        self.trackers_list.clear()

        # Reset the tracker id counter
        Tracker.id_tracker = 0

        # Get the list of trackers from the character dict "trackers"
        tracker_list = self.character["trackers"]
        tracker_id = None
        for t in tracker_list:
            # Create a new tracker object
            new_tracker = Tracker(t["name"], t["value"], t["max_value"], t["refresh"])
            self.trackers_list.append(new_tracker)
            tracker_id = new_tracker.id

            # Create UI
            this_tracker_frame = self.create_tracker_item_entry(new_tracker.id, new_tracker.name, new_tracker.value)

            # Add to UI
            this_tracker_frame.grid(column=0, padx=5, row=tracker_id)
            this_tracker_frame.grid_anchor("sw")

        # 
        # Weapons
        #
        
        # Clear the existing weapons
        for child in self.weapons_scroll_display_frame.winfo_children():
            child.destroy()
        self.weapons_list.clear()

        # Reset the weapon id counter
        Weapon.id_tracker = 0

        # Get the list of weapons from the character dict "weapons"
        weapon_list = self.character["weapons"]
        weapon_id = None
        for w in weapon_list:
            # Create a new weapon object
            new_weapon = Weapon(w["name"], w["attributes"], (w["ability"].lower()), w["damageType"], w["isProficient"], w["range"], w["damage"], w["hit_bns"])
            self.weapons_list.append(new_weapon)
            weapon_id = new_weapon.id

            # Caluculate the hit value by getting the ability modifier, adding prof (if applicable), and adding the hit bonus from the weapon (if applicable
            # Get the relevant ability modifier
            hit_val = Helpers.calculate_modifier(self.character[new_weapon.ability])
            # Convert the hit value to an int
            if(hit_val[0] == "+"):
                hit_val = hit_val[1:]
            try:
                hit_val = int(hit_val)
            except ValueError:
                raise ValueError("Hit value is not an int")
            
            # Add proficiency if applicable
            if new_weapon.is_proficient:
                hit_val += int(self.character["prof"])
            hit_val += new_weapon.hit_bonus

            # Add a + to the hit value if it's positive
            hit = ""
            if hit_val >= 0:
                hit = "+" + str(hit_val)
            else:
                hit = str(hit_val)

            # Create UI
            this_weapon_frame = self.create_weapon_item_entry(new_weapon.id, new_weapon.name, new_weapon.attributes, new_weapon.ability, new_weapon.range, hit, new_weapon.damage, new_weapon.damage_type)

            # # Add to UI
            this_weapon_frame.grid(column=0, padx=5, row=weapon_id)
            this_weapon_frame.grid_anchor("nw")

        #
        # Spells
        #
            
        # Clear the existing spells
        for child in self.spells_scroll_display_frame.winfo_children():
            child.destroy()
        self.spells_list.clear()

        # Reset the spell id counter
        Spell.id_tracker = 0

        # Get the list of spells from the character dict "spells"
        spell_list = self.character["spells"]
        spell_id = None

        # Sort the spells by level, and then by name
        spell_list = sorted(spell_list, key=lambda k: k['level'])
        
        # Create a new spell object for each spell in the list
        for s in spell_list:
            new_spell = Spell(s["level"], s["name"], s["save"], s["cast_time"], s["range"], s["damage"], s["duration"], s["description"], s["ritual"], s["concentration"])
            self.spells_list.append(new_spell)
            spell_id = new_spell.id

            # Create UI
            this_spell_frame = self.create_spell_item_entry(new_spell.id, new_spell.name, new_spell.level, new_spell.save, new_spell.cast_time, new_spell.range, new_spell.damage, new_spell.duration, new_spell.description, new_spell.ritual, new_spell.concentration)

            # Add to UI
            this_spell_frame.grid(column=0, padx=5, row=spell_id)
            this_spell_frame.grid_anchor("nw")

    # Create a box that displays some text, an input for some value, and a button to update that value, then the value is returned
    def create_update_value_box(self, text_to_show, curr_value, parent=None):
        p = Popup.Change_One_Value(text_to_show, curr_value)
        return p

    # Create a box that displays the result of a dice roll. All of this text is already created by the associated helper function, so this function just needs to display it
    def roll_dialogue(self, sides, count, modifier, parent=None):
        message = Helpers.show_dice_roll_message_component(sides, count, modifier)
        Popup.Roll_Result(message)
    
    def roll_dialogue_string(self, dice_string, parent=None):
        message = Helpers.show_dice_roll_message_string(dice_string)
        Popup.Roll_Result(message)

if __name__ == "__main__":
    app = ActiveCharacterSheetUI("test_sheet.json")
    app.reload_ui()
    app.run()

