from pathlib import Path
import logging
import logging.handlers

def configure_logger(name=''):
	LOG_FORMAT = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
	
	Path("./logs").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
	log = logging.getLogger(name)
	handler = logging.handlers.TimedRotatingFileHandler(filename='./logs/gomway.log',
										when="midnight",
										backupCount=15)
	formatter = logging.Formatter(LOG_FORMAT)
	handler.setFormatter(formatter)
	log.addHandler(handler)
	return log
