from models import DatabaseManager
from views import MainMenu
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(f"{BASE_DIR}/db")

if __name__ == '__main__':
    try:
        DatabaseManager.initialize()
        MainMenu.display()
    except KeyboardInterrupt:
        print('Interrupted')


