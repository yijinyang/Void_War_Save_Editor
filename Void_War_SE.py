import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re

class VoidWarSaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Void War Save Editor")
        self.root.minsize(600, 700)
        
        # Weapon mapping dictionary
        self.weapon_map = {
            -1.0: "Empty Slot",
            3719.0: "Displacement Missile",
            3380.0: "Sabre Missile",
            3408.0: "Blight Bomb",
            3889.0: "Flayer Missile",
            3431.0: "Rift Bomb",
            3427.0: "Heavy Disruptor Missile",
            3409.0: "Claymore Missile",
            3395.0: "Antimatter Bomb",
            2770.0: "Thunder Cannon",
            2425.0: "Hull Ripper I",
            4184.0: "Hull Ripper II",
            3350.0: "Graviton Cannon",
            3635.0: "Heat Beam",
            4051.0: "Flayer Beam",
            3019.0: "Grave Beam",
            3324.0: "Retributor II",
            1458.0: "Magnetic Pulse I",
            3355.0: "Macro Disruptor",
            3361.0: "Kinetic Lance",
            3356.0: "Energy Lance",
            3358.0: "Macro Lance",
            3053.0: "Auto-Disruptor",
            3334.0: "Storm Cannon I",
            3340.0: "Storm Cannon III",
            3914.0: "Fusilade I",
            3388.0: "Fusilade II"
        }
        
        # Equipment mapping dictionary
        self.equipment_map = {
            -1.0: "Empty Slot",
            2675.0: "Tactical Armor",
            3525.0: "Duraplate Armor",
            4480.0: "Heavy Duraplate Armor",
            2663.0: "Pressure Suit",
            4410.0: "Tactical Exoskeleton",
            4085.0: "Dark Matter Prism",
            4610.0: "Microshield",
            2615.0: "Hull Integrity Patch",
            3511.0: "Antidote",
            3718.0: "Med Drone",
            1393.0: "Fusion Charge",
            2686.0: "Repair Drone",
            4692.0: "Cryofoam",
            3954.0: "Chaos Engine",
            2607.0: "Stygian Reagent",
            4407.0: "Howling Reagent",
            3997.0: "Ruinous Reagent",
            2463.0: "Combat Shield",
            4141.0: "Machine Cannon",
            3649.0: "Power Sword",
            4645.0: "Zenith Blade",
            4541.0: "Ripper Fist",
            3199.0: "Cursed Spear",
            2674.0: "Decapitator",
            2656.0: "Plague Sword",
            3872.0: "Evisorator",
            3776.0: "GoreBlaster",
            2648.0: "HellFire Blade",
            867.0: "BloodCurse"
        }
        
        # Default save location
        self.default_dir = os.path.join(os.getenv('APPDATA'), 'Void_War')
        self.save_data = None
        
        # Create main frame with scrollbar
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Scrap Section
        self.scrap_frame = tk.LabelFrame(self.scrollable_frame, text="Scrap Resources", padx=5, pady=5)
        self.scrap_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.scrap_label = tk.Label(self.scrap_frame, text="Current Scrap:")
        self.scrap_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        
        self.scrap_entry = tk.Entry(self.scrap_frame, width=15)
        self.scrap_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Missile Section
        self.missile_frame = tk.LabelFrame(self.scrollable_frame, text="Current Missiles:", padx=5, pady=5)
        self.missile_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.missile_label = tk.Label(self.missile_frame, text="Missile Count:")
        self.missile_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        
        self.missile_entry = tk.Entry(self.missile_frame, width=15)
        self.missile_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Cargo Section
        self.cargo_frame = tk.LabelFrame(self.scrollable_frame, text="Cargo Slots", padx=5, pady=5)
        self.cargo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.cargo_labels = []
        self.cargo_combos = []
        
        for i in range(4):
            slot_frame = tk.Frame(self.cargo_frame)
            slot_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = tk.Label(slot_frame, text=f"Slot {i+1}:", width=8, anchor="w")
            label.pack(side=tk.LEFT, padx=(5, 0))
            
            combo = ttk.Combobox(slot_frame, width=25, state="normal")
            weapon_names = sorted([name for name in self.weapon_map.values() if name != "Empty Slot"])
            combo['values'] = ["Empty Slot"] + weapon_names
            combo.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
            
            self.cargo_labels.append(label)
            self.cargo_combos.append(combo)
        
        # Equipment Section
        self.equipment_frame = tk.LabelFrame(self.scrollable_frame, text="Equipment Slots", padx=5, pady=5)
        self.equipment_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.equipment_labels = []
        self.equipment_combos = []
        self.quantity_entries = []
        
        for i in range(8):
            slot_frame = tk.Frame(self.equipment_frame)
            slot_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = tk.Label(slot_frame, text=f"Slot {i+1}:", width=8, anchor="w")
            label.pack(side=tk.LEFT, padx=(5, 0))
            
            # Equipment type combo
            combo = ttk.Combobox(slot_frame, width=25, state="normal")
            equipment_names = sorted([name for name in self.equipment_map.values() if name != "Empty Slot"])
            combo['values'] = ["Empty Slot"] + equipment_names
            combo.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
            
            # Quantity entry
            qty_label = tk.Label(slot_frame, text="Qty:")
            qty_label.pack(side=tk.LEFT, padx=(10, 0))
            
            qty_entry = tk.Entry(slot_frame, width=8)
            qty_entry.pack(side=tk.LEFT, padx=(0, 5))
            
            self.equipment_labels.append(label)
            self.equipment_combos.append(combo)
            self.quantity_entries.append(qty_entry)
        
        # Button Section
        self.btn_frame = tk.Frame(self.scrollable_frame)
        self.btn_frame.pack(fill=tk.X, pady=10)
        
        self.load_btn = tk.Button(self.btn_frame, text="Load Savegame", command=self.load_save)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.save_btn = tk.Button(self.btn_frame, text="Save Changes", command=self.save_changes, state="disabled")
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status Bar
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_save(self):
        try:
            # Set initial directory if it exists
            initial_dir = self.default_dir if os.path.exists(self.default_dir) else os.getenv('APPDATA')
            
            # Open file browser
            file_path = filedialog.askopenfilename(
                title="Select Void War Save File",
                initialdir=initial_dir,
                filetypes=(("Save files", "*.sav"), ("All files", "*.*"))
            )
            
            if not file_path:  # User canceled
                return
                
            with open(file_path, 'r') as f:
                self.save_data = f.read()
                self.current_file_path = file_path
                self.backup_path = file_path + ".bak"
            
            # Find scrap value
            scrap_match = re.search(r'"currScrap":(\d+\.?\d*)', self.save_data)
            missile_match = re.search(r'"playerMissileCt":(\d+\.?\d*)', self.save_data)
            
            if scrap_match:
                scrap_value = scrap_match.group(1)
                self.scrap_entry.delete(0, tk.END)
                self.scrap_entry.insert(0, scrap_value)
            else:
                raise ValueError("Scrap value not found in save file")
                
            if missile_match:
                missile_value = missile_match.group(1)
                self.missile_entry.delete(0, tk.END)
                self.missile_entry.insert(0, missile_value)
            else:
                raise ValueError("Missile count not found in save file")
            
            # Find cargo list
            cargo_match = re.search(r'"cargoList":\[([^\]]+)\]', self.save_data)
            if cargo_match:
                cargo_str = cargo_match.group(1)
                cargo_values = [float(x.strip()) for x in cargo_str.split(',')]
                
                if len(cargo_values) < 4:
                    cargo_values += [-1.0] * (4 - len(cargo_values))
                
                for i, value in enumerate(cargo_values[:4]):
                    if value in self.weapon_map:
                        display_value = self.weapon_map[value]
                    else:
                        display_value = str(value)
                    self.cargo_combos[i].set(display_value)
            else:
                for i in range(4):
                    self.cargo_combos[i].set("Empty Slot")
                self.status.config(text="Cargo list not found - initialized with empty slots")
            
            # Find equipment list and quantities
            equipment_list_match = re.search(r'"equipmentList":\[([^\]]+)\]', self.save_data)
            equipment_qt_match = re.search(r'"equipmentQt":\[([^\]]+)\]', self.save_data)
            
            if equipment_list_match and equipment_qt_match:
                equipment_str = equipment_list_match.group(1)
                qt_str = equipment_qt_match.group(1)
                
                equipment_values = [float(x.strip()) for x in equipment_str.split(',')]
                qt_values = [float(x.strip()) for x in qt_str.split(',')]
                
                # Pad arrays if needed
                if len(equipment_values) < 8:
                    equipment_values += [-1.0] * (8 - len(equipment_values))
                if len(qt_values) < 8:
                    qt_values += [0.0] * (8 - len(qt_values))
                
                for i, (eq_val, qt_val) in enumerate(zip(equipment_values[:8], qt_values[:8])):
                    # Set equipment type
                    if eq_val in self.equipment_map:
                        display_value = self.equipment_map[eq_val]
                    else:
                        display_value = str(eq_val)
                    self.equipment_combos[i].set(display_value)
                    
                    # Set quantity
                    self.quantity_entries[i].delete(0, tk.END)
                    self.quantity_entries[i].insert(0, str(qt_val))
            else:
                for i in range(8):
                    self.equipment_combos[i].set("Empty Slot")
                    self.quantity_entries[i].delete(0, tk.END)
                    self.quantity_entries[i].insert(0, "0.0")
                self.status.config(text="Equipment lists not found - initialized with empty slots")
            
            self.save_btn.config(state="normal")
            self.status.config(text=f"Loaded: {os.path.basename(file_path)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save:\n{str(e)}")
            self.status.config(text="Load failed")

    def save_changes(self):
        try:
            # Validate inputs
            new_scrap = self.scrap_entry.get().strip()
            new_missile = self.missile_entry.get().strip()
            
            if not re.match(r'^\d+(\.\d*)?$', new_scrap):
                raise ValueError("Invalid scrap value. Must be a number")
            
            if not re.match(r'^\d+(\.\d*)?$', new_missile):
                raise ValueError("Invalid missile count. Must be a number")
            
            # Process cargo values
            cargo_values = []
            for i, combo in enumerate(self.cargo_combos):
                value = combo.get().strip()
                
                # Check if it's a weapon name
                if value in self.weapon_map.values():
                    for num, name in self.weapon_map.items():
                        if name == value:
                            cargo_values.append(num)
                            break
                # Check if it's "Empty Slot"
                elif value == "Empty Slot":
                    cargo_values.append(-1.0)
                # Try to parse as float
                else:
                    try:
                        num_value = float(value)
                        cargo_values.append(num_value)
                    except ValueError:
                        raise ValueError(f"Invalid value in cargo slot {i+1}: '{value}'. Must be a weapon name or number")
            
            # Process equipment values and quantities
            equipment_values = []
            quantity_values = []
            
            for i, (combo, qty_entry) in enumerate(zip(self.equipment_combos, self.quantity_entries)):
                eq_value = combo.get().strip()
                qty_value = qty_entry.get().strip()
                
                # Validate quantity
                if not re.match(r'^\d+(\.\d*)?$', qty_value):
                    raise ValueError(f"Invalid quantity in equipment slot {i+1}. Must be a number")
                
                # Convert to float
                qty_float = float(qty_value)
                
                # Process equipment type
                if eq_value == "Empty Slot":
                    equipment_values.append(-1.0)
                    # Force quantity to 0 for empty slots
                    quantity_values.append(0.0)
                elif eq_value in self.equipment_map.values():
                    found = False
                    for num, name in self.equipment_map.items():
                        if name == eq_value:
                            equipment_values.append(num)
                            quantity_values.append(qty_float)
                            found = True
                            break
                    if not found:
                        # Shouldn't happen, but handle just in case
                        equipment_values.append(-1.0)
                        quantity_values.append(0.0)
                else:
                    try:
                        eq_float = float(eq_value)
                        equipment_values.append(eq_float)
                        quantity_values.append(qty_float)
                    except ValueError:
                        raise ValueError(f"Invalid value in equipment slot {i+1}: '{eq_value}'. Must be an equipment name or number")
            
            # Create backup
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)
            os.rename(self.current_file_path, self.backup_path)
            
            # Update scrap value
            updated_data = re.sub(
                r'("currScrap":)(\d+\.?\d*)',
                f'\\g<1>{new_scrap}',
                self.save_data
            )
            
            # Update missile count
            updated_data = re.sub(
                r'("playerMissileCt":)(\d+\.?\d*)',
                f'\\g<1>{new_missile}',
                updated_data
            )
            
            # Update cargo list
            cargo_str = ",".join([str(v) for v in cargo_values])
            updated_data = re.sub(
                r'("cargoList":)(\[[^\]]+\])',
                f'\\g<1>[{cargo_str}]',
                updated_data
            )
            
            # Update equipment list
            equipment_str = ",".join([str(v) for v in equipment_values])
            updated_data = re.sub(
                r'("equipmentList":)(\[[^\]]+\])',
                f'\\g<1>[{equipment_str}]',
                updated_data
            )
            
            # Update equipment quantities
            quantity_str = ",".join([str(v) for v in quantity_values])
            updated_data = re.sub(
                r'("equipmentQt":)(\[[^\]]+\])',
                f'\\g<1>[{quantity_str}]',
                updated_data
            )
            
            # Save changes
            with open(self.current_file_path, 'w') as f:
                f.write(updated_data)
            
            # Update status and show success message
            self.status.config(text=f"Saved: {os.path.basename(self.current_file_path)}")
            
            # Show summary
            cargo_summary = "\n".join([f"Slot {i+1}: {self.cargo_combos[i].get()}" for i in range(4)])
            equipment_summary = "\n".join(
                [f"Slot {i+1}: {self.equipment_combos[i].get()} x{self.quantity_entries[i].get()}" 
                 for i in range(8)]
            )
            
            messagebox.showinfo("Success", 
                f"Save file updated successfully!\n\n"
                f"Scrap: {new_scrap}\n"
                f"Missiles: {new_missile}\n\n"
                f"Cargo Summary:\n{cargo_summary}\n\n"
                f"Equipment Summary:\n{equipment_summary}\n\n"
                f"Backup created: {os.path.basename(self.backup_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes:\n{str(e)}")
            self.status.config(text="Save failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoidWarSaveEditor(root)
    root.mainloop()