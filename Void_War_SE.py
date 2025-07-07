import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re

class VoidWarSaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Void War Save Editor")
        self.root.minsize(600, 800)
        
        # Weapon mapping dictionary with string keys
        self.weapon_map = {
            -1.0: "Empty Slot",
            "oWPDisruptor2": "Twin Disruptor",
            "oWPBlessedCannon1": "Retributor I",
            "oWPBlessedCannon2": "Retributor II",
            "oWPBlessedCannon3": "Retributor III",
            "oWPCannon1": "Bolt Cannon",
            "oWPCannon1x2": "Thunder Cannon",
            "oWPCannon2x2": "Thunder Cannon II",
            "oWPCannon1x2Pierce": "Penetrator",
            "oWPCannon1x3": "Zeus Cannon",
            "oWPCannon2": "Storm Cannon I",
            "oWPCannon2Breach": "Flayer Cannon",
            "oWPCannon3": "Storm Cannon II",
            "oWPCannon6": "Storm Cannon III",
            "oWPCannonCrew1": "Radium Blaster I",
            "oWPCannonCrew2": "Radium Blaster II",
            "oWPCannonHull1": "Hull Ripper I",
            "oWPCannonHull2": "Hull Ripper II",
            "oWPCannonPsnCloud1": "Putrefactor I",
            "oWPCannonPsnCloud2": "Putrefactor II",
            "oWPCannonSlow1": "Graviton Cannon",
            "oWPBeam1": "Energy Beam I",
            "oWPBeamPoison": "Corruption Beam",
            "oWPBeamZombie": "Grave Beam",
            "oWPPierceBeam1": "Devastator Beam",
            "oWPArea3": "Fusillade I",
            "oWPArea8": "Fusillade II",
            "oWPAreaMag2": "Magnetic Pulse I",
            "oWPAreaIon5": "Ion Tunneler",
            "oWPDisruptor": "Disruptor",
            "oWPDisruptor2": "Twin Disruptor",
            "oWPLanceIon": "Heavy Ion Lance",
            "oWPLance1": "Energy Lance",
            "oWPLance2": "Heavy Energy lance",
            "oWPLance3": "Macro Lance",
            "oWPLanceBreach": "Kinetic Lance",
            "oWPLanceSlow": "Gravitic Lance",
            "oWPLanceStun": "Neural Lance",
            "oWPLanceWarp1": "Warp Lance",
            "oWPBlessedLance": "Flame Lance",
            "oWPMissile1x1Basic": "Gladius Missile",
            "oWPMissile1x10": "Antimatter Bomb",
            "oWPMissile1x1PsnCloud": "Acid Missile",
            "oWPMissile1x1Slow": "Graviton Bomb",
            "oWPMissile1x2": "Sabre Missile",
            "oWPMissile1x2Breach": "Heavy Flayer Missile",
            "oWPMissile1x2Hull": "Siege Missile",
            "oWPMissile1x3": "Claymore Missile",
            "oWPMissileFire": "Hellfire Missile",
            "oWPMissileIon2": "Heavy Disruptor Missile",
            "oWPMissileWarp": "Rift Bomb",
            "oWPCannon1Teleport": "Displacement Field Emitter",
            "oWPBeam2": "Energy Beam II",
            "oWPBeamBreach": "Flayer Beam",
            "oWPCannon8": "Storm Cannon Array",
            "oWPBeamFire1": "Heat Beam I",
            "oWPBeamFire2": "Heat Beam II",
            "oWPBeamInferno": "Inferno Beam",
            "oWPBeamSlow": "Gravitic Ray",
            "oWPBeamStun": "Neuralizer",
            "oWPHyperBeam": "Macro Devastator",
            "oWPAreaFire4": "Inferno Fougasse",
            "oWPAreaMag3": "Magnetic Pulse II",
            "oWPAreaMag5": "Magnetic Pulse III",
            "oWPDisruptorHeavy": "Heavy Disruptor",
            "oWPDisruptorMacro": "Macro Disruptor",
            "oWPDisruptorRapid": "Auto-Disruptor",
            "oWPMissile1x1": "Shiv Missile",
            "oWPMissile1x1Breach": "Flayer Missile",
            "oWPMissile1x2PsnCloud": "Blight Bomb",
            "oWPMissileFire2": "Incendiary Missile",
            "oWPMissileIon1": "Disruptor Missile",
            "oWPMissileSprint": "Fury Missile",
            "oWPMissileStun": "Terror Missile",
            "oWPMissileTeleport": "Displacement Bomb"
        }
        
        # Create reverse weapon map for saving
        self.weapon_display_to_key = {v: k for k, v in self.weapon_map.items()}
        
        # Equipment mapping dictionary with string keys
        self.equipment_map = {
            -1.0: "Empty Slot",
            "oItemAxe_doorBreak": "Siege Axe",
            "oItemArmor_basic30": "Chaos Armor",
            "oItemArmor_basic5": "Combat Mesh",
            "oItemArmor_basic15": "Duraplate Armor",
            "oItemArmor_basic10": "Ferro-plas Vest",
            "oItemArmor_psnImm": "Fetid Rags",
            "oItemArmor_fireImm": "Fire Suit",
            "oItemArmor_basic20": "Heavy Duraplate Armor",
            "oItemArmor_fireImm10": "Hellfire Cuirass",
            "oItemArmor_vacImm": "Pressure Suit",
            "oItemArmor_slowVacImm20": "Siege Armor",
            "oItemArmor_basic10_vacRes": "Tactical Armor",
            "oItemArmor_speedVacRes15": "Tactical Exoskeleton",
            "oItemAxe_basic3": "Fell Axe",
            "oItemAxe_basic2": "Power Axe",
            "oItemAxe_doorBreak": "Siege Axe",
            "oItemFist_sysDPS": "Arc Talons",
            "oItemFist_doorBreakBreach": "Assault Drill",
            "oItemFist_lifeSteal": "Eviscerator",
            "oItemFist_basic1": "Power Claw",
            "oItemFist_sysDmgOnKill": "Pulverizer",
            "oItemFist_basic2": "Siege Claw",
            "oItemGun_sysDPS": "Arc Rifle",
            "oItemGun_rapidFire1": "Assault Rifle",
            "oItemGun_beam": "Beam Carbine",
            "oItemGun_rapidFire3_antiDemon": "Blessed Machine Cannon",
            "oItemGun_slow": "Grav-Carbine",
            "oItemGun_explode": "Grenade Launcher",
            "oItemGun_ionOnKill": "Ion Carbine",
            "oItemGun_rapidFire3": "Machine Cannon",
            "oItemGun_rapidFire2": "Machine Rifle",
            "oItemGun_flame2": "Magma Gun",
            "oItemGun_flame": "Plasma Projector",
            "oItemPistol_poison": "Rotblaster",
            "oItemHammer_doorBreak_sysBreak": "Assault Sledge",
            "oItemHammer_antiDemon": "Blessed Hammer",
            "oItemHammer_stun": "Electro-Maul",
            "oItemHammer_explode": "Gore Sledge",
            "oItemHammer_sysDmgOnKill": "Havoc Maul",
            "oItemHammer_basic1": "Power Hammer",
            "oItemHammer_antiHeavy": "War Pick",
            "oItemKnife_basic": "Combat Knife",
            "oItemKnife_poison": "Plague Knife",
            "oItemMace_stun": "Electrobaton",
            "oItemMace_cleanse": "Holy Scepter",
            "oItemMace_basic1": "Spiked Club",
            "oItemPistol_moveSpeed": "Assault Pistol",
            "oItemPistol_explode": "Goreblaster",
            "oItemPistol_rapidFire": "Machine Pistol",
            "oItemSpear_drainStrength": "Cursed Spear",
            "oItemSpear_slow": "Grav-Spear",
            "oItemSpear_basic2": "Power Glaive",
            "oItemSpear_DPSOnKill": "Soul Thresher",
            "oItemSpear_lifeSteal": "Thirsting Glaive",
            "oItemSword_zombieOnKill": "Athame",
            "oItemSword_antiDemon": "Blessed Blade",
            "oItemSword_antiHeavy": "Ceremonial Sword",
            "oItemSword_antiLight": "Cult Blade",
            "oItemSword_chainsaw": "Decapitator",
            "oItemSword_hellfire": "Hellfire Blade",
            "oItemSword_poison": "Plague Sword",
            "oItemSword_basic": "Power Sword",
            "oItemSword_zenith": "Zenith Blade",
            "oItemShield_DPS2": "Assault Shield",
            "oItemShield_basic": "Ballistic Shield",
            "oItemShield_DPS1": "Combat Shield",
            "oItemShield_HP20_slow": "Fortress Shield",
            "oItemShield_HP10": "Imperial Aegis",
            "oItemShield_speed_negHP5": "Parasite Shield",
            "oItemShield_stunSlow": "Riot Shield",
            "oItemShield_HP5": "Tactical Shield",
            "oItemWard_DG_HP10_slow": "Cathedral Ward",
            "oItemWard_DG_DPS": "Chronofield",
            "oItemWard_DG_basic": "Prismatic Veil",
            "oItemWard_DG_speed_negHP5": "Unholy Talisman",
            "oItemOxygenTank": "Oxygen Tank",
            "oItemPowerField": "Power Field",
            "oItemServoArm": "Servo-Arm",
            "oItemWeldingTorch": "Welding Torch",
            "oItemTeleportRoomRandom": "Chaos Engine",
            "oItemTeleportRoomTarget": "Heavy Translocator",
            "oItemTeleportSelfTarg": "Translocator",
            "oItemTeleportGroupTarget": "Aetheric Gate",
            "oItemTeleportTarget": "Aetherstride",
            "oItemSummonZombie2x": "Animate Dead",
            "oItemSummonZombiePoison3x": "Animate Noxious Dead",
            "oItemWretchCannon": "Blood Spear",
            "oItemSpawnThrallTarget": "Bloodcurse",
            "oItemSlowTarget": "Burden",
            "oItemTeleportProjectile": "Chaotic Rift",
            "oItemWretchSealCannon": "Coagulate",
            "oItemStrengthDrainTarget3": "Drain Strength",
            "oItemFearNearbyAll": "Fear",
            "oItemFireball": "Fireball",
            "oItemForceShield": "Force Shield",
            "oItemSummonZombie5x": "Greater Animate Dead",
            "oItemMindBolt": "Mind Bolt",
            "oItemStunCannon2": "Psychic Shriek",
            "oItemCleanse": "Purify",
            "oItemHeal": "Rejuvenate",
            "oItemPoisonRoomInstant": "Smother",
            "oItemPsyCannon": "Soul Spear",
            "oItemPsyCannon2": "Soul Barrage",
            "oItemPsyCannon3": "Soul Storm",
            "oItemSummonDemonBloat": "Summon Bloatmite",
            "oItemSummonDemonImp3x": "Summon Fleshlings",
            "oItemSummonDemonHound": "Summon Hound",
            "oItemSummonDemonBlob": "Summon Necrolurch",
            "oItemSummonRevenant_eidolon": "Summon Skeletons",
            "oItemSummonZombieBlood": "Summon Thrall",
            "oItemWretchHealCannon": "Transfusion",
            "oItemMindControl": "Treasonous Whispers",
            "oItemSystemCannotRepair": "Techno Virus",
            "oConsumableRepairHull": "Hull Integrity Patch",
            "oConsumableMedKitRemote": "Med-Drone",
            "oConsumableAntidote": "Antidote",
            "oConsumableExtinguisher": "Cryofoam",
            "oConsumableTeleportRoomTarget": "Dark Matter Prism",
            "oConsumableDamageSystem": "Fusion Charge",
            "oConsumableDeployableShield": "Microshield",
            "oConsumableDamageControlRemote": "Repair Drone",
            "oConsumableSummonBloat": "Bloated Reagents",
            "oConsumableSummonEidolon": "Doom Reagents",
            "oConsumableSummonRedeemer": "Exalted Reagents",
            "oConsumableSummonDemonImp3x": "Fleshy Reagents",
            "oConsumableSummonMaw": "Hungering Reagents",
            "oConsumableSummonBlob": "Necrotizing Reagents",
            "oConsumableSummonHellbringer": "Ruinous Reagents",
            "oConsumableSummonHydra": "Stygian Reagents",
            "oItemFist_doorBreak": "Ripper Fist",
            "oItemSummonDemonWar": "Doom Ritual",
            "oItemSummonDemonCambion": "Summon Fiend",
            "oItemSummonDemonMaw": "Summon Hungerer",
            "oItemSummonDemonHydraHead": "Summon Stygian Worm",
            "oItemTeleportToWretch": "Thrallwalk"
        }
        
        # Create reverse equipment map for saving
        self.equipment_display_to_key = {v: k for k, v in self.equipment_map.items()}
        
        # Module mapping dictionary remains the same
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
            "oModule_HP_blood": "Pain Engine: +10 HP to all Blood Cultist units.",
            "oModule_doorBreakInvulnerable": "Bunker Drills: Your crew are invulnerable against crew attacks while breaking doors.",
            "oModule_forceShieldOnWeaponShot": "Barrier Relay: For every other weapon you fire, gain a force shield on a random room: up to a maximum of 2.",
            "oModule_rewardExtraCrystal": "Thrice-cursed Reliquary: Frequently gain a Dark Matter Prism: in addition to normal rewards after defeating an enemy ship.",
            "oModule_poisonSlowsRepair": "Corpse Effigy: Halves the repair speed of poisoned enemies.",
            "oModule_doorBreakStun": "Assault Harnesses: Your crew will stun nearby enemy crew for 8s upon destroying a door.",
            "oModule_sensorVisionGainEvasion": "Vector Analyzer: Gain 10% Evasion while your Sensor Status is Active.",
            "oModule_sensorVisionLoseEvasion": "Inertial Probe: Enemy ships lose 10% Evasion when your Sensor Status is Active.",
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
            "oModule_lanceBonusDamageCostCrewHP": "Demon Lance: Lances deal 1 extra damage for each crew aboard your ship. Each lance shot you fire depletes the current HP of all shipboard crew by 50%.",
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
            "oModule_bonusCrewHound": "Seal of Cerberus: Call upon a demonic Hound.",
            "oModule_fightStartHullInvulnerable": "Temporal Shroud: Immunity to hull damage and system damage from enemy projectiles for the first 25 seconds of combat.",
            "oModule_spellsDoDamage": "Hate Matrix: All non-summoning psychic projetiles deal 1 extra damage to the targeted ship in addition to their normal effect.",
            "oModule_firstWeaponAlwaysHits": "Ghost-Linked Reticle: The first time your ship fires a weapon during a fight, it always hits.",
            "oModule_DPS_HP_demon": "Obscene Organ: +1 DPS and +10 HP to all Demonic units",
            "oModule_bonusCrewOnEnemySpellCast": "Vile Sepulchre: Once per fight, summon a random demon on the first enemy crew to use a psychic power.",
            "oModule_firstWeaponDoubleDamage": "Reaper Shells: The first time your ship fires a damaging weapon during a fight, that weapon's base damage is doubled."
        }
        
        # Create inverse module map for saving
        self.inv_module_map = {v: k for k, v in self.module_map.items()}
        
        # Default save location
        self.default_dir = os.path.join(os.getenv('APPDATA'), 'Void_War')
        self.save_data = None
        self.original_save_data = None
        self.original_values = {}
        
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
        self.original_modules = {}  # Store original module data
        
        for i in range(3):
            slot_frame = tk.Frame(self.modules_frame)
            slot_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = tk.Label(slot_frame, text=f"Slot {i+1}:", width=8, anchor="w")
            label.pack(side=tk.LEFT, padx=(5, 0))
            
            combo = ttk.Combobox(slot_frame, width=25, state="normal")
            module_names = sorted([name for name in self.module_map.values()])
            combo['values'] = module_names
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
                self.original_save_data = f.read()
                self.save_data = self.original_save_data
                self.current_file_path = file_path
                self.backup_path = file_path + ".bak"
            
            # Store original values for comparison
            self.original_values = {}
            
            # Find scrap value
            scrap_match = re.search(r'"currScrap":(\d+\.?\d*)', self.save_data)
            missile_match = re.search(r'"playerMissileCt":(\d+\.?\d*)', self.save_data)
            
            if scrap_match:
                scrap_value = scrap_match.group(1)
                self.scrap_entry.delete(0, tk.END)
                self.scrap_entry.insert(0, scrap_value)
                self.original_values['scrap'] = scrap_value
            else:
                raise ValueError("Scrap value not found in save file")
                
            if missile_match:
                missile_value = missile_match.group(1)
                self.missile_entry.delete(0, tk.END)
                self.missile_entry.insert(0, missile_value)
                self.original_values['missile'] = missile_value
            else:
                raise ValueError("Missile count not found in save file")
            
            # Find cargo list with formatting
            cargo_match = re.search(r'"cargoList":\s*(\[.*?\])', self.save_data, re.DOTALL)
            if cargo_match:
                # Store original cargo list with formatting
                self.original_values['cargo_list_str'] = cargo_match.group(1)
                
                # Extract just the items
                cargo_items = []
                items_str = re.search(r'\[(.*)\]', self.original_values['cargo_list_str'], re.DOTALL)
                if items_str:
                    for item in items_str.group(1).split(','):
                        item = item.strip()
                        if item == '-1.0':
                            cargo_items.append(-1.0)
                        elif item.startswith('"') and item.endswith('"'):
                            # String identifier
                            cargo_items.append(item[1:-1])
                        else:
                            # Try to parse as float, but only allow -1.0
                            try:
                                num_val = float(item)
                                if num_val == -1.0:
                                    cargo_items.append(num_val)
                                else:
                                    # Unexpected number, treat as string
                                    cargo_items.append(item)
                            except ValueError:
                                # Not a number, treat as string
                                cargo_items.append(item)
                
                # Pad to 4 slots
                if len(cargo_items) < 4:
                    cargo_items += [-1.0] * (4 - len(cargo_items))
                
                # Set values in UI
                self.original_values['cargo'] = cargo_items[:4]
                for i, value in enumerate(cargo_items[:4]):
                    if value in self.weapon_map:
                        display_value = self.weapon_map[value]
                    else:
                        # Handle unknown items
                        display_value = str(value)
                    self.cargo_combos[i].set(display_value)
            else:
                self.original_values['cargo_list_str'] = "[-1.0, -1.0, -1.0, -1.0]"
                self.original_values['cargo'] = [-1.0] * 4
                for i in range(4):
                    self.cargo_combos[i].set("Empty Slot")
                self.status.config(text="Cargo list not found - initialized with empty slots")
            
            # Find equipment list and quantities with formatting
            equipment_list_match = re.search(r'"equipmentList":\s*(\[.*?\])', self.save_data, re.DOTALL)
            equipment_qt_match = re.search(r'"equipmentQt":\s*(\[.*?\])', self.save_data, re.DOTALL)
            
            if equipment_list_match and equipment_qt_match:
                # Store original lists with formatting
                self.original_values['equipment_list_str'] = equipment_list_match.group(1)
                self.original_values['equipment_qt_str'] = equipment_qt_match.group(1)
                
                # Extract equipment items
                equipment_items = []
                eq_items_str = re.search(r'\[(.*)\]', self.original_values['equipment_list_str'], re.DOTALL)
                if eq_items_str:
                    for item in eq_items_str.group(1).split(','):
                        item = item.strip()
                        if item == '-1.0':
                            equipment_items.append(-1.0)
                        elif item.startswith('"') and item.endswith('"'):
                            # String identifier
                            equipment_items.append(item[1:-1])
                        else:
                            # Try to parse as float, but only allow -1.0
                            try:
                                num_val = float(item)
                                if num_val == -1.0:
                                    equipment_items.append(num_val)
                                else:
                                    # Unexpected number, treat as string
                                    equipment_items.append(item)
                            except ValueError:
                                # Not a number, treat as string
                                equipment_items.append(item)
                
                # Parse quantities
                qt_values = []
                qt_items_str = re.search(r'\[(.*)\]', self.original_values['equipment_qt_str'], re.DOTALL)
                if qt_items_str:
                    for item in qt_items_str.group(1).split(','):
                        item = item.strip()
                        try:
                            qt_values.append(float(item))
                        except ValueError:
                            qt_values.append(0.0)
                
                # Pad arrays if needed
                if len(equipment_items) < 8:
                    equipment_items += [-1.0] * (8 - len(equipment_items))
                if len(qt_values) < 8:
                    qt_values += [0.0] * (8 - len(qt_values))
                
                # Store original values
                self.original_values['equipment'] = equipment_items[:8]
                self.original_values['quantity'] = qt_values[:8]
                
                # Set values in UI
                for i, (eq_val, qt_val) in enumerate(zip(equipment_items[:8], qt_values[:8])):
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
                self.original_values['equipment_list_str'] = "[-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]"
                self.original_values['equipment_qt_str'] = "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
                self.original_values['equipment'] = [-1.0] * 8
                self.original_values['quantity'] = [0.0] * 8
                for i in range(8):
                    self.equipment_combos[i].set("Empty Slot")
                    self.quantity_entries[i].delete(0, tk.END)
                    self.quantity_entries[i].insert(0, "0.0")
                self.status.config(text="Equipment lists not found - initialized with empty slots")
            
            # Find ship modules
            self.module_slot_present = [False, False, False]  # Reset presence flags
            self.original_modules = {}  # Clear previous module data
            
            # Create regex pattern to find modules
            module_pattern = re.compile(r'"moduleSlot":(\d)\.0.*?"obj":"([^"]+)"', re.DOTALL)
            
            # Find all modules in save data
            modules = {}
            for match in module_pattern.finditer(self.save_data):
                slot_index = int(match.group(1))
                module_obj = match.group(2)
                modules[slot_index] = module_obj
            
            # Store original module values
            self.original_values['modules'] = modules
            
            # Populate module slots
            for slot_index in range(3):
                if slot_index in modules:
                    module_obj = modules[slot_index]
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
                display_name = combo.get().strip()
                
                if display_name == "Empty Slot":
                    cargo_values.append(-1.0)
                elif display_name in self.weapon_display_to_key:
                    # Get the string key for this display name
                    key = self.weapon_display_to_key[display_name]
                    cargo_values.append(key)
                else:
                    # Fallback to using display name as key
                    cargo_values.append(display_name)
            
            # Process equipment values and quantities
            equipment_values = []
            quantity_values = []
            
            for i, (combo, qty_entry) in enumerate(zip(self.equipment_combos, self.quantity_entries)):
                display_name = combo.get().strip()
                qty_value = qty_entry.get().strip()
                
                # Validate quantity
                if not re.match(r'^\d+(\.\d*)?$', qty_value):
                    raise ValueError(f"Invalid quantity in equipment slot {i+1}. Must be a number")
                
                # Convert to float
                qty_float = float(qty_value)
                
                # Process equipment type
                if display_name == "Empty Slot":
                    equipment_values.append(-1.0)
                    quantity_values.append(0.0)
                elif display_name in self.equipment_display_to_key:
                    # Get the string key for this display name
                    key = self.equipment_display_to_key[display_name]
                    equipment_values.append(key)
                    quantity_values.append(qty_float)
                else:
                    # Fallback to using display name as key
                    equipment_values.append(display_name)
                    quantity_values.append(qty_float)
            
            # Start with original data
            updated_data = self.original_save_data
            changes_made = False
            
            # Update scrap if changed
            if new_scrap != self.original_values['scrap']:
                updated_data = re.sub(
                    r'("currScrap":)(\d+\.?\d*)',
                    f'\\g<1>{new_scrap}',
                    updated_data
                )
                changes_made = True
            
            # Update missile count if changed
            if new_missile != self.original_values['missile']:
                updated_data = re.sub(
                    r'("playerMissileCt":)(\d+\.?\d*)',
                    f'\\g<1>{new_missile}',
                    updated_data
                )
                changes_made = True
            
            # Update cargo list if changed - preserve original formatting
            if 'cargo' in self.original_values and cargo_values != self.original_values['cargo']:
                # Create new cargo list with original formatting
                new_cargo_list = self.original_values['cargo_list_str']
                
                # Replace each item while preserving formatting
                for i in range(4):
                    orig_val = self.original_values['cargo'][i]
                    new_val = cargo_values[i]
                    
                    # Format new value properly
                    if new_val == -1.0:
                        new_val_str = "-1.0"
                    elif isinstance(new_val, str):
                        new_val_str = f'"{new_val}"'
                    else:
                        new_val_str = str(new_val)
                    
                    # Format original value for regex
                    if orig_val == -1.0:
                        orig_val_str = r'-1\.0'
                    elif isinstance(orig_val, str):
                        orig_val_str = re.escape(f'"{orig_val}"')
                    else:
                        orig_val_str = re.escape(str(orig_val))
                    
                    # Replace only this specific occurrence
                    pattern = re.compile(orig_val_str, re.DOTALL)
                    new_cargo_list, count = pattern.subn(new_val_str, new_cargo_list, 1)
                    
                    if count == 0:
                        # Fallback if we couldn't find exact match
                        # This is safer than replacing the whole array
                        self.status.config(text="Warning: Could not find exact cargo item to replace")
                
                # Replace the entire cargo list with updated version
                updated_data = updated_data.replace(self.original_values['cargo_list_str'], new_cargo_list)
                changes_made = True
            
            # Update equipment lists if changed - preserve original formatting
            if ('equipment' in self.original_values and 'quantity' in self.original_values and 
                (equipment_values != self.original_values['equipment'] or 
                 quantity_values != self.original_values['quantity'])):
                
                # Update equipment list
                new_equipment_list = self.original_values['equipment_list_str']
                for i in range(8):
                    orig_val = self.original_values['equipment'][i]
                    new_val = equipment_values[i]
                    
                    # Format new value properly
                    if new_val == -1.0:
                        new_val_str = "-1.0"
                    elif isinstance(new_val, str):
                        new_val_str = f'"{new_val}"'
                    else:
                        new_val_str = str(new_val)
                    
                    # Format original value for regex
                    if orig_val == -1.0:
                        orig_val_str = r'-1\.0'
                    elif isinstance(orig_val, str):
                        orig_val_str = re.escape(f'"{orig_val}"')
                    else:
                        orig_val_str = re.escape(str(orig_val))
                    
                    # Replace only this specific occurrence
                    pattern = re.compile(orig_val_str, re.DOTALL)
                    new_equipment_list, count = pattern.subn(new_val_str, new_equipment_list, 1)
                    
                    if count == 0:
                        self.status.config(text="Warning: Could not find exact equipment item to replace")
                
                # Update quantity list
                new_quantity_list = self.original_values['equipment_qt_str']
                for i in range(8):
                    orig_val = self.original_values['quantity'][i]
                    new_val = quantity_values[i]
                    
                    # Format new value properly
                    new_val_str = str(new_val)
                    
                    # Format original value for regex
                    orig_val_str = re.escape(str(orig_val))
                    
                    # Replace only this specific occurrence
                    pattern = re.compile(orig_val_str, re.DOTALL)
                    new_quantity_list, count = pattern.subn(new_val_str, new_quantity_list, 1)
                    
                    if count == 0:
                        self.status.config(text="Warning: Could not find exact quantity to replace")
                
                # Replace both lists in the save data
                updated_data = updated_data.replace(self.original_values['equipment_list_str'], new_equipment_list)
                updated_data = updated_data.replace(self.original_values['equipment_qt_str'], new_quantity_list)
                changes_made = True
            
            # Update modules if changed
            if 'modules' in self.original_values:
                for slot_index in range(3):
                    if slot_index in self.original_values['modules']:
                        display_name = self.module_combos[slot_index].get().strip()
                        if not display_name:
                            continue
                        
                        # Convert display name back to object name
                        if display_name in self.inv_module_map:
                            obj_name = self.inv_module_map[display_name]
                        else:
                            obj_name = display_name
                        
                        # Skip if not changed
                        if obj_name == self.original_values['modules'][slot_index]:
                            continue
                        
                        # Create precise pattern for replacement
                        original_obj = re.escape(self.original_values['modules'][slot_index])
                        pattern = re.compile(
                            rf'(?s)("moduleSlot":{slot_index}\.0.*?"obj":\s*"){original_obj}(")',
                            re.DOTALL
                        )
                        
                        # Replace with new object name
                        replacement = f'\\g<1>{obj_name}\\g<2>'
                        updated_data = pattern.sub(replacement, updated_data, 1)
                        changes_made = True
            
            # Only proceed if changes were made
            if not changes_made:
                self.status.config(text="No changes detected - file not modified")
                return
            
            # Create backup
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)
            os.rename(self.current_file_path, self.backup_path)
            
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