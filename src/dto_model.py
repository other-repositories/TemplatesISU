
from enum import Enum

class FilterType(Enum):
    EQUALS = "EQUALS" 
    LIKE = "LIKE"  

class FilterDTO:
    def __init__(self, filter_type: FilterType, name: str = None, unique_code: str = None):
        self.filter_type = filter_type 
        self.name = name 
        self.unique_code = unique_code  

from typing import List, Any
from typing import Any
import inspect

class FilterPrototype:
    def filter(self, data: List[Any], filter_dto: FilterDTO) -> List[Any]:
        return [
            item for item in data 
            if self.apply_recursive_filter(filter_dto, item)
        ]

    def apply_recursive_filter(self, filter_dto: FilterDTO, obj: Any) -> bool:
        if obj is None:
            return False

        # Проверка, является ли объект простым типом данных
        if isinstance(obj, (str, int, float, bool)):
            return self.apply_filter(filter_dto, str(obj))  # Преобразуем к строке для сравнения
        
        # Если объект - список или другой итерабельный объект, проверяем каждый элемент
        if isinstance(obj, (list, tuple, set)):
            return any(self.apply_recursive_filter(filter_dto, item) for item in obj)

        # Получаем все атрибуты объекта через рефлексию
        for attr_name, attr_value in inspect.getmembers(obj, lambda a: not(inspect.isroutine(a))):
            # Пропускаем встроенные атрибуты и защищенные поля
            if not attr_name.startswith('_'):
                if self.apply_recursive_filter(filter_dto, attr_value):
                    return True

        return False

    def apply_filter(self, filter_dto: FilterDTO, field: str) -> bool:
        if not field:
            return False

        if filter_dto.filter_type == FilterType.EQUALS:
            return field == filter_dto.name or field == filter_dto.unique_code
        elif filter_dto.filter_type == FilterType.LIKE:
            return (filter_dto.name and filter_dto.name in field) or \
                   (filter_dto.unique_code and filter_dto.unique_code in field)
        return False
