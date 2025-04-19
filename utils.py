# utils.py
import json
from datetime import datetime

def save_history_to_file(user_msg, bot_msg, file_path="history.json"):
    try:
        # Nếu file chưa tồn tại, tạo mới
        with open(file_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_msg
    })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
