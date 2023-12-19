import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class BofLog:
    def __init__(self, level:int=logging.INFO, format:str="%(asctime)s - %(levelname)s - %(message)s")->None:
        logging.basicConfig(level=level, format=format)
        self.log_handler_collection = []
        self.root_format = format

    def SetLogLevel(self, level:int)->None:
        logging.getLogger().setLevel(level)
        for log_handler in self.log_handler_collection:
            log_handler.setLevel(level)    
            
    def SetLogFormat(self, format:str)->None:
        #logging.getLogger().setFormatter(format)
        #self.root_format=format
        for log_handler in self.log_handler_collection:
            log_handler.setFormatter(format)               
# StreamHandler, TimedRotatingFileHandler, SocketHandler, DatagramHandler, SysLogHandler, SMTPHandler, 
# NTEventLogHandler,HTTPHandler, BufferingHandler, MemoryHandler, QueueHandler, QueueListener
    #def AddConsoleHandler(self, level:int) -> None:
    #    handler = logging.StreamHandler()
    #    handler.setLevel(level)
    #    formatter = logging.Formatter(self.root_format)
    #    handler.setFormatter(formatter)
    #    logging.getLogger().addHandler(handler)
    #    self.log_handler_collection.append(handler)
                    
    def AddRotatingLog(self, level:int, log_file:str,max_file_size_bytes:int,backup_count:int):
        handler = RotatingFileHandler(log_file, maxBytes=max_file_size_bytes, backupCount=backup_count)
        handler.setLevel(level)
        formatter = logging.Formatter(self.root_format)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        self.log_handler_collection.append(handler)
        
    def AddTimedRotatingFileHandler(self, level:int, log_file: str, when: str, interval: int, backup_count: int) -> None:
        handler = TimedRotatingFileHandler(log_file, when=when, interval=interval, backupCount=backup_count)
        handler.setLevel(level)
        formatter = logging.Formatter(self.root_format)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        self.log_handler_collection.append(handler)        
        
    def Debug(self, msg:str)->None:
        logging.debug(msg)
 
    def Info(self, msg:str)->None:
        logging.info(msg)

    def Warning(self, msg:str)->None:
        logging.warning(msg)
    
    def Error(self, msg:str)->None:
        logging.error(msg)
    
    def Critical(self, msg:str)->None:
        logging.critical(msg)
