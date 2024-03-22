import logging

# Create a logger instance
LOGGER = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(filename='history.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a stream handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the stream handler to the logger
LOGGER.addHandler(console_handler)