import logging
import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial

from .game_data import GameData
from .save_manager import SaveManager

logger = logging.getLogger(__name__)


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
        self.minsize(700, 700)
        self.geometry("700x700")

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

        # Add scrollable canvas
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Resources Frame
        resources_frame = ttk.LabelFrame(scrollable_frame, text="Resources")
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
        equipment_frame = ttk.LabelFrame(scrollable_frame, text="Equipment")
        equipment_frame.pack(fill=tk.X, pady=5)
        self.equipment_combos = []
        self.equipment_descriptions = []
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
            combo.bind(
                "<<ComboboxSelected>>",
                lambda e, idx=i: self._update_equipment_description(idx),
            )
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
            description_label = ttk.Label(equipment_frame, text="", wraplength=400)
            description_label.pack(fill=tk.X, padx=5, pady=2)
            self.equipment_descriptions.append(description_label)

        # Cargo Frame
        cargo_frame = ttk.LabelFrame(scrollable_frame, text="Cargo")
        cargo_frame.pack(fill=tk.X, pady=5)
        self.cargo_combos = []
        self.cargo_descriptions = []
        ship_weapon_types = sorted(
            set(
                item_data.get("Type", "")
                for item_data in self.game_data.ship_weapon.values()
            )
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
            combo.bind(
                "<<ComboboxSelected>>",
                lambda e, idx=i: self._update_cargo_description(idx),
            )
            self.cargo_combos.append(combo)
            description_label = ttk.Label(cargo_frame, text="", wraplength=400)
            description_label.pack(fill=tk.X, padx=5, pady=2)
            self.cargo_descriptions.append(description_label)
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

        # Modules Frame
        modules_frame = ttk.LabelFrame(scrollable_frame, text="Modules")
        modules_frame.pack(fill=tk.X, pady=5)
        self.module_combos = []
        self.module_descriptions = []

        if not self.save_manager.modules:
            ttk.Label(
                modules_frame,
                text="No modules available. Please add modules ingame first.",
                foreground="red",
            ).pack(pady=10)
        else:
            sorted_slots = sorted(self.save_manager.modules.keys())
            for slot_number in sorted_slots:
                module_data = self.save_manager.modules[slot_number]
                row = ttk.Frame(modules_frame)
                row.pack(fill=tk.X, padx=5, pady=2)
                ttk.Label(row, text=f"Slot {slot_number}:").pack(side=tk.LEFT)
                combo = ttk.Combobox(row, width=25, state="readonly")
                combo["values"] = [
                    module.get("Name", "")
                    for module in self.game_data.ship_module.values()
                    if module.get("Name", "")
                ]
                combo.set(module_data.get("obj", ""))
                combo.pack(side=tk.LEFT, padx=5)
                combo.bind(
                    "<<ComboboxSelected>>",
                    lambda e, idx=slot_number: self._update_module_description(idx),
                )
                self.module_combos.append(combo)
                description_label = ttk.Label(modules_frame, text="", wraplength=400)
                description_label.pack(fill=tk.X, padx=5, pady=2)
                self.module_descriptions.append(description_label)
                select_btn = ttk.Button(
                    row,
                    text="List",
                    command=partial(self._open_module_table, slot_number),
                    width=10,
                )
                select_btn.pack(side=tk.LEFT, padx=2)

        # If no modules exist, disable all widgets inside the frame
        if not self.save_manager.modules:
            for child in modules_frame.winfo_children():
                child.configure(state=tk.DISABLED)

        # Save Button
        save_button = ttk.Button(
            scrollable_frame, text="Save Changes", command=self._save_changes
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
            description = self.game_data.item_id_description_map.get(
                str(item_id), "Item has no description"
            )
            self.equipment_descriptions[i].config(text=description)
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
            description = self.game_data.item_id_description_map.get(
                str(item_id), "Item has no description"
            )
            self.cargo_descriptions[i].config(text=description)

        # Modules
        if self.save_manager.modules:
            module_list = self.save_manager.get_module_list()
            for i, combo in enumerate(self.module_combos):
                item_id = module_list[i] if i < len(module_list) else -1.0
                item_name = self.game_data.item_id_name_map.get(
                    str(item_id), "Empty Slot"
                )
                combo.set(item_name)
                description = self.game_data.item_id_description_map.get(
                    str(item_id), "Item has no description"
                )
                self.module_descriptions[i].config(text=description)

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

            # Modules
            new_modules = self._get_module_data()
            self.save_manager.set_module_list(new_modules)

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

    def _get_module_data(self):
        """
        Retrieve module data from UI.
        Returns:
            list: module_list
        """
        module_list = []
        for combo in self.module_combos:
            name = combo.get()
            item_id = (
                self.game_data.item_name_id_map.get(name, -1.0)
                if name != "Empty Slot"
                else -1.0
            )
            module_list.append(item_id)
        return module_list

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
        win.geometry("800x400")
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
                self.equipment_descriptions[slot_idx].config(
                    text="Item has no description"
                )
            else:
                name = cat_dict[item_id].get("Name", "")
                description = cat_dict[item_id].get(
                    "Description", "Item has no description"
                )
                self.equipment_combos[slot_idx].set(name)
                self.equipment_descriptions[slot_idx].config(text=description)
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
        win.geometry("800x400")
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
                self.cargo_descriptions[slot_idx].config(text="Item has no description")
            else:
                name = filtered_items[item_id].get("Name", "")
                description = filtered_items[item_id].get(
                    "Description", "Item has no description"
                )
                self.cargo_combos[slot_idx].set(name)
                self.cargo_descriptions[slot_idx].config(text=description)
            win.destroy()

        select_btn = ttk.Button(win, text="Select", command=select_item)
        select_btn.pack(pady=5)

        def on_double_click(event):
            select_item()

        tree.bind("<Double-1>", on_double_click)

    def _open_module_table(self, slot_idx):
        """
        Open a table window for selecting a module for a given slot.
        Fix: Ensure the correct slot index is used to update the combo box and save data.
        """
        filtered_items = self.game_data.ship_module
        columns = []
        if filtered_items:
            first_item = next(iter(filtered_items.values()))
            columns = [k for k in first_item.keys()]
            if "Name" not in columns:
                columns.insert(0, "Name")
            if "Description" not in columns and "Description" in first_item:
                columns.append("Description")
        else:
            columns = ["Name"]

        win = tk.Toplevel(self)
        win.title(f"Select Module for Slot {slot_idx}")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        # Insert items
        for item_id, data in filtered_items.items():
            values = [data.get(col, "") for col in columns]
            tree.insert("", "end", values=values, iid=item_id)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def select_item():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Module", "Please select a module.")
                return
            item_id = selected[0]
            # Correctly update the combo box and save data for the selected slot
            name = filtered_items[item_id].get("Name", "")
            description = filtered_items[item_id].get(
                "Description", "Item has no description"
            )
            self.module_combos[slot_idx].set(name)
            self.module_descriptions[slot_idx].config(text=description)
            self.save_manager.set_module_slot(slot_idx, item_id)  # Update save data
            win.destroy()

        select_btn = ttk.Button(win, text="Select", command=select_item)
        select_btn.pack(pady=5)

        def on_double_click(event):
            select_item()

        tree.bind("<Double-1>", on_double_click)

    def _update_equipment_description(self, idx):
        """
        Update the description label for the selected equipment slot.
        """
        item_name = self.equipment_combos[idx].get()
        if item_name == "Empty Slot":
            self.equipment_descriptions[idx].config(text="")
        else:
            item_id = self.game_data.item_name_id_map.get(item_name, "-1.0")
            description = self.game_data.item_id_description_map.get(
                item_id, "Item has no description"
            )
            self.equipment_descriptions[idx].config(text=description)

    def _update_cargo_description(self, idx):
        """
        Update the description label for the selected cargo slot.
        """
        item_name = self.cargo_combos[idx].get()
        if item_name == "Empty Slot":
            self.cargo_descriptions[idx].config(text="")
        else:
            item_id = next(
                (
                    k
                    for k, v in self.game_data.ship_weapon.items()
                    if v.get("Name") == item_name
                ),
                "-1.0",
            )
            description = self.game_data.item_id_description_map.get(
                item_id, "Item has no description"
            )
            self.cargo_descriptions[idx].config(text=description)
        """
        Update the description label for the selected equipment slot.
        """
        item_name = self.equipment_combos[idx].get()
        if item_name == "Empty Slot":
            self.equipment_descriptions[idx].config(text="")
        else:
            item_id = self.game_data.item_name_id_map.get(item_name, "-1.0")
            description = self.game_data.item_id_description_map.get(
                item_id, "Item has no description"
            )
            self.equipment_descriptions[idx].config(text=description)

    def _update_cargo_description(self, idx):
        """
        Update the description label for the selected cargo slot.
        """
        item_name = self.cargo_combos[idx].get()
        if item_name == "Empty Slot":
            self.cargo_descriptions[idx].config(text="")
        else:
            item_id = next(
                (
                    k
                    for k, v in self.game_data.ship_weapon.items()
                    if v.get("Name") == item_name
                ),
                "-1.0",
            )
            description = self.game_data.item_id_description_map.get(
                item_id, "Item has no description"
            )
            self.cargo_descriptions[idx].config(text=description)

    def _update_module_description(self, idx):
        """
        Update the description label for the selected module slot.
        """
        item_name = self.module_combos[idx].get()
        item_id = next(
            (
                k
                for k, v in self.game_data.ship_module.items()
                if v.get("Name") == item_name
            ),
            "-1.0",
        )
        description = self.game_data.item_id_description_map.get(
            item_id, "Item has no description"
        )
        self.module_descriptions[idx].config(text=description)
        description = self.game_data.item_id_description_map.get(
            item_id, "Item has no description"
        )
        self.module_descriptions[idx].config(text=description)
