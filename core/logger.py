import logging
from logging.handlers import TimedRotatingFileHandler

log_handler = TimedRotatingFileHandler(
    "logs/logs.log",
    when="midnight",
    interval=1,
    backupCount=5
)

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
log_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(log_handler)