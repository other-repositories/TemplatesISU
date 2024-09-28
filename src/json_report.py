from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference
from src.models.receipt_model import receipt_model

import json
import uuid

class json_report(abstract_report):

    _maps = {}
    def uuid_convertor(self, field, object: uuid.UUID):
        return {field:object.hex}
    def basic_convertor(self, field: str, object):
        return { field: object }
    def reference_convertor(self,field: str, object):
        factory = json_report({"temp": object})
        return factory.create("temp")

    def __init__(self, data = None) -> None:
        super().__init__(data)
        self._maps[int] = self.basic_convertor
        self._maps[float] = self.basic_convertor
        self._maps[str] = self.basic_convertor
        self._maps[bool] = self.basic_convertor
        self._maps[uuid.UUID] = self.uuid_convertor
        for  inheritor in abstract_reference.__subclasses__():
            self._maps[inheritor] = self.reference_convertor

    def create(self, storage_key: str):
        
        items = self.data[ storage_key ]

        result = self.__serialize_list("data", items)
        if result is not None:
            return result
        
        data = {}
        fields = abstract_reference.create_fields(items)

        for field in fields:
            attribute = getattr(items.__class__, field)
            if isinstance(attribute, property):
                value = getattr(items, field)
                dictionary =  self.__serialize_list(field, value)
                if dictionary is None:
                    dictionary = self.__serialize_item(field, value)
                    if len(dictionary) == 1:
                        data[field] =  dictionary[field]
                    else:
                        data[field] = dictionary       
                else: 
                    data[field] = dictionary

        result = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)  
        return result
      
    def __serialize_list(self, field: str,  source) -> list:
        error_proxy.check(field, str)
        if isinstance(source, list):
            result = []
            for item in source:
                result.append( self.__serialize_item( field,  item ))  

            return result
        
        if isinstance(source, dict):
            result = []
            for key,  value in source.items():
                result.append( self.__serialize_item( key, value  ))  
            return result
        
    def __serialize_item(self, field: str,  source):

        error_proxy.check(field, str)
        if source is None:
            return {field: None}
 
        if isinstance(source, (list, dict)):
            return self.__serialize_list(field, source)
        
        if type(source) not in self._maps.keys():
            raise operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}")

        convertor = self._maps[ type(source)]
        dictionary = convertor( field, source )
        
        return  dictionary            
        
        
        
    
    