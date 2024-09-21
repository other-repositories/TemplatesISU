from  src.abstract_reference import abstract_reference
from  src.models.range_model import range_model
from  src.models.nom_group_model import nom_group_model
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

class nomenclature_model(abstract_reference):
    _nom_group = None
    _range = None
    _full_name = None
    
    def __init__(self, full_name:str = None, name:str = None, nom_group: abstract_reference = None, range: abstract_reference = None):
        if nom_group is not None:
            self.nom_group = nom_group
        if range is not None:    
            self.range = range
        if full_name is not None:
            self.full_name = full_name
        super().__init__(name)
    
    @property
    def nom_group(self) -> nom_group_model:
        return self._nom_group
    
    @nom_group.setter
    def nom_group(self, value: abstract_reference):
        error_proxy.check(value, abstract_reference)
        self._nom_group = value    
    
    @property
    def range(self) -> range_model:
        return self._range
    
    @range.setter
    def range(self, value: abstract_reference):
        error_proxy.check(value, abstract_reference)
        self._range = value

    @property
    def full_name(self) -> str:
        return self._full_name
    
    @full_name.setter
    def full_name(self, value: str):
        error_proxy.check(value.strip(), str, 255)
        self._full_name = value

    @staticmethod
    def get(nomenclature_name: str, nomenclatures: dict):
        error_proxy.check(nomenclature_name, str)
        
        keys = list(filter(lambda x: x == nomenclature_name, nomenclatures.keys() ))

        if len(keys) == 0:
            raise operation_exception(f"Inncorect list {nomenclature_name}!")
                
        return nomenclatures[keys[0]]