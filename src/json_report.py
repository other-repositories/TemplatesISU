from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference

import json

#
# Формирование отчета в формате json
#
class json_report(abstract_report):
    
    def create(self, storage_key: str):
        super().create(storage_key)
        
         # Исходные данные
        items = self.data[ storage_key ]
        if items == None:
            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")
        
        if len(items) == 0:
            raise operation_exception("Невозможно сформировать данные. Нет данных!")
        

        # Сконвертируем данные как список
        result = self.__serialize_list("data", object)
        if result is not None:
            return result
        
        # Сконвертируем данные как значение
        data = {}
        fields = abstract_reference.create_fields(object)
        
        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)
                
                # Сконвертируем данные как список
                dictionary =  self.__serialize_list(field, value)
                if dictionary is None:
                    # Сконвертируем данные как значение
                    dictionary = self.__serialize_item(field, value)
                    
                try:    
                    if len(dictionary) == 1:
                        # Обычное поле
                        data[field] =  dictionary[field]
                    else:
                        # Вложенный словарь
                        data[field] = dictionary    
                except:
                    raise operation_exception(f"Невозможно сериализовать объект в набор словарей. Поле {field}, значение: {dictionary}")            
        
        # Формируем Json
        result = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)  
        return result
      
    def __serialize_list(self, field: str,  source) -> list:
        """
            Сконвертировать список
        Args:
            source (_type_): _description_

        Returns:
            dict: _description_
        """
        error_proxy.check(field, str)
        
        # Сконвертировать список
        if isinstance(source, list):
            result = []
            for item in source:
                result.append( self.__serialize_item( field,  item ))  
            
            return result 
                
        
        
        
    
    