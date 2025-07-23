import csv
import pathlib
import logging


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



class GameData:

    def __init__(self, data_dir: pathlib.Path):
        """
        Initializes the GameData instance and loads game data from CSV files.
        """
        self.data_dir = data_dir
        for category, file_name in GAME_DATA_FILENAME_MAP.items():
            category_data = self._get_game_data(file_name)
            if not category_data:
                logger.warning(f"No data found for category: {category}")
            else:
                logger.debug(
                    f"Loaded {len(category_data)} entries for category: {category}"
                )
            setattr(self, category, category_data)

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
