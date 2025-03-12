from models import DatabaseManager
from views import MainMenu
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

if __name__ == '__main__':
    DatabaseManager.initialize()
    try:
        MainMenu.display()
    except KeyboardInterrupt:
        print('Interrupted: Closing application...')


