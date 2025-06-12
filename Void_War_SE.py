import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re

class VoidWarSaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Void War Save Editor")
        self.root.minsize(600, 800)  # Increased height for new modules section
        
        # Weapon mapping dictionary
        self.weapon_map = dict(sorted({
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
            3335.0: "Thunder Cannon II",
            2425.0: "Hull Ripper I",
            4184.0: "Hull Ripper II",
            4185.0: "Heat Beam I",
            3350.0: "Graviton Cannon",
            3635.0: "Heat Beam",
            4051.0: "Flayer Beam",
            3019.0: "Grave Beam",
            3320.0: "Retributor I",
            3324.0: "Retributor II",
            3325.0: "Retributor III",
            3329.0: "Flame Lance",
            1458.0: "Magnetic Pulse I",
            3339.0: "Magnetic Pulse II",
            3355.0: "Macro Disruptor",
            3361.0: "Kinetic Lance",
            3356.0: "Energy Lance",
            3357.0: "Heavy Lance",
            3358.0: "Macro Lance",
            3053.0: "Auto-Disruptor",
            3334.0: "Storm Cannon I",
            3336.0: "Storm Cannon II",
            3340.0: "Storm Cannon III",
            3341.0: "Storm Cannon Array",
            3914.0: "Fusilade I",
            3388.0: "Fusilade II",
            4158.0: "Displacement Field Emitter",
            3068.0: "Penetrator",
            3342.0: "Radium Blaster I",
            3343.0: "Radium Blaster II",
            3345.0: "Radium Blaster III",
            3989.0: "Fury Missile",
            3337.0: "Titan Multicannon",
            3347.0: "Putrefactor I",
            3348.0: "Putrefactor II",
            3349.0: "Toxin Carronade",
            3352.0: "Disruptor",
            3353.0: "Twin Disruptor",
            3354.0: "Heavy Disruptor",
            3338.0: "Plasma Battery",
            3361.0: "Kinetic Lance",
            3364.0: "Thermal Lance",
            3365.0: "Heavy Ion Lance",
            3366.0: "Plasma Lance",
            3370.0: "Gravitic Lance",
            3375.0: "Gravitic Lance",
            3376.0: "Spirit Lance",
            3378.0: "Neural Lance",
            3381.0: "Warp Lance",
            3382.0: "Nemesis Lance",
            3383.0: "Void Mass Driver",
            3384.0: "Warpflame Lance",
            3386.0: "Magnetic Pulse I",
            3389.0: "Magnetic Pulse II",
            3390.0: "Magnetic Pulse III",
            3394.0: "Shiv Missile",
            3398.0: "Acid Missile",
            3399.0: "Graviton Bomb",
            3404.0: "Heavy Flayer Missile",
            3330.0: "Bolt Cannon",
            3332.0: "Bastard Artillery",
            3333.0: "Graviton Imperator",
            4000.0: "Energy Beam II",
            3044.0: "Neuralizer",
            3849.0: "Gravitic Ray",
            3148.0: "Siege Missile"
        }.items()))
        
        # Equipment mapping dictionary
        self.equipment_map = dict(sorted({
            -1.0: "Empty Slot",
            846.0: "Holy Scepter",
            867.0: "Blood Curse",
            1393.0: "Fusion Charge",
            2426.0: "Purify",
            2463.0: "Combat Shield",
            2555.0: "Soul Storm",
            2607.0: "Stygian Reagent",
            2612.0: "Riot Shield",
            2615.0: "Hull Integrity Patch",
            2628.0: "Assault Drill",
            2630.0: "Beam Carbine",
            2635.0: "Siege Armor",
            2641.0: "Fetid Rags",
            2642.0: "Fireball",
            2645.0: "Force Shield",
            2648.0: "HellFire Blade",
            2656.0: "Plague Sword",
            2657.0: "Electro Maul",
            2660.0: "Power Field",
            2662.0: "Power Hammer",
            2663.0: "Pressure Suit",
            2672.0: "Assault Sledge",
            2674.0: "Decapitator",
            2675.0: "Tactical Armor",
            2679.0: "Welding Torch",
            2686.0: "Repair Drone",
            2854.0: "Psychic Shriek",
            2885.0: "Soul Spear",
            2961.0: "Blessed Hammer",
            3084.0: "Soul Barrage",
            3089.0: "Imperial Aegis",
            3091.0: "Fear",
            3099.0: "Rejuvenate",
            3132.0: "Power Claw",
            3158.0: "Heavy Translocator",
            3171.0: "Fleshy Reagents",
            3199.0: "Cursed Spear",
            3363.0: "Power Axe",
            3438.0: "Tactical Shield",
            3446.0: "Spiked Club",
            3449.0: "Fiendish Reagents",
            3511.0: "Antidote",
            3525.0: "Duraplate Armor",
            3534.0: "Drain Strength",
            3540.0: "Assault Shield",
            3574.0: "Plasma Projector",
            3584.0: "Summon Fleshlings",
            3661.0: "Noxious Blast",
            3649.0: "Power Sword",
            3659.0: "Doom Reagents",
            3716.0: "Blood Spear",
            3718.0: "Med Drone",
            3776.0: "Goreblaster",
            3808.0: "Power Glaive",
            3872.0: "Evisorator",
            3878.0: "Grav Spear",
            3911.0: "Siege Axe",
            3954.0: "Chaos Engine",
            3959.0: "Blessed Blade",
            3997.0: "Ruinous Reagent",
            4029.0: "Parasite Shield",
            4085.0: "Dark Matter Prism",
            4124.0: "Athame",
            4141.0: "Machine Cannon",
            4164.0: "Rotblaster",
            4187.0: "Unholy Talisman",
            4195.0: "Ballistic Shield",
            4221.0: "Assault Pistol",
            4280.0: "Mind Bolt",
            4312.0: "Machine Pistol",
            4407.0: "Howling Reagent",
            4410.0: "Tactical Exoskeleton",
            4426.0: "Necrotizing Reagents",
            4445.0: "Treasonous Whispers",
            4464.0: "Combat Knife",
            4480.0: "Heavy Duraplate Armor",
            4482.0: "Summon Hound",
            4501.0: "Aetheric Gate",
            4528.0: "Arc Talons",
            4541.0: "Ripper Fist",
            4550.0: "Grenade Launcher",
            4610.0: "Microshield",
            4625.0: "Burden",
            4645.0: "Zenith Blade",
            4659.0: "Chaotic Rift",
            4692.0: "Cryofoam"
        }.items()))
        
        # Module mapping dictionary
        self.module_map = {
            "oModule_preChargedWeapons": "Night Field: Begin fights with fully pre-charged weapons.",
            "oModule_huskRepairSpeed": "Support Prosthetics: Friendly Machine Slave units repair 50% faster.",
            "oModule_commander_speed": "Hyperlinked Neural Socket: +50% move speed to commander.",
            "oModule_firstWeaponDoubleShots": "Mirrored Fire Control: The first time your ship fires a non-beam weapon, that weapon's shot count is doubled.",
            "oModule_consumablesFireProjectiles": "Seeker Missiles: Friendly crew fire a missile at the enemy ship upon activating a consumable.",
            "oModule_shotsBreakDoors": "Demolisher Rounds: Your ship's weapons that deal hull damage now break doors on impact.",
            "oModule_systemHalvesFireDamage": "Heat Shielding: Systems and subsystems take half damage from fire.",
            "oModule_spellEvasion": "Spectral Drives: Your ship can now dodge spells using its evasion attribute.",
            "oModule_HP_technoLow": "Hardened Casing: +10 HP to all Machine Slave Units.",
            "oModule_HP_techno": "Guardian Protocols: +10 HP to all Machine Priest units.",
            "oModule_HP_death": "Pathogenic Recycler Unit: +10 HP to all Death Cultist units.",
            "oModule_HP_demon": "Desecrated Shrine: +10 HP to all Demonic units.",
            "oModule_HP_raider": "Adaptive Nanoplate: +10 HP to all Raider Outlaw units.",
            "oModule_HP_war": "Synaptic Enforcers: +10 HP to all War Cultist units.",
            "oModule_HP_empire": "Meditech Boosters: +10 HP to all Imperial Citizen units.",
            "oModule_doorBreakInvulnerable": "Bunker Drills: Your crew are invulnerable against crew attacks while breaking doors.",
            "oModule_forceShieldOnWeaponShot": "Barrier Relay: For every other weapon you fire, gain a force shield on a random room: up to a maximum of 2.",
            "oModule_rewardExtraCrystal": "Thrice-cursed Reliquary: Frequently gain a Dark Matter Prism: in addition to normal rewards after defeating an enemy ship.",
            "oModule_poisonSlowsRepair": "Corpse Effigy: Halves the repair speed of poisoned enemies.",
            "oModule_doorBreakStun": "Assault Harnesses: Your crew will stun nearby enemy crew for 8s upon destroying a door.",
            "oModule_sensorVisionGainEvasion": "Vector Analyzer: Gain 10% Evasion while your Sensor Status is Active.",
            "oModule_sensorVisionGainCrewDamage": "Carnage Optics: Your ship's weapons deal +10 crew damage to enemies while your Sensor Status is Active.",
            "oModule_crewExplodeOnDeath": "Terminus Bands: All friendly crew explode on death dealing 10 damage to nearby enemy crew.",
            "oModule_fightStartDamageEnemies": "Ancient Psytronome: Applies 5-22 damage to all enemy crew at the start of every fight.",
            "oModule_DPS_technoLow": "Combat Subroutines: +2 DPS to all Machine Slave units.",
            "oModule_DPS_techno": "Ocular-Laser Implants: +2 DPS to all Machine Priest units.",
            "oModule_DPS_empire": "Standard-Issue Sidearm: +2 DPS to all Imperial Citizen units.",
            "oModule_DPS_commanderFightStart": "Tower of Skulls: Commander gains +10 DPS for 30 seconds at the start of every fight.",
            "oModule_DPS_war": "Psyk-Chem Injectors: +2 DPS to all War Cultist units.",
            "oModule_DPS_death": "Death Totem: +2 DPS to all Death Cultists units.",
            "oModule_DPS_raider": "Volt Knives: +2 DPS to all Raider Outlaw units.",
            "oModule_DPS_demon": "Aberrant Conduit: +2 DPS to all Demonic units.",
            "oModule_DPS_blood": "Altar of Blood: +2 DPS to all Blood Cultist units.",
            "oModule_repairAppliesCleanse": "Purity of Steel: Upon repairing a system, friendly crew gain immunity to debilitating effects for 10 seconds.",
            "oModule_bonusCrewThrallSkeleRot": "Chaos Star: Calls upon the dark gods in times of need.",
            "oModule_firstEnemyShotMisses": "Distortion Sphere: First enemy ship weapon fired at your ship will always miss.",
            "oModule_rewardExtraChoice": "God-King's Mantle: Select from three rewards instead of two when choosing rewards.",
            "oModule_poisonDoubleDamage": "Sigil of Rot: Poison does double damage to enemy crew.",
            "oModule_lanceChargesRandomWeapon": "Seraphic Resonators: Each lance shot you fire fully charges one random, uncharged weapon: must be powered.",
            "oModule_restHealBonus": "Circadian Stabilizer: Resting heals 15% extra HP.",
            "oModule_DPS_inVacuum": "Splinter Bombs: Friendly crew gain +3 DPS when fighting in vacuum.",
            "oModule_lancesAlwaysHit": "Wrath of Angels: Your lances always hit.",
            "oModule_doorBreakAfterBoarding": "Shatterfields: Your crew gain 1000% door break speed for 10s when boarding an enemy ship for the first time during a fight using a launch bay.",
            "oModule_launchBayEatsEnemies": "Carnivore Hatch: Launch Bays can load enemy crew. Prioritizes enemy crew and deals 140 damage to them while loading. Triggers 30s cooldown after use.",
            "oModule_consumablesGrantHP": "Bio-Regenerator: Consumables restore 10 HP in addition to their normal effect.",
            "oModule_bonusCrewHound": "Seal of Cerberus: Call upon a demonic Hound."
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
        
        # Resources Section - Combines Scrap and Missiles
        self.resources_frame = tk.LabelFrame(self.scrollable_frame, text="Resources", padx=5, pady=5)
        self.resources_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Scrap Row
        scrap_row = tk.Frame(self.resources_frame)
        scrap_row.pack(fill=tk.X, padx=5, pady=2)
        
        scrap_label = tk.Label(scrap_row, text="Scrap:")
        scrap_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.scrap_entry = tk.Entry(scrap_row, width=15)
        self.scrap_entry.pack(side=tk.LEFT, padx=5)
        
        # Missile Row
        missile_row = tk.Frame(self.resources_frame)
        missile_row.pack(fill=tk.X, padx=5, pady=2)
        
        missile_label = tk.Label(missile_row, text="Missiles:")
        missile_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.missile_entry = tk.Entry(missile_row, width=15)
        self.missile_entry.pack(side=tk.LEFT, padx=5)
        
        # Cargo Section
        self.cargo_frame = tk.LabelFrame(self.scrollable_frame, text="Cargo Slots (4 slots)", padx=5, pady=5)
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
        self.equipment_frame = tk.LabelFrame(self.scrollable_frame, text="Equipment Slots (8 slots)", padx=5, pady=5)
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
            
        # Ship Modules Section
        self.modules_frame = tk.LabelFrame(self.scrollable_frame, text="Ship Modules (3 slots)", padx=5, pady=5)
        self.modules_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.module_labels = []
        self.module_combos = []
        self.module_slot_present = [False, False, False]  # Track which slots exist
        
        for i in range(3):
            slot_frame = tk.Frame(self.modules_frame)
            slot_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = tk.Label(slot_frame, text=f"Slot {i+1}:", width=8, anchor="w")
            label.pack(side=tk.LEFT, padx=(5, 0))
            
            combo = ttk.Combobox(slot_frame, width=25, state="normal")
            module_names = sorted([name for name in self.module_map.values()])
            combo['values'] = ["Empty Slot"] + module_names
            combo.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
            
            self.module_labels.append(label)
            self.module_combos.append(combo)
        
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
            
            # Find ship modules
            self.module_slot_present = [False, False, False]  # Reset presence flags
            
            # Check for each module slot (0.0, 1.0, 2.0)
            for slot_index in range(3):
                # Look for the module slot pattern
                pattern = rf'"moduleSlot":{slot_index}\.0.*?"obj":"([^"]+)"'
                match = re.search(pattern, self.save_data)
                
                if match:
                    module_obj = match.group(1)
                    self.module_slot_present[slot_index] = True
                    
                    # Convert obj to display name if available
                    if module_obj in self.module_map:
                        display_name = self.module_map[module_obj]
                    else:
                        display_name = module_obj
                    
                    self.module_combos[slot_index].set(display_name)
                    self.module_combos[slot_index].config(state="readonly")
                else:
                    # Slot not found, disable and clear
                    self.module_combos[slot_index].set("")
                    self.module_combos[slot_index].config(state="disabled")
            
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
            
            # Process module changes
            updated_data = self.save_data
            for slot_index in range(3):
                if self.module_slot_present[slot_index]:
                    display_name = self.module_combos[slot_index].get().strip()
                    
                    # Skip if nothing selected
                    if not display_name:
                        continue
                    
                    # Convert display name back to object name if available
                    if display_name in self.module_map.values():
                        # Find the object name for this display name
                        obj_name = None
                        for obj, name in self.module_map.items():
                            if name == display_name:
                                obj_name = obj
                                break
                    else:
                        obj_name = display_name
                    
                    if obj_name:
                        # Create pattern to find the existing module entry
                        pattern = rf'("moduleSlot":{slot_index}\.0[^,]*,"obj":")[^"]+(")'
                        
                        # Replace with new object name
                        updated_data = re.sub(
                            pattern,
                            rf'\g<1>{obj_name}\g<2>',
                            updated_data
                        )
            
            # Create backup
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)
            os.rename(self.current_file_path, self.backup_path)
            
            # Update scrap value
            updated_data = re.sub(
                r'("currScrap":)(\d+\.?\d*)',
                f'\\g<1>{new_scrap}',
                updated_data
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
            
            # Module summary
            module_summary = []
            for i in range(3):
                if self.module_slot_present[i]:
                    module_summary.append(f"Slot {i+1}: {self.module_combos[i].get()}")
            
            messagebox.showinfo("Success", 
                f"Save file updated successfully!\n\n"
                f"Scrap: {new_scrap}\n"
                f"Missiles: {new_missile}\n\n"
                f"Cargo Summary:\n{cargo_summary}\n\n"
                f"Equipment Summary:\n{equipment_summary}\n\n"
                f"Module Summary:\n" + "\n".join(module_summary) + "\n\n"
                f"Backup created: {os.path.basename(self.backup_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes:\n{str(e)}")
            self.status.config(text="Save failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoidWarSaveEditor(root)
    root.mainloop()