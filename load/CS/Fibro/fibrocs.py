from ipmp.receivers.fibro_reciever import FibroServer
import logging
from logging import StreamHandler
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

fp = sys.argv[1]
cc = sys.argv[2]
first_port = int(fp)
cs_count = int(cc)

for port in range(first_port, first_port+cs_count):
    logger = logging.getLogger(__name__ + f'_{port}')
    logger.setLevel('DEBUG')
    formater = logging.Formatter('%(levelname)s --[%(asctime)s] %(message)s')
    filename = datetime.now().strftime("%Y%m%d-%H%M%S")
    handler = logging.handlers.RotatingFileHandler(f"{port}-{filename}.log", maxBytes=100000000, backupCount=5)
    handler.setFormatter(formater)
    logger.addHandler(StreamHandler(stream=sys.stdout))
    logger.addHandler(handler)

    server = FibroServer('0.0.0.0', port, logger=logger)
    server.start()
