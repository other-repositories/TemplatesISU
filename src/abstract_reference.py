from abc import ABC
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

class abstract_reference(ABC):
    _name = ""
    
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
    
    
                
            
        
    
    
    
    