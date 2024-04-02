#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.ttk as ttk

class EncounterTracker:

    def __init__(self, master=None):
        self.enemies = []
        
        example_enemy = EncounterEnemy(
            name="Enemy 0",
            damage_taken=0,
            lowest_hit=999,
            highest_miss=0,
            combat_log=CombatLog()
        )
        self.enemies.append(example_enemy)

        # build ui
        toplevel_2 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel_2.configure(height=200, width=200)
        frame_5 = ttk.Frame(toplevel_2)
        frame_5.configure(height=310, width=450)
        self.header_label = ttk.Label(frame_5)
        self.header_label.configure(
            font="{Arial} 16 {}",
            text='Encounter Tracker')
        self.header_label.place(anchor="nw", x=10, y=10)
        self.new_tab_button = ttk.Button(frame_5)
        self.new_tab_button.configure(text='New Tab')
        self.new_tab_button.place(anchor="ne", x=440, y=5)
        self.new_tab_button.configure(command=self.new_tab_button_action)
        self.beastiary_button = ttk.Button(frame_5)
        self.beastiary_button.configure(text='Beastiary')
        self.beastiary_button.place(anchor="ne", x=440, y=30)
        self.beastiary_button.configure(command=self.beastiary_button_action)
        frame_9 = ttk.Frame(frame_5)
        frame_9.configure(height=300, width=490)
        self.combat_notebook = ttk.Notebook(frame_9)
        self.combat_notebook.configure(height=200, width=470)
        self.combat_notebook.enable_traversal()

        # Dynamic content would be here, but moved to reload_ui

        self.combat_notebook.pack(expand=True, fill="both", side="top")
        frame_9.place(anchor="nw", height=245, width=435, x=5, y=60)
        frame_5.pack(side="top")

        # Main widget
        self.mainwindow = toplevel_2
        self.reload_ui()

    def reload_ui(self):
        # Get the currently selected tab's index
        try:
            selected_tab = self.combat_notebook.index(self.combat_notebook.select())
        except tk.TclError:
            selected_tab = 0

        self.enemy_vars = {}

        # Remove all tabs from the notebook
        tabs = self.combat_notebook.tabs()
        for tab in tabs:
            self.combat_notebook.forget(tab)

        for enemy in self.enemies:
            # start of dynamic content
            this_mainframe = ttk.Frame(self.combat_notebook)
            this_mainframe.configure(height=200, width=200)
            this_combat_frame = ttk.Frame(this_mainframe)
            this_combat_frame.configure(height=140, width=150)
            this_combat_topframe = ttk.Frame(this_combat_frame)
            this_combat_topframe.configure(height=200, width=200)
            this_combat_log_header = ttk.Label(this_combat_topframe)
            this_combat_log_header.configure(text='Combat Log')
            this_combat_log_header.pack(side="left")
            this_undobutton = ttk.Button(this_combat_topframe)
            this_undobutton.configure(text='Undo', width=5)
            this_undobutton.configure(command=lambda e_id=enemy.id: self.undo_button_action(e_id))
            this_undobutton.pack(padx=20, side="right")
            this_combat_topframe.pack(side="top")
            this_combat_log = tk.Text(this_combat_frame)
            this_combat_log.configure(font="{arial} 8 {}", height=10, width=45)
            
            # Add text to the combat log
            combat_log_text = " H    | D    | T    | R    | A    \n"
            current = None
            if(enemy.combat_log is not None):
                current = enemy.combat_log.head
            while current is not None:
                combat_log_text += current.to_string() + "\n"
                current = current.next
            this_combat_log.insert(tk.END, combat_log_text)
            this_combat_log.configure(state='disabled')

            this_combat_log.pack(expand=True, fill="both", side="top")
            this_combat_frame.place(
                anchor="nw", height=220, width=150, x=2, y=2)
            frame_15 = ttk.Frame(this_mainframe)
            frame_15.configure(height=200, width=200)
            frame_23 = ttk.Frame(frame_15)
            frame_23.configure(height=200, width=200)
            this_function_label = ttk.Label(frame_23)
            this_function_label.configure(text='Functions')
            this_function_label.grid(column=0, columnspan=2, row=0)
            frame_6 = ttk.Frame(frame_23)
            frame_6.configure(height=7, width=1)
            frame_6.grid(column=0, row=1)
            this_renametab_button = ttk.Button(frame_23)
            this_renametab_button.configure(text='Rename Tab')
            this_renametab_button.grid(column=0, row=2)
            this_renametab_button.configure(
                command=lambda e_id=enemy.id: self.renametab_button_action(e_id))
            this_delete_tab_button = ttk.Button(frame_23)
            this_delete_tab_button.configure(text='Delete Tab')
            this_delete_tab_button.grid(column=1, row=2)
            this_delete_tab_button.configure(command=lambda e_id=enemy.id: self.delete_tab_button_action(e_id))
            this_clearlog_button = ttk.Button(frame_23)
            this_clearlog_button.configure(text='Clear Log')
            this_clearlog_button.grid(column=0, row=3)
            this_clearlog_button.configure(command=lambda e_id=enemy.id: self.clearlog_action(e_id))
            this_savetobeastiary_button = ttk.Button(frame_23)
            this_savetobeastiary_button.configure(text='Save to BST')
            this_savetobeastiary_button.grid(column=1, row=3)
            this_savetobeastiary_button.configure(
                command=lambda e_id=enemy.id: self.savetobeastiary_action(e_id))
            frame_23.grid(column=0, row=0, sticky="n")
            frame_16 = ttk.Frame(frame_15)
            frame_16.configure(height=200, width=200)
            this_hm_label = ttk.Label(frame_16)
            this_hm_label.configure(
                font="{Arial} 10 {}",
                justify="right",
                text='Highest Miss:')
            this_hm_label.grid(column=0, row=0, sticky="e")
            this_lh_label = ttk.Label(frame_16)
            this_lh_label.configure(text='Lowest Hit:')
            this_lh_label.grid(column=0, row=1, sticky="e")
            this_td_label = ttk.Label(frame_16)
            this_td_label.configure(text='Total Damage:')
            this_td_label.grid(column=0, row=2, sticky="e")
            this_hm_val_label = ttk.Label(frame_16)
            this_hm_val_label.configure(text=enemy.highest_miss)
            this_hm_val_label.grid(column=1, row=0, sticky="w")
            this_lh_val_label = ttk.Label(frame_16)
            this_lh_val_label.configure(text=enemy.lowest_hit)
            this_lh_val_label.grid(column=1, row=1, sticky="w")
            this_td_val_label = ttk.Label(frame_16)
            this_td_val_label.configure(text=enemy.damage_taken)
            this_td_val_label.grid(column=1, row=2, sticky="w")
            frame_16.grid(column=1, row=0, sticky="e")
            frame_25 = ttk.Frame(frame_15)
            frame_25.configure(height=20, width=110)
            frame_25.grid(column=0, columnspan=2, row=1)
            frame_20 = ttk.Frame(frame_15)
            frame_20.configure(height=200, width=100)
            this_dt_header_label = ttk.Label(frame_20)
            this_dt_header_label.configure(text='Damage Type')
            this_dt_header_label.pack(side="top")
            this_damagetype_box = ttk.Combobox(frame_20)
            this_damagetype_box['values'] = ['', 'Piercing', 'Slashing', 'Bludgeoning', 'Fire', 'Cold', 'Lightning', 'Thunder', 'Poison', 'Acid', 'Psychic', 'Necrotic', 'Radiant', 'Force', 'Physical', 'Magical', 'Other']
            this_damagetype_box.current(0)
            this_damagetype_box.pack(side="top")
            frame_1 = ttk.Frame(frame_20)
            frame_1.configure(height=130, width=140)
            this_DT_immune_rbtn = ttk.Radiobutton(frame_1)
            this_DT_immune_rbtn.configure(text='(x0.0) Immune')
            this_DT_immune_rbtn.place(anchor="nw", x=0, y=0)
            this_DT_resistant_rbtn = ttk.Radiobutton(frame_1)
            this_DT_resistant_rbtn.configure(text='(x0.5) Resistant')
            this_DT_resistant_rbtn.place(anchor="nw", x=0, y=20)
            this_DT_normal_rbtn = ttk.Radiobutton(frame_1)
            this_DT_normal_rbtn.configure(text='(x1.0) Normal')
            this_DT_normal_rbtn.place(anchor="nw", x=0, y=40)
            this_DT_weak_rbtn = ttk.Radiobutton(frame_1)
            this_DT_weak_rbtn.configure(text='(x2.0) Weak')
            this_DT_weak_rbtn.place(anchor="nw", x=0, y=60)

            # Generate a unique ID for each tab
            # Create a new dictionary for this enemy
            self.enemy_vars[enemy.id] = {}

            # Create the BooleanVar instances for this enemy
            self.enemy_vars[enemy.id]['immune'] = tk.BooleanVar()
            self.enemy_vars[enemy.id]['resistant'] = tk.BooleanVar()
            self.enemy_vars[enemy.id]['normal'] = tk.BooleanVar()
            self.enemy_vars[enemy.id]['weak'] = tk.BooleanVar()

            # Configure the radio buttons to use the BooleanVar instances for this enemy
            this_DT_immune_rbtn.configure(variable=self.enemy_vars[enemy.id]['immune'], command=lambda: [self.enemy_vars[enemy.id]['resistant'].set(False), self.enemy_vars[enemy.id]['normal'].set(False), self.enemy_vars[enemy.id]['weak'].set(False)])
            this_DT_resistant_rbtn.configure(variable=self.enemy_vars[enemy.id]['resistant'], command=lambda: [self.enemy_vars[enemy.id]['immune'].set(False), self.enemy_vars[enemy.id]['normal'].set(False), self.enemy_vars[enemy.id]['weak'].set(False)])
            this_DT_normal_rbtn.configure(variable=self.enemy_vars[enemy.id]['normal'], command=lambda: [self.enemy_vars[enemy.id]['immune'].set(False), self.enemy_vars[enemy.id]['resistant'].set(False), self.enemy_vars[enemy.id]['weak'].set(False)])
            this_DT_weak_rbtn.configure(variable=self.enemy_vars[enemy.id]['weak'], command=lambda: [self.enemy_vars[enemy.id]['immune'].set(False), self.enemy_vars[enemy.id]['resistant'].set(False), self.enemy_vars[enemy.id]['normal'].set(False)])
            
            frame_1.pack(side="top")
            frame_20.grid(column=0, row=2, sticky="n")
            frame_19 = ttk.Frame(frame_15)
            frame_19.configure(height=200, width=100)
            this_hr_header_label = ttk.Label(frame_19)
            this_hr_header_label.configure(text='Hit Roll')
            this_hr_header_label.pack(side="top")
            this_hitroll_entry = ttk.Entry(frame_19)
            this_hitroll_entry.pack(side="top")
            this_attack_hit_button = ttk.Checkbutton(frame_19)
            self.enemy_vars[enemy.id]['attack_hit'] = tk.BooleanVar()
            self.enemy_vars[enemy.id]['attack_hit_button'] = this_attack_hit_button
            this_attack_hit_button.configure(
                text='Attack Hit?', variable=self.enemy_vars[enemy.id]['attack_hit'])
            this_attack_hit_button.pack(side="top")

            # Call invoke twice to set the button to not selected
            this_attack_hit_button.invoke()
            this_attack_hit_button.invoke()
            
            this_dr_header_label = ttk.Label(frame_19)
            this_dr_header_label.configure(text='Damage Roll')
            this_dr_header_label.pack(side="top")
            this_dmgroll_entry = ttk.Entry(frame_19)
            this_dmgroll_entry.pack(side="top")
            this_add_to_tracker_button = ttk.Button(frame_19)
            this_add_to_tracker_button.configure(text='Add to Tracker')
            this_add_to_tracker_button.pack(side="top")
            this_add_to_tracker_button.configure(
                command=lambda e_id=enemy.id: self.add_to_tracker_button_action(e_id))
            frame_19.grid(column=1, row=2, sticky="ne")
            frame_15.place(anchor="nw", height=220, width=280, x=150, y=0)
            this_mainframe.pack(side="top")
            self.combat_notebook.add(this_mainframe, text=enemy.name)
            # end of dynamic content

            # Add the enemy's UI components to the enemy object
            ui_components = {
                'combat_log': this_combat_log,
                'hitroll_entry': this_hitroll_entry,
                'damage_roll': this_dmgroll_entry,
                'damagetype_box': this_damagetype_box,
                'immune': self.enemy_vars[enemy.id]['immune'],
                'resistant': self.enemy_vars[enemy.id]['resistant'],
                'weak': self.enemy_vars[enemy.id]['weak'],
                'attack_hit': self.enemy_vars[enemy.id]['attack_hit'],
                'highest_miss_val': this_hm_val_label,
                'lowest_hit_val': this_lh_val_label,
                'total_damage_val': this_td_val_label
            }
            enemy.ui_components = ui_components

        # Select the tab that was selected before reloading the UI
        try:
            self.combat_notebook.select(selected_tab)
        except tk.TclError:
            try:
                self.combat_notebook.select(0)
            except tk.TclError:
                pass
                

    def run(self):
        self.mainwindow.mainloop()

    def new_tab_button_action(self):
        # Create a new enemy for the encounter
        new_enemy = EncounterEnemy(
            name="Enemy " + str(EncounterEnemy.next_id),
            damage_taken=0,
            lowest_hit=999,
            highest_miss=0,
            combat_log=CombatLog()
        )

        # Add the enemy to the list of enemies
        self.enemies.append(new_enemy)

        # Reload the UI to display the new enemy
        self.reload_ui()

    def beastiary_button_action(self):
        # Show a popup warning that this feature is not yet implemented
        messagebox.showinfo("Beastiary", "This feature is not yet implemented")

    def undo_button_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Undo the last log entry
        if enemy is not None and enemy.combat_log is not None:
            enemy.combat_log.undo_log()

        # Reload the UI to display the updated combat log
        self.reload_ui()

    def renametab_button_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Show a popup to get the new name for the enemy
        new_name = simpledialog.askstring("Rename Tab", "Enter the new name for the enemy:")

        # Update the enemy's name if the enemy object is not None
        if enemy is not None:
            enemy.name = new_name

        # Reload the UI to display the updated name
        self.reload_ui()

    def delete_tab_button_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Remove the enemy from the list of enemies
        self.enemies.remove(enemy)

        # Reload the UI to remove the tab for the deleted enemy
        self.reload_ui()

    def clearlog_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Clear the combat log for the enemy if it exists
        if enemy is not None and enemy.combat_log is not None:
            enemy.combat_log.clear_log()

        # Reload the UI to display the cleared combat log
        self.reload_ui()

    def savetobeastiary_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Show a popup warning that this feature is not yet implemented
        messagebox.showinfo("Save to Beastiary", "This feature is not yet implemented")

    def add_to_tracker_button_action(self, enemy_id):
        # Get the enemy object from the list of enemies
        enemy = next((x for x in self.enemies if x.id == enemy_id), None)

        # Check if the enemy object is None
        if enemy is None:
            return

        # Get the ui components for the enemy, which are stored in the enemy object
        ui_components = enemy.ui_components

        # Ensure that the hit roll is not empty
        if ui_components['hitroll_entry'].get() == "":
            messagebox.showerror("Error", "Please enter a hit roll")
            return
        
        # Get whether the attack hit from the checkbox
        attack_hit = self.enemy_vars[enemy.id]['attack_hit_button'].state()[0] == 'selected' #This works, for some reason
        
        if(not attack_hit):
            # If the attack missed, get the attack roll and the highest miss value
            hit_roll = int(ui_components['hitroll_entry'].get())
            highest_miss = int(ui_components['highest_miss_val'].cget("text"))

            # Update the highest miss value if the attack roll is higher
            if hit_roll > highest_miss:
                highest_miss = hit_roll
                enemy.highest_miss = highest_miss

            # Add the attack roll to the combat log
            log = CombatLog_LL()
            log.hr = hit_roll
            log.dm = "miss"
            enemy.combat_log.add_log(log)
        else:
            # Get the attack roll, damage roll, damage type, damage modfiers, total damage done, and the lowest hit value
            hit_roll = int(ui_components['hitroll_entry'].get())
            damage_roll = int(ui_components['damage_roll'].get())
            damage_type = ui_components['damagetype_box'].get()
            immune = ui_components['immune'].get()
            resistant = ui_components['resistant'].get()
            weak = ui_components['weak'].get()
            lowest_hit = int(ui_components['lowest_hit_val'].cget("text"))
            total_damage = int(ui_components['total_damage_val'].cget("text"))

            # Ensure the damage roll is not empty
            if damage_roll == "":
                messagebox.showerror("Error", "Please enter a damage roll")
                return

            # If the damage type is empty, set it to "Other"
            if damage_type == "":
                damage_type = "Other"

            # If none of the damage modifiers are selected, set the damage to normal
            if not immune and not resistant and not weak:
                immune = False
                resistant = False
                weak = False

            # Update the lowest hit value if the attack roll is lower
            if hit_roll < lowest_hit:
                lowest_hit = hit_roll
                enemy.lowest_hit = lowest_hit

            # Calculate the damage absorbed based on the damage modifiers, update 
            # the total damage done, and update the damage dictionary
            this_dm = "NRM"
            damage_absorbed = damage_roll
            ddt = enemy.damage_dict
            if immune:
                damage_absorbed = 0
                this_dm = "IMM"
                if damage_type not in ddt["immune"]:
                    ddt["immune"].append(damage_type)
            elif resistant: # x0.5, round down
                damage_absorbed = damage_roll // 2
                this_dm = "RES"
                if damage_type not in ddt["resistant"]:
                    ddt["resistant"].append(damage_type)
            elif weak:
                damage_absorbed = damage_roll * 2
                this_dm = "WEA"
                if damage_type not in ddt["weak"]:
                    ddt["weak"].append(damage_type)

            # Update the total damage with the absorbed damage
            total_damage += damage_absorbed
            enemy.damage_taken = total_damage

            # For each item to be added to the combat log, ensure that it is not None
            if hit_roll is None:
                hit_roll = 0
            if damage_roll is None:
                damage_roll = 0
            if damage_type is None:
                damage_type = "Other"
            if damage_absorbed is None:
                damage_absorbed = 0
            
            # Add entry to the combat log
            log = CombatLog_LL(
                hr=hit_roll,
                dm=this_dm,
                dv=damage_roll,
                dt=damage_type,
                da=damage_absorbed
            )
            enemy.combat_log.add_log(log)

        # Reload the UI to display the updated combat log
        self.reload_ui()

class EncounterEnemy:
    next_id = 0
    def __init__(self, name="Unnamed", damage_taken=0, lowest_hit=0, highest_miss=999, combat_log=None, ui_components=None):
        self.id = EncounterEnemy.next_id
        EncounterEnemy.next_id += 1

        self.name = name
        self.damage_taken = damage_taken
        self.lowest_hit = lowest_hit
        self.highest_miss = highest_miss
        self.damage_dict = {
            "immune": [],
            "resistant": [],
            "weak": []
        }
        self.combat_log = combat_log
        self.ui_components = ui_components

class CombatLog:
    def __init__(self):
        self.head = None

    def add_log(self, log):
        if self.head is None:
            self.head = log
        else:
            log.next = self.head
            self.head.prev = log
            self.head = log

    def remove_log(self, log):
        if log.prev is None:
            self.head = log.next
        else:
            log.prev.next = log.next
        if log.next is not None:
            log.next.prev = log.prev

    def clear_log(self):
        current = self.head
        while current is not None:
            next_node = current.next
            current.prev = None
            current.next = None
            current = next_node
        self.head = None

    def undo_log(self):
        if self.head is not None:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None

        # Recalculate the total damage taken, lowest hit, and highest miss
        current = self.head
        total_damage = 0
        lowest_hit = 999
        highest_miss = 0

        while current is not None:
            if current.dm != "miss":
                total_damage += current.da
                if current.hr < lowest_hit:
                    lowest_hit = current.hr
            else:
                if current.hr > highest_miss:
                    highest_miss = current.hr
            current = current.next

class CombatLog_LL:
    def __init__(self, hr=0, dm="x0.0", dv=0, dt="Other", da=0):
        self.hr = hr    # hit roll
        self.dm = dm    # damage modifier
        self.dv = dv    # damage value (rolled)
        self.dt = dt    # damage type
        self.da = da    # damage absorbed (inc resistances)
        
        # linked list pointer
        self.prev = None
        self.next = None

    def to_string(self):
        if(self.dm == "miss"):
            return f"H{self.hr} | Miss"
        else:
            # Truncate the damage modifier to 3 characters
            if len(self.dt) > 3:
                this_dt = self.dt[:3]
            return f"{self.hr} | {self.dv} | {this_dt} | {self.dm} | {self.da}"

if __name__ == "__main__":
    app = EncounterTracker()
    app.run()

