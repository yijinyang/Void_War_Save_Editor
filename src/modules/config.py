import pathlib

SRC_DIR = pathlib.Path(__file__).resolve().parent.parent
SRC_DATA_DIR = SRC_DIR / "data"

GAME_DATA_FILENAME_MAP = {
    "armor": "Armors.csv",
    "consumable": "Consumables.csv",
    "psychic": "Psychics.csv",
    "tool": "Tools.csv",
    "weapon": "Weapons.csv",
    "ship_module": "ShipModules.csv",
    "ship_weapon": "ShipWeapons.csv",
}

# Save Data Constants

