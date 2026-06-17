import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.db.tui import RestaurantUI

if __name__ == "__main__":
    app = RestaurantUI()
    app.run()