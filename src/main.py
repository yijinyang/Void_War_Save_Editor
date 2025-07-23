# import save manager module
from modules.save_manager import SaveManager
from modules.utils import get_logger

logger = get_logger()


from modules.game_data import GameData
from modules.user_interface import MainApp


def main():
    """
    Entry point for Void War Save Editor.
    Initializes SaveManager, GameData, and launches the Tkinter UI.
    Ensures no file changes if user closes the window before saving.
    """
    save_manager = SaveManager()
    if not save_manager.save_file_path:
        logger.info("No save file selected. Exiting.")
        return
    game_data = GameData()
    app = MainApp(save_manager, game_data)
    try:
        app.mainloop()
    except Exception as e:
        logger.error(f"Tkinter UI error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise
