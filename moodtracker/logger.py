from datetime import datetime
import traceback
import os
from config import ERROR_LOG_PATH


def log_error_to_file(e: Exception) -> None:
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
    with open(ERROR_LOG_PATH, "a") as f:
        f.write(datetime.now().astimezone().isoformat() + "\n")
        f.write(traceback.format_exc())
        f.write("\n" + "-" * 40 + "\n")  # Divider
