import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
        'RESET': '\033[0m',  # Reset
    }

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = self.COLORS.get(levelname, self.COLORS['RESET'])
        return color + message + self.COLORS['RESET']
    
def set_log_color_level(level):
    logger = logging.getLogger()
    logger.setLevel(level)

    # 检查是否已经有 console handler
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s\n')
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(console_handler)

    # 防止日志消息向上传播到根日志器
    logger.propagate = False    

    # Test messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")