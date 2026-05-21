import logging

def setup_logging():
    """Configures logging to output to both a file and the console."""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    log_filename = "trading_bot.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filename,encoding ="utf-8"),  # Saves to your hard drive
            logging.StreamHandler()             # Prints to your terminal screen
        ]
    )
    
    return logging.getLogger("trading_bot")