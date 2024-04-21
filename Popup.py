#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
from pygubu.widgets.scrolledframe import ScrolledFrame

class Popup:
    @staticmethod
    def Message(message, master=None):
        messagebox.showinfo("Message", message=message)

    @staticmethod
    def Roll_Result(text_to_show, master=None):
        messagebox.showinfo("Roll Result", message=text_to_show)

    @staticmethod
    def Change_One_Value(description, current_value, master=None):
        return simpledialog.askstring("Change Value", prompt=description, initialvalue=current_value)

    @staticmethod
    def ComboBoxChoice(header_text, combo_choices, callback, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=120, width=150)
        header_label = ttk.Label(frame1)
        header_label.configure(text=header_text)
        header_label.place(anchor="n", x=75, y=0)
        choice_box = ttk.Combobox(frame1)
        choice_box.configure(values=combo_choices)
        choice_box.place(anchor="n", x=75, y=40)
        ok_button = ttk.Button(frame1)
        ok_button.configure(text='OK')
        ok_button.place(anchor="s", x=75, y=110)
        ok_button.configure(command=lambda: Popup.combo_ok_button_action(callback, choice_box, toplevel1))
        frame1.pack(side="top")

        # Main widget
        mainwindow = toplevel1
        callback = callback

        mainwindow.mainloop()

    @staticmethod
    def combo_ok_button_action(callback, combo_box, mainwindow):
        val = combo_box.get()
        mainwindow.destroy()
        callback(val)

    @staticmethod
    def EditItemPopup(header_text, item_to_edit, callback, master=None):
        callback = callback
        backup = item_to_edit.copy()               

        # build ui
        edit_item_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        edit_item_toplevel.configure(height=500, width=300)
        edit_item_toplevel.maxsize(300, 1000)
        edit_item_toplevel.minsize(300, 500)
        main_frame = ttk.Frame(edit_item_toplevel)
        main_frame.configure(height=200, width=300)
        header_label = ttk.Label(main_frame)
        header_label.configure(
            font="{Arial} 12 {bold}",
            justify="left",
            text='Edit Item')
        header_label.pack(side="top")
        attributes_frame = ttk.Frame(main_frame)
        attributes_frame.configure(height=450, width=300)

        attributeslist_scrollframe = ScrolledFrame(
            attributes_frame, scrolltype="both")
        attributeslist_scrollframe.innerframe.configure(width=300)
        attributeslist_scrollframe.configure(usemousewheel=False)

        # Start of dynamic content
        item_list = []
        for item_property in item_to_edit:
            ui_items_list = []

            # this_frame = ttk.Frame(main_frame)
            this_frame = ttk.Frame(attributeslist_scrollframe.innerframe)
            this_frame.configure(height=20, width=300)
            this_label = ttk.Label(this_frame)
            this_label.configure(text=item_property.name)
            this_label.place(anchor="ne", x=75, y=0)

            """
                Decide what kind of input to use, from the "input type" in each EditItem_Option object.
                "" = No restrictions, just use an Entry widget
                "b" = Boolean, use a tick to indicate True or False
                "int" = Integer, only allow numbers
                "+ve_int" = Positive Integer, only allow positive numbers (including 0)
                "av" = Accepted Values, only allow values from the list of accepted values (in EditItem_Option object)
            """
            if item_property.input_type == "b":
                this_genericinput = ttk.Checkbutton(this_frame)
                boolean_var = tk.BooleanVar()
                boolean_var.set(item_property.current_value)
                this_genericinput.configure(variable=boolean_var)
                this_genericinput.place(anchor="nw", x=85, y=0)

            elif item_property.input_type == "int":
                this_genericinput = ttk.Entry(this_frame)
                this_genericinput.insert(0, item_property.current_value)
                this_genericinput.place(anchor="nw", width=200, x=85, y=0)

            elif item_property.input_type == "+ve_int":
                this_genericinput = ttk.Entry(this_frame)
                this_genericinput.insert(0, item_property.current_value)
                this_genericinput.place(anchor="nw", width=200, x=85, y=0)

            elif item_property.input_type == "av":
                this_genericinput = ttk.Combobox(this_frame)
                this_genericinput.configure(values=item_property.accepted_values)
                if item_property.current_value in item_property.accepted_values:
                    this_genericinput.set(item_property.current_value)
                else:
                    this_genericinput.set(item_property.accepted_values[0])
                this_genericinput.place(anchor="nw", width=200, x=85, y=0)
            else:
                this_genericinput = ttk.Entry(this_frame)
                this_genericinput.insert(0, item_property.current_value)
                this_genericinput.place(anchor="nw", width=200, x=85, y=0)

            this_frame.pack(pady=5, side="top")

            ui_items_list.append(this_frame)
            ui_items_list.append(this_label)
            ui_items_list.append(this_genericinput)
            item_list.append(ui_items_list)

        # End of dynamic content

        attributeslist_scrollframe.place(
            anchor="nw", height=450, width=300, x=0, y=0)
        attributes_frame.pack(expand=True, fill="both", side="top")
        button_frame = ttk.Frame(main_frame)
        button_frame.configure(height=200, width=300)
        delete_button = ttk.Button(button_frame)
        delete_button.configure(text='Delete')
        delete_button.pack(padx=15, side="left")
        delete_button.configure(command=lambda: Popup.editItem_delete_button_action(callback=callback, mainwindow=edit_item_toplevel))
        cancel_button = ttk.Button(button_frame)
        cancel_button.configure(text='Cancel')
        cancel_button.pack(padx=15, side="left")
        cancel_button.configure(command=lambda: Popup.editItem_cancel_button_action(callback=callback, backup=backup, mainwindow=edit_item_toplevel))
        ok_button = ttk.Button(button_frame)
        ok_button.configure(text='OK')
        ok_button.pack(padx=15, side="right")
        ok_button.configure(command=lambda: Popup.editItem_ok_button_action(callback=callback, input_list=item_to_edit, item_list=item_list, mainwindow=edit_item_toplevel))
        button_frame.pack(side="top")
        main_frame.pack(expand=True, fill="both", side="top")

        # Main widget
        mainwindow = edit_item_toplevel

        # Main widget
        mainwindow = edit_item_toplevel

        mainwindow.mainloop()

    @staticmethod
    def editItem_delete_button_action(callback, mainwindow):
        # Ask the user to confirm that they want to delete the item
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?\n(This action cannot be undone)"):
            # Call the callback function with an empty dictionary (to indicate that the 
            # item should be deleted), and close the window
            callback(None)
            mainwindow.destroy()
        
        # Else, do nothing

    @staticmethod
    def editItem_cancel_button_action(callback, backup, mainwindow):
        # Extract the values from the backup dictionary and call the callback function with the backup values
        new_item = {}
        for prop in backup:
            new_item[prop.name] = prop.current_value

        callback(new_item)
        mainwindow.destroy()

    @staticmethod
    def editItem_ok_button_action(callback, input_list, item_list, mainwindow):
        
        # new_item = {}
        # for item in item_list:
        #     new_item[item[1].cget("text")] = item[2].get()

        """ 
            Test if the input is valid using the "input type" in each EditItem_Option object
            "" = No restrictions, just use an Entry widget
            "b" = Boolean, use a tick to indicate True or False
            "int" = Integer, only allow numbers
            "+ve_int" = Positive Integer, only allow positive numbers (including 0)
            "av" = Accepted Values, only allow values from the list of accepted values (in EditItem_Option object)
        """
        # Create a dictionary of the new item, with the key being the name of the property and the value being the new value
        new_item = {}
        prop_errors = []

        # Check each item in the list of items to edit
        for item in item_list:

            # Get the key (name of the property) and value (new value) of the item, and the EditItem_Option object for that item
            key = item[1].cget("text")
            value = None
            edit_item_option = input_list[item_list.index(item)]

            # Get the value of the item, depending on the input type
            if isinstance(item[2], ttk.Checkbutton):
                value = item[2].instate(('selected',))
            else:
                value = item[2].get()

            # Check if the value is valid, depending on the input type
                
            # If the input type is a boolean, try to convert the value to a boolean
            if edit_item_option.input_type == "b":
                try:
                    value = bool(value)
                except:
                    prop_errors.append(f"Invalid input for {key}: {value}. Must be a boolean.")

            # If the input type is an integer, try to convert the value to an integer
            elif edit_item_option.input_type == "int":
                try:
                    value = int(value)
                except:
                    prop_errors.append(f"Invalid input for {key}: {value}. Must be an integer.")

            # If the input type is a positive integer, try to convert the value to a positive integer
            elif edit_item_option.input_type == "+ve_int":
                try:
                    value = int(value)
                    if value < 0:
                        prop_errors.append(f"Invalid input for {key}: {value}. Must be a positive integer.")
                except:
                    prop_errors.append(f"Invalid input for {key}: {value}. Must be a positive integer.")

            # If the input type is accepted values, check if the value is in the list of accepted values
            elif edit_item_option.input_type == "av":
                if value not in edit_item_option.accepted_values:
                    prop_errors.append(f"Invalid input for {key}: {value}. Must be one of the accepted values.")

            # If the input type is not specified, just use the value as it is
                    
            # Add the new item to the dictionary
            new_item[key] = value

        # If there are no errors, call the callback function with the new item and close the window
        if len(prop_errors) > 0:
            messagebox.showerror("Error", "\n".join(prop_errors))
        
        else:
            # Call the callback function with the new item, and close the window
            callback(new_item)
            mainwindow.destroy()

class EditItem_Option:
    def __init__(self, name, current_value, input_type="", accepted_values=[]):
        self.name = name
        self.current_value = current_value
        self.input_type = input_type
        self.accepted_values = accepted_values

def combo_box_callback(choice):
    print(f"Choice: {choice}")

def edit_item_callback(item):
    print(f"Item: {item}")

if __name__ == "__main__":
    # # Example usage:
    Popup.Roll_Result("You rolled a 20!")

    new_value = Popup.Change_One_Value("Enter new value:", "old value")
    print(f"New value: {new_value}")

    Popup.ComboBoxChoice("Choose a number", [1, 2, 3, 4, 5], combo_box_callback)
    
    Popup.EditItemPopup("Edit Item", {
        "Name": "Rick", 
        "Url" : "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }, edit_item_callback)
    
    Popup.EditItemPopup("Edit Item", [
        EditItem_Option("Name", "Rick"),
        EditItem_Option("Url", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        EditItem_Option("Age", 20, "int"),
        EditItem_Option("Is Human", True, "b"),
        EditItem_Option("Favourite Colour", "Red", "av", ["Red", "Blue", "Green", "Yellow"]),
        EditItem_Option("Number of Legs", 2, "+ve_int"),
        ], edit_item_callback)
