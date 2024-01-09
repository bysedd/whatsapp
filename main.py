from tasks.task import main_task
from src.constants import AVAILABLE_CHANNELS

if __name__ == "__main__":
    main_task(channels=AVAILABLE_CHANNELS, headless=False)
