import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Daily log file
log_file = os.path.join(
    "logs",
    f"{datetime.now().strftime('%Y-%m-%d')}.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("EVA")

def log_exception(error, module="EVA"):
    logger.error(
        f"[{module}] {type(error).__name__}: {error}"
    )

# Hide external HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)