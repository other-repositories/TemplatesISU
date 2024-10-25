from  src.abstract_reference import abstract_reference
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

from random import randrange

from src.models.storage_model import storage_model
from src.models.storage_row_turn_model import storage_row_turn_model
#from src.storage import storage
from datetime import datetime, timedelta
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model

#
# Модель складской проводки
#
class storage_row_model(abstract_reference):
    # Тип складской проводки
    _storage_type: bool = False
    # Период
    _period : datetime
     # Номенклатура
    _nomenclature: nomenclature_model = None
    # Склад
    _storage: storage_model = None
    # Единица измерений
    _unit: range_model = None
    # Значение
    _value: float = 0
    
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float) -> float:
        error_proxy.check(value, (float, int))
        if value <= 0:
            raise argument_exception("Некорректно переданы параметры!")
        
        self._value = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self._nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model) -> nomenclature_model:
        error_proxy.check(value, nomenclature_model)
        self._nomenclature = value
        
    
    @property    
    def unit(self) -> range_model:
        return self._unit
    
    @unit.setter
    def unit(self, value: range_model) -> range_model:
        error_proxy.check(value, range_model)
        self._unit = value
    
    @property    
    def storage(self) -> storage_model:
        return self._storage
    
    @storage.setter
    def storage(self, value: storage_model) -> storage_model:
        error_proxy.check(value, storage_model)
        self._storage = value
    
    @property
    def storage_type(self) -> bool:
        return self._storage_type
    
    @storage_type.setter
    def storage_type(self, value) -> bool:
        if isinstance(value, int):
            self._storage_type = True if value > 0 else False
            
        elif isinstance(value, bool):
            self._storage_type = value
            
        else:
            raise argument_exception("Некорректно переданы параметры!")
        
    @property    
    def period(self) -> datetime:
        return self._period
    
    @period.setter
    def period(self, value: datetime) -> datetime:            
        error_proxy.check(value, datetime)
        self._period = value
        
    # Фабричные методы    
        
    @staticmethod    
    def create_credit_row(nomenclature_name: str, quantity, unit_name: str, data: dict, _storage: storage_model) -> abstract_reference:
        error_proxy.check(nomenclature_name, str)
        error_proxy.check(_storage, storage_model)
        error_proxy.check(quantity, (int, float))
        error_proxy.check(unit_name, str)
        
        
        # Определим номенклатуру
        items = data[ "nomenclatures" ]    
        nomenclatures = abstract_reference.transform_to_dict(items)
        nomenclature = nomenclature_model.get( nomenclature_name, nomenclatures)

        # Определяем единицу измерения
        items = data[ "units" ]
        units = abstract_reference.transform_to_dict(items)
        unit = range_model.get(unit_name, units )
        
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-02-01", "%Y-%m-%d")

        # Создаем транзакцию
        item = storage_row_model("sample_credit_transaction")
        item.nomenclature = nomenclature
        item.unit = unit
        item.storage_type = True
        item.value = quantity
        item.storage = _storage
        item.period = storage_row_model.random_date(start_date, stop_date)
        
        return item
    
    @staticmethod
    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)
            
        
    
    
    
