import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Capture all logs from DEBUG level and above
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s ",  # Log format
    handlers=[
        # logging.StreamHandler(),  # Logs to console
        RotatingFileHandler("./logs/backend.log", maxBytes=1000000, backupCount=3),  # Logs to a file
    ],
)

logging.getLogger("watchman.main").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)