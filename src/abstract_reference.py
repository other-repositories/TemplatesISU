from abc import ABC
from abc import abstractmethod
import uuid
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

class abstract_reference(ABC):
    __unique_code:str =  uuid.uuid4()
    _name = ""
    
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, st) -> str:
        self.__unique_code = st


    def __init__(self, name = None):
        if(name is not None):
            self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        error_proxy.check( value.strip(), str, 50)
        self._name = value.strip()
    
    #@abstractmethod todo connect to other code
    #def set_compare_mode(self, other_object) -> bool:
    #    if other_object is  None: return False
    #    if not isinstance(other_object, abstract_model): return False
    #
    #    return self.__unique_code == other_object.unique_code
    
    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)

    @staticmethod
    def transform_to_dict(items: list):
        error_proxy.check(items, list)
        result = {}
        for position in items:
            result[ position.name ] = position
        return result           
            
    @staticmethod
    def create_fields(source) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы параметры!")
        
        items = list(filter(lambda x: not x.startswith("_") and not x.startswith("create_") , dir(source))) 
        result = []
        
        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                result.append(item)    
                
        return result
    
    
    