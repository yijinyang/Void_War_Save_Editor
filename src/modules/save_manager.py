import ast
import datetime
import json
import logging
from pathlib import Path
from tkinter import filedialog
from typing import List

from .utils import enforce_positive_float

logger = logging.getLogger(__name__)


class SaveManager:

    EMPTY_SLOT = -1.0

    PLAYER_DATA_TAG = "playerData"
    GAME_OBJECT_DATA_TAG = "gameObjectData"

    SCRAP_TAG = "currScrap"
    MISSILE_COUNT_TAG = "playerMissileCt"

    EQUIPMENT_LIST_TAG = "equipmentList"
    EQUIPMENT_QUANTITY_TAG = "equipmentQt"
    EQUIPMENT_VIEWED_TAG = "equipmentHasBeenViewed"

    CARGO_LIST_TAG = "cargoList"
    CARGO_VIEWED_TAG = "cargoHasBeenViewed"

    MODULE_SLOT_TAG = "moduleSlot"
    MODULE_OBJECT_ID_TAG = "obj"

    def __init__(self):
        self.default_dir = Path.home() / "AppData" / "Roaming" / "Void_War"
        self.save_file_path: Path = None
        self.save_data_raw: str = None
        self.save_data: dict = {}

        self.save_file_path = self._get_user_save_file()
        if not self.save_file_path:
            logger.info("No save file selected. Exiting SaveManager initialization.")
            return
        self._create_backup()
        self._load_save_data()

        if self.save_data_raw:
            try:
                # Remove null bytes and fix lowercase booleans before parsing
                cleaned_data = self.save_data_raw.replace("\x00", "")
                cleaned_data = cleaned_data.replace("true", "True").replace(
                    "false", "False"
                )
                self.save_data = ast.literal_eval(cleaned_data)
            except (SyntaxError, ValueError) as e:
                logger.error(f"Failed to convert save data: {str(e)}")
                raise

        if self.PLAYER_DATA_TAG not in self.save_data:
            raise ValueError(
                f"Invalid save data format: Save data does not contain '{self.PLAYER_DATA_TAG}' key."
            )

        # Update this if game data structure changes
        self.player_data: dict = self.save_data[self.PLAYER_DATA_TAG][0]

        # Update equipment and cargo max storage based on player data
        self.equipment_max_storage_count = len(
            self.player_data[self.EQUIPMENT_LIST_TAG]
        )
        self.cargo_max_storage_count = len(self.player_data[self.CARGO_LIST_TAG])

        # Game Data for module slot
        self.game_object_data: List[dict] = self.save_data[self.GAME_OBJECT_DATA_TAG]
        self.modules = {}
        for game_object in self.game_object_data:
            if self.MODULE_SLOT_TAG not in game_object:
                continue
            module_slot_number = game_object[self.MODULE_SLOT_TAG]
            if module_slot_number not in self.modules:
                self.modules[int(module_slot_number)] = game_object
        self.module_count = len(self.modules)

    # ===================================================================================
    # Save File Management
    # ===================================================================================
    def _get_user_save_file(self):
        """Prompt user to select a .sav file."""
        initial_dir = (
            self.default_dir
            if self.default_dir.exists()
            else Path.home() / "AppData" / "Roaming"
        )
        logger.debug(f"Prompting user to select a save file in {initial_dir}")
        file_path = filedialog.askopenfilename(
            title="Select Void War autosav.sav",
            initialdir=str(initial_dir),
            filetypes=(("Save files", "*.sav"), ("All files", "*.*")),
        )

        logger.debug(f"User selected file: {file_path}")
        if file_path and Path(file_path).name != "autosave.sav":
            raise ValueError(
                f"Selected file must be named 'autosave.sav'. Selected: {file_path}"
            )
        return Path(file_path)

    def _create_backup(self):
        """Create a backup of the original save file."""
        backup_dir = self.save_file_path.parent / "vwse_backups"
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"autosav_{timestamp}.bak"
        try:
            backup_path.write_text(self.save_file_path.read_text())
            logger.info(f"Backup created at {backup_path}")
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")

    def _load_save_data(self):
        """Load save data from the selected file."""
        try:
            self.save_data_raw = self.save_file_path.read_text()
            logger.debug(
                f"Loaded save data from {self.save_file_path} with {len(self.save_data_raw)} characters."
            )
        except Exception as e:
            raise ValueError(f"Failed to load save file: {str(e)}")

    def save_changes(self):
        """Save changes to the .sav file."""
        # Overwrite the original save file with the modified data
        if not self.save_file_path:
            raise ValueError("No save file path specified.")
        if not self.save_data:
            raise ValueError("No changes to save.")
        json_string = json.dumps(self.save_data)
        self.save_file_path.write_text(json_string)

    # ===================================================================================
    # Data Management
    # ===================================================================================
    def get_scrap(self) -> float:
        """Get the current scrap value from the save data."""
        return enforce_positive_float(self.player_data.get(self.SCRAP_TAG, 0.0))

    def set_scrap(self, new_scrap: float):
        """Update the scrap value in the save data."""
        self.player_data[self.SCRAP_TAG] = enforce_positive_float(new_scrap)

    def get_missile_count(self) -> float:
        """Get the current missile count from the save data."""
        return enforce_positive_float(self.player_data.get(self.MISSILE_COUNT_TAG, 0.0))

    def set_missile_count(self, new_count: float):
        """Update the missile count in the save data."""
        self.player_data[self.MISSILE_COUNT_TAG] = enforce_positive_float(new_count)

    def get_equipment_list(self) -> list:
        """Get a list of all equipment in the player's inventory."""
        return self.player_data.get(self.EQUIPMENT_LIST_TAG, [])

    def set_equipment_list(
        self, equipment_list: list, equipment_quantities: list = None
    ):
        """Set the player's equipment list and update related quantities.

        Args:
            equipment_list (list): The new equipment list to set.
            equipment_quantities (list, optional): The corresponding quantities for each equipment slot.
        """
        if not isinstance(equipment_list, list):
            raise ValueError("Equipment list must be a list.")
        # Fill missing slots with EMPTY_SLOT
        while len(equipment_list) < self.equipment_max_storage_count:
            equipment_list.append(self.EMPTY_SLOT)
        # Truncate the list to the maximum storage count
        equipment_list = equipment_list[: self.equipment_max_storage_count]
        self.player_data[self.EQUIPMENT_LIST_TAG] = equipment_list

        # Update equipment quantities
        if equipment_quantities is not None:
            # Fill/truncate quantities to match equipment slots
            while len(equipment_quantities) < self.equipment_max_storage_count:
                equipment_quantities.append(0)
            equipment_quantities = equipment_quantities[
                : self.equipment_max_storage_count
            ]
            self.player_data[self.EQUIPMENT_QUANTITY_TAG] = equipment_quantities
        else:
            self.player_data[self.EQUIPMENT_QUANTITY_TAG] = [
                1 if item != self.EMPTY_SLOT else 0 for item in equipment_list
            ]

        # Update equipment viewed status
        equipment_viewed = [
            False if item == self.EMPTY_SLOT else True for item in equipment_list
        ]
        self.player_data[self.EQUIPMENT_VIEWED_TAG] = equipment_viewed

    def get_cargo_list(self) -> list:
        """Get a list of all cargo in the player's inventory."""
        return self.player_data.get(self.CARGO_LIST_TAG, [])

    def set_cargo_list(self, cargo_list: list):
        """Set the player's cargo list and update related quantities.

        Args:
            cargo_list (list): The new cargo list to set.
        """
        if not isinstance(cargo_list, list):
            raise ValueError("Cargo list must be a list.")
        # Fill missing slots with EMPTY_SLOT
        while len(cargo_list) < self.cargo_max_storage_count:
            cargo_list.append(self.EMPTY_SLOT)
        # Truncate the list to the maximum storage count
        cargo_list = cargo_list[: self.cargo_max_storage_count]
        self.player_data[self.CARGO_LIST_TAG] = cargo_list
        # Update cargo viewed status
        cargo_viewed = [
            False if item == self.EMPTY_SLOT else True for item in cargo_list
        ]
        self.player_data[self.CARGO_VIEWED_TAG] = cargo_viewed

    def set_module_list(self, module_list: list):
        """Set the player's module list.

        Args:
            module_list (list): The new module list to set.
        """
        if not isinstance(module_list, list):
            raise ValueError("Module list must be a list.")
        if len(module_list) != self.module_count:
            raise ValueError(
                f"Module list length ({len(module_list)}) does not match module count ({self.module_count})."
            )
        for idx, obj_id in enumerate(module_list):
            self.set_module_slot(idx, obj_id)

    def set_module_slot(self, slot_number: int, obj_id: str):
        """Set the module slot for a specific slot number.
        Slot starts from 0 to module_count - 1.

        Args:
            slot_number (int): The slot number to set.
            obj_id (str): The object ID to assign to the slot.
        """
        if slot_number < 0 or slot_number >= self.module_count:
            raise ValueError("Invalid module slot number.")
        self.modules[slot_number][self.MODULE_OBJECT_ID_TAG] = obj_id

    def get_module_list(self) -> list:
        """
        Retrieve the list of module object IDs from the save data.
        """
        if not self.modules:
            return []
        sorted_slots = sorted(self.modules.keys())
        return [self.modules[slot][self.MODULE_OBJECT_ID_TAG] for slot in sorted_slots]
