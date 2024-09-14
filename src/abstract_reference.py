from abc import ABC
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

class abstract_reference(ABC):
    __unique_code:str =  uuid.uuid4()
    _name = ""
    
    @property
    def unique_code(self) -> str:
        return self.__unique_code

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
    
    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is  None: return False
        if not isinstance(other_object, abstract_model): return False

        return self.__unique_code == other_object.unique_code
    
    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)
    
                
            
        
    
    
    
    