import csv
import logging
import pathlib
from typing import Dict

logger = logging.getLogger(__name__)

GAME_DATA_FILENAME_MAP = {
    "armor": "Armors.csv",
    "consumable": "Consumables.csv",
    "psychic": "Psychics.csv",
    "tool": "Tools.csv",
    "weapon": "Weapons.csv",
    "ship_module": "ShipModules.csv",
    "ship_weapon": "ShipWeapons.csv",
}

ITEM_MAP = {
    "equipment": ["armor", "consumable", "psychic", "tool", "weapon"],
    "cargo": ["ship_module", "ship_weapon"],
}


class GameData:

    def __init__(self):
        """
        Initializes the GameData instance and loads game data from CSV files.
        """
        self.data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
        # Explicitly declare each category
        self.armor = self._get_game_data(GAME_DATA_FILENAME_MAP["armor"])
        self.consumable = self._get_game_data(GAME_DATA_FILENAME_MAP["consumable"])
        self.psychic = self._get_game_data(GAME_DATA_FILENAME_MAP["psychic"])
        self.tool = self._get_game_data(GAME_DATA_FILENAME_MAP["tool"])
        self.weapon = self._get_game_data(GAME_DATA_FILENAME_MAP["weapon"])
        self.ship_module = self._get_game_data(GAME_DATA_FILENAME_MAP["ship_module"])
        self.ship_weapon = self._get_game_data(GAME_DATA_FILENAME_MAP["ship_weapon"])

        # Logging and item_id_name_map population combined
        self.item_id_name_map = {}
        for category in GAME_DATA_FILENAME_MAP.keys():
            category_data: Dict[str, dict] = getattr(self, category, {})
            if not category_data:
                logger.warning(f"No data found for category: {category}")
            else:
                logger.debug(
                    f"Loaded {len(category_data)} entries for category: {category}"
                )
            for item_id, item_data in category_data.items():
                item_name = item_data.get("Name", "")
                if item_id and item_name:
                    self.item_id_name_map[item_id] = item_name
        self.item_name_id_map = {v: k for k, v in self.item_id_name_map.items()}

    def format_id(self, id_value: str) -> str:
        """
        Formats the ID value by prefixing a "o" character (2025.07.15).
        """
        return f"o{id_value}" if id_value else None

    def _get_game_data(self, file_name: str) -> dict:
        """
        Reads a CSV file and returns its contents as a dictionary
        where the keys are the values in the "Id" column.

        Args:
            file_name (str): The name of the CSV file to read.

        Returns:
            dict: A dictionary with "Id" as keys and the rest of the row as values.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the CSV file does not contain an "Id" column.
        """
        file_path = self.data_dir / file_name
        if not file_path.exists():
            logger.error(f"Data file {file_name} not found in {self.data_dir}")
            raise FileNotFoundError(f"Data file {file_name} not found.")
        data = {}
        with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if "Id" not in row:
                    raise ValueError(f"CSV file {file_name} must contain 'Id' column.")
                formatted_id = self.format_id(row["Id"])
                del row["Id"]
                data[formatted_id] = row
        return data
