import tkinter as tk
from tkinter import messagebox, ttk

from .game_data import GameData
from .save_manager import SaveManager


class MainApp(tk.Tk):
    """
    Main Tkinter application for Void War Save Editor.
    Allows editing of resources, equipment, and cargo slots.
    """

    def __init__(self, save_manager: SaveManager, game_data: GameData):
        """
        Initialize the main application window.
        """
        super().__init__()
        self.save_manager = save_manager
        self.game_data = game_data

        self.title("Void War Save Editor")
        self.geometry("800x600")

        if not self.save_manager.save_file_path:
            self.destroy()
            return

        self._create_widgets()
        self._populate_data()

    def _create_label_entry_row(self, parent, label_text, var, row_idx):
        """
        Helper to create a label and entry row in a grid.
        """
        ttk.Label(parent, text=label_text).grid(
            row=row_idx, column=0, padx=5, pady=5, sticky=tk.W
        )
        ttk.Entry(parent, textvariable=var).grid(row=row_idx, column=1, padx=5, pady=5)

    def _create_widgets(self):
        """
        Create and layout all widgets in the main window.
        """
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Resources Frame
        resources_frame = ttk.LabelFrame(main_frame, text="Resources")
        resources_frame.pack(fill=tk.X, pady=5)
        self.scrap_var = tk.StringVar()
        self.missile_var = tk.StringVar()

        # Integer validation function for entry fields
        def validate_int(P):
            if P == "":
                return True
            try:
                int(P)
                return True
            except ValueError:
                return False

        vcmd = (self.register(validate_int), "%P")

        ttk.Label(resources_frame, text="Scrap:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        scrap_entry = ttk.Entry(
            resources_frame,
            textvariable=self.scrap_var,
            validate="key",
            validatecommand=vcmd,
        )
        scrap_entry.grid(row=0, column=1, padx=5, pady=5)
        scrap_max_btn = ttk.Button(
            resources_frame,
            text="9999",
            command=lambda: self.scrap_var.set("9999"),
            width=5,
        )
        scrap_max_btn.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(resources_frame, text="Missiles:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        missile_entry = ttk.Entry(
            resources_frame,
            textvariable=self.missile_var,
            validate="key",
            validatecommand=vcmd,
        )
        missile_entry.grid(row=1, column=1, padx=5, pady=5)
        missile_max_btn = ttk.Button(
            resources_frame,
            text="9999",
            command=lambda: self.missile_var.set("9999"),
            width=5,
        )
        missile_max_btn.grid(row=1, column=2, padx=5, pady=5)

        # Equipment Frame
        equipment_frame = ttk.LabelFrame(main_frame, text="Equipment")
        equipment_frame.pack(fill=tk.X, pady=5)
        self.equipment_combos = []
        self.equipment_select_btns = []
        item_names = ["Empty Slot"] + list(self.game_data.item_id_name_map.values())
        categories = ["armor", "consumable", "psychic", "tool", "weapon"]
        for i in range(8):
            row = ttk.Frame(equipment_frame)
            row.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(row, text=f"Slot {i+1}:").pack(side=tk.LEFT)
            combo = ttk.Combobox(row, width=25, state="readonly")
            combo["values"] = item_names
            combo.pack(side=tk.LEFT, padx=5)
            self.equipment_combos.append(combo)
            btns = []
            for cat in categories:
                btn = ttk.Button(
                    row,
                    text=cat.capitalize(),
                    command=lambda idx=i, cat=cat: self._open_equipment_table(idx, cat),
                    width=10,
                )
                btn.pack(side=tk.LEFT, padx=2)
                btns.append(btn)
            self.equipment_select_btns.append(btns)
        # (No qty_entry, hidden from UI)

        # Cargo Frame
        cargo_frame = ttk.LabelFrame(main_frame, text="Cargo")
        cargo_frame.pack(fill=tk.X, pady=5)
        self.cargo_combos = []
        self.cargo_select_btns = []
        ship_weapon_types = set(
            item_data.get("Type", "")
            for item_data in self.game_data.ship_weapon.values()
        )
        for i in range(4):
            row = ttk.Frame(cargo_frame)
            row.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(row, text=f"Slot {i+1}:").pack(side=tk.LEFT)
            combo = ttk.Combobox(row, width=25, state="readonly")
            combo["values"] = ["Empty Slot"] + [
                item_data.get("Name", "")
                for item_data in self.game_data.ship_weapon.values()
                if item_data.get("Name", "")
            ]
            combo.pack(side=tk.LEFT, padx=5)
            self.cargo_combos.append(combo)
            btns = []
            for weapon_type in ship_weapon_types:
                btn = ttk.Button(
                    row,
                    text=weapon_type,
                    command=lambda idx=i, weapon_type=weapon_type: self._open_cargo_table(
                        idx, weapon_type
                    ),
                    width=10,
                )
                btn.pack(side=tk.LEFT, padx=2)
                btns.append(btn)
            self.cargo_select_btns.append(btns)

        # Save Button
        save_button = ttk.Button(
            main_frame, text="Save Changes", command=self._save_changes
        )
        save_button.pack(pady=10)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _populate_data(self):
        """
        Populate UI widgets with current save data.
        """
        self.scrap_var.set(str(int(self.save_manager.get_scrap())))
        self.missile_var.set(str(int(self.save_manager.get_missile_count())))

        # Equipment
        equipment_list = self.save_manager.get_equipment_list()
        for i, combo in enumerate(self.equipment_combos):
            item_id = equipment_list[i] if i < len(equipment_list) else -1.0
            item_name = self.game_data.item_id_name_map.get(str(item_id), "Empty Slot")
            combo.set(item_name)
        # (No qty_entry population, hidden from UI)

        # Cargo
        cargo_list = self.save_manager.get_cargo_list()
        ship_weapon_id_name_map = {
            k: v.get("Name", "") for k, v in self.game_data.ship_weapon.items()
        }
        for i, combo in enumerate(self.cargo_combos):
            item_id = cargo_list[i] if i < len(cargo_list) else -1.0
            item_name = ship_weapon_id_name_map.get(str(item_id), "Empty Slot")
            combo.set(item_name)

    def _save_changes(self):
        """
        Save changes made in the UI to the save file.
        """
        try:
            new_scrap = int(self.scrap_var.get())
            new_missiles = int(self.missile_var.get())
            self.save_manager.set_scrap(new_scrap)
            self.save_manager.set_missile_count(new_missiles)

            # Equipment
            new_equipment, new_equipment_qty = self._get_equipment_data()
            self.save_manager.set_equipment_list(new_equipment, new_equipment_qty)

            # Cargo
            new_cargo = self._get_cargo_data()
            self.save_manager.set_cargo_list(new_cargo)

            self.save_manager.save_changes()
            self.status_var.set("Changes saved successfully!")
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to save changes: {e}")

    def _get_equipment_data(self):
        """
        Retrieve equipment and quantity data from UI.
        Returns:
            tuple: (equipment_list, equipment_qty_list)
        """
        equipment_list = []
        equipment_qty_list = []
        consumable_ids = set(self.game_data.consumable.keys())
        for combo in self.equipment_combos:
            name = combo.get()
            item_id = (
                self.game_data.item_name_id_map.get(name, -1.0)
                if name != "Empty Slot"
                else -1.0
            )
            equipment_list.append(item_id)
            # Set quantity: 2 if consumable, 1 if other equipment, 0 if empty
            if item_id == -1.0:
                qty = 0
            elif str(item_id) in consumable_ids:
                qty = 2
            else:
                qty = 1
            equipment_qty_list.append(qty)
        return equipment_list, equipment_qty_list

    def _get_cargo_data(self):
        """
        Retrieve cargo data from UI.
        Returns:
            list: cargo_list
        """
        cargo_list = []
        # Only allow ship_weapon items
        ship_weapon_name_id_map = {
            v.get("Name", ""): k for k, v in self.game_data.ship_weapon.items()
        }
        for combo in self.cargo_combos:
            name = combo.get()
            item_id = (
                ship_weapon_name_id_map.get(name, -1.0)
                if name != "Empty Slot"
                else -1.0
            )
            cargo_list.append(item_id)
        return cargo_list

    def _open_equipment_table(self, slot_idx, category):
        """
        Open a table window for selecting equipment for a given slot and category.
        """
        cat_dict = getattr(self.game_data, category, {})
        # Get all columns from the first item (if any)
        columns = []
        if cat_dict:
            first_item = next(iter(cat_dict.values()))
            columns = [k for k in first_item.keys()]
            # Always include Name and Description if present
            if "Name" not in columns:
                columns.insert(0, "Name")
            if "Description" not in columns and "Description" in first_item:
                columns.append("Description")
        else:
            columns = ["Name"]

        win = tk.Toplevel(self)
        win.title(f"Select {category.capitalize()}")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        # Insert items
        for item_id, data in cat_dict.items():
            values = [data.get(col, "") for col in columns]
            tree.insert("", "end", values=values, iid=item_id)
        # Add "Empty Slot" option
        empty_values = ["Empty Slot"] + [""] * (len(columns) - 1)
        tree.insert("", "end", values=empty_values, iid="-1.0")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def select_item():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Equipment", "Please select an item.")
                return
            item_id = selected[0]
            # Set the combo box value for the slot
            if item_id == "-1.0":
                self.equipment_combos[slot_idx].set("Empty Slot")
            else:
                name = cat_dict[item_id].get("Name", "")
                self.equipment_combos[slot_idx].set(name)
            win.destroy()

        select_btn = ttk.Button(win, text="Select", command=select_item)
        select_btn.pack(pady=5)

        # Allow double-click to select
        def on_double_click(event):
            select_item()

        tree.bind("<Double-1>", on_double_click)

    def _open_cargo_table(self, slot_idx, weapon_type):
        """
        Open a table window for selecting cargo items filtered by weapon type.
        """
        filtered_items = {
            item_id: data
            for item_id, data in self.game_data.ship_weapon.items()
            if data.get("Type", "") == weapon_type
        }
        # Get all columns from the first item (if any)
        columns = []
        if filtered_items:
            first_item = next(iter(filtered_items.values()))
            columns = [k for k in first_item.keys()]
            # Always include Name and Description if present
            if "Name" not in columns:
                columns.insert(0, "Name")
            if "Description" not in columns and "Description" in first_item:
                columns.append("Description")
        else:
            columns = ["Name"]

        win = tk.Toplevel(self)
        win.title(f"Select {weapon_type}")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        # Insert items
        for item_id, data in filtered_items.items():
            values = [data.get(col, "") for col in columns]
            tree.insert("", "end", values=values, iid=item_id)
        # Add "Empty Slot" option
        empty_values = ["Empty Slot"] + [""] * (len(columns) - 1)
        tree.insert("", "end", values=empty_values, iid="-1.0")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def select_item():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Cargo", "Please select an item.")
                return
            item_id = selected[0]
            # Set the combo box value for the slot
            if item_id == "-1.0":
                self.cargo_combos[slot_idx].set("Empty Slot")
            else:
                name = filtered_items[item_id].get("Name", "")
                self.cargo_combos[slot_idx].set(name)
            win.destroy()

        select_btn = ttk.Button(win, text="Select", command=select_item)
        select_btn.pack(pady=5)

        def on_double_click(event):
            select_item()

        tree.bind("<Double-1>", on_double_click)
