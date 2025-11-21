import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os

class LoggingConfig:
    #General
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR = os.path.join(os.getcwd(), "logs")
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    MAX_BYTES = 10 * 1024 * 1024 #10mb per file
    BACKUP_COUNT = 5
    
    @staticmethod
    def setup(app):
        #create log dir if it doesnt already exist
        if not os.path.exists(LoggingConfig.LOG_DIR):
            os.makedirs(LoggingConfig.LOG_DIR)
            
        #Formatter
        formatter = logging.Formatter(LoggingConfig.LOG_FORMAT)
        
        #console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LoggingConfig.LOG_LEVEL)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
        
        #Rotating File Handler
        file_handler = RotatingFileHandler(
            LoggingConfig.LOG_FILE,
            maxBytes=LoggingConfig.MAX_BYTES,
            backupCount=LoggingConfig.BACKUP_COUNT
        )
        file_handler.setLevel(LoggingConfig.LOG_LEVEL)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        
        
        #Email handler for errors
        if app.config.get("MAIL_SERVER"):
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config.get("MAIL_PORT", 25)),
                fromaddr=app.config.get("MAIL_DEFAULT_SENDER"),
                toaddrs=[app.config.get("ADMIN_EMAIL", "admin@example.com")],
                subject="Application Error",
                credentials=(app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD")),
                secure=()
            )
            mail_handler.setLevel(logging.ERROR)
            mail_handler.setFormatter(formatter)
            app.logger.addHandler(mail_handler)
        
        app.logger.setLevel(LoggingConfig.LOG_LEVEL)