# import save manager module
from modules.save_manager import SaveManager
from modules.utils import get_logger

logger = get_logger()


def main():
    save_manager = SaveManager()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise
