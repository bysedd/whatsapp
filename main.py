from src.constants import AVAILABLE_CHANNELS
from tasks.task import main_task

if __name__ == "__main__":
    main_task(channels=AVAILABLE_CHANNELS, headless=False)
