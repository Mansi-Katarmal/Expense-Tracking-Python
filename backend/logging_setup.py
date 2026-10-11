import logging

def setup_logger(name,level =logging.DEBUG,log_file = 'server.log'):
    logger = logging.getLogger(name)
    
    logger.setLevel(level)
    filehandler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s , %(name)s , %(levelname)s , %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger