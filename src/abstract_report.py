import abc 
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference

class abstract_report(abc.ABC):
    __data = {}
    __fields = []    

    
    def __init__(self, _data):
        error_proxy.check(_data, dict)
        self.__data = _data
        

    @abc.abstractmethod
    def create(self, storage_key: str):
        error_proxy.check(storage_key, str)
        self.__fields = self.build(storage_key, self.__data)
        
        return ""  
    
    @staticmethod
    def build( storage_key: str, data: dict) -> list:
        error_proxy.check(storage_key, str)
        if data is None:
            raise operation_exception("No data!")
        
        if len(data) == 0:
            raise operation_exception("Data empty!")
        item = data[storage_key][0]
        result = abstract_reference.create_fields( item )
        return result    
    
    def _build(self, storage_key: str) -> list:
        return abstract_report.build(storage_key, self.__data)
        
        
    @property    
    def fields(self) -> list:
        return self.__fields    
            
    @property         
    def data(self) -> dict:
        return self.__data    