import json
import os


def load_menu_data():
    """Đọc file menu.json"""

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "menu.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_menu_by_role(role):
    """Trả menu theo role"""

    data = load_menu_data()

    return data.get(role, data["guest"])