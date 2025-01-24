import logging

def setup_silent_logging():
    logging.basicConfig(
        level=logging.CRITICAL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.NullHandler()]  # No escribe en ningún lado
    )