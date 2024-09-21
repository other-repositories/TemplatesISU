from src.abstract_reference import abstract_reference
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.errors.error_utils import error_proxy, argument_exception, operation_exception

from datetime import datetime

class receipt_model_unit(abstract_reference):
    __size: int = 0
    __nomenclature: nomenclature_model = None
    __unit: range_model = None
    
    def __init__(self):
        super().__init__()
    
    @property
    def nomenclature(self):
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        error_proxy.check(value, nomenclature_model)
        self._name = f"{value.name}"
        self.__nomenclature = value
    
    
    @property
    def size(self) -> float:
        return self.__size
    
    
    @size.setter
    def size(self, value ):
        error_proxy.check(value, (float, int))
        self.__size = value
    
    
    @property    
    def unit(self) -> range_model:
        return self.__unit    
    
    @unit.setter
    def unit(self, value: range_model):
        error_proxy.check(value, range_model)
        self.__unit = value
    
