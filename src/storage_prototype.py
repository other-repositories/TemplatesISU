from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from datetime import datetime
from src.models.nomenclature_model import nomenclature_model
import uuid

class storage_prototype(error_proxy):
    __data = []
    
    def __init__(self, data: list) -> None:
        if len(data) <= 0:
            self.error = "Набор данных пуст!"
        
        error_proxy.check(data, list)
        self.__data = data
        self.clear()


    def filter_by_period( self,start_period: datetime, stop_period: datetime  ):
        self.clear()
        
        error_proxy.check(start_period, datetime)
        error_proxy.check(stop_period, datetime)
        if len(self.__data) <= 0:
            self.error = "Некорректно переданы параметры!"
            
        if start_period > stop_period:
            self.error = "Некорректный период!"
            
         
        if not self.is_empty:
            return self.__data
        
        result = []
        for item in self.__data:
            if item.period > start_period and item.period <= stop_period:
                result.append(item)
                
        return   storage_prototype( result )
    
    def filter_by_nomenclature(self, nomenclature:  nomenclature_model):
        self.clear()
        
        error_proxy.check(nomenclature, nomenclature_model)
        
        result = []
        for item in self.__data:
            if item.nomenclature.unique_code == nomenclature.unique_code:
                result.append(item)
                
        return   storage_prototype( result )
        
    def filter_by_id(self, id: str):
        self.clear()
        
        error_proxy.check(id, str)
        
        result = []
        for item in self.__data:
            if item.id == id:
                result.append(item)
                
        return   storage_prototype( result )

    @property
    def data(self):
        return self.__data         
                
    @data.setter            
    def data(self, value: list):
        error_proxy.check(value, list)
        self.__data = value            