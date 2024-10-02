from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference
from src.models.receipt_model import receipt_model
from src.models.receipt_model_unit import receipt_model_unit

import numpy
import json
import uuid

class json_deserializer:

    def __init__(self):
        self._maps = {}
        # Добавляем маппинг для базовых типов данных
        self._maps[int] = self.basic_deserialize
        self._maps[float] = self.basic_deserialize
        self._maps[str] = self.basic_deserialize
        self._maps[bool] = self.basic_deserialize
        self._maps[uuid.UUID] = self.uuid_deserialize
        
        # Добавляем маппинг для всех наследников abstract_reference
        for inheritor in abstract_reference.__subclasses__():
            self._maps[inheritor] = self.reference_deserialize

    def basic_deserialize(self, field, value):
        return value

    def uuid_deserialize(self, field, value):
        return str(uuid.UUID(value))
    
    def reference_deserialize(self, field, value, model_class=None):
        # Для вложенных объектов создаем новый объект модели и заполняем его поля
        if model_class is None:
            model_class = self._get_reference_class(field)
        return self.deserialize_model(model_class, value)

    def deserialize(self, json_data, model_type):
        # Десериализация JSON-строки
        ##data = json.loads(json_data)
        
        return self.deserialize_model(model_type, json_data)

    def deserialize_model(self, model_class, data: dict):
        model_instance = model_class()
        fields = abstract_reference.create_fields(model_instance)
        
        for field in fields:
            if field in data:
                value = data[field]
                attribute = getattr(model_instance.__class__, field)
                if isinstance(attribute, property):
                    deserialized_value = self._deserialize_field(field, value, attribute,model_instance)
                    if deserialized_value is not None:
                        setattr(model_instance, field, deserialized_value)
        
        return model_instance

    def _deserialize_field(self, field: str, value, attribute,model_instance):
        # Если поле является списком
        if isinstance(value, list):
            if(field == "receipts_list"):
                element_type = receipt_model_unit
                return [self.reference_deserialize(field, v, element_type) for v in value]
        
        # Если поле — это вложенный объект
        elif isinstance(value, dict):
            reference_class = self._get_reference_class(field)
            return self.deserialize_model(reference_class, value)
        
        # Для простых типов данных
        field_type = type(getattr(attribute, 'fget', lambda: None)(model_instance))
        if field_type in self._maps:
            deserializer = self._maps[field_type]
            return deserializer(field, value)
        else:
            return None
            #raise operation_exception(f"Не удалось десериализовать поле {field} с типом {type(value)}")

    def _get_reference_class(self, field: str):
        # Получаем соответствующий класс модели по имени поля
        for inheritor in abstract_reference.__subclasses__():
            if inheritor.__name__.lower() == 'range_model' and field.lower() == 'base_range' or field.lower() == 'unit':
                return inheritor
            if inheritor.__name__.lower().replace('_model','') == field.lower():
                return inheritor
            if inheritor.__name__.lower() == field.lower():
                return inheritor
        raise argument_exception(f"Класс для поля {field} не найден")
    
    def _get_list_element_type(self, attribute):
        # Определение типа элементов списка (моделей)
        return attribute.fget.__annotations__['return'].__args__[0]