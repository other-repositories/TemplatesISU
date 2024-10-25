from src.abstract_reference import abstract_reference
from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from src.models.nomenclature_model import nomenclature_model
from src.models.storage_model import storage_model
from src.models.range_model import range_model

#
# Модель складского оборота
#
class storage_row_turn_model(abstract_reference):
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
    
    def unit(self, value: range_model) -> range_model:
        error_proxy.check(value, range_model)
        self._unit = value
    
        
    def storage(self) -> storage_model:
        return self._storage
    
    def storage(self, value: storage_model) -> storage_model:
        error_proxy.check(value, storage_model)
        self._storage = value
        
    @staticmethod
    def create(nomenclature  : nomenclature_model, storage: storage_model, unit: range_model) -> abstract_reference:
        row = storage_row_turn_model("-")
        row.storage = storage
        row.unit = unit
        row.nomenclature = nomenclature
        
        return row 