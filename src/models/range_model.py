from  src.abstract_reference import abstract_reference
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception

class range_model(abstract_reference):
    _base_range: abstract_reference = None
    _coefficient: int = 1
    
    def __init__(self, name: str = None, base: abstract_reference = None, coefficient: int = 1 ):
        #self._synonym_list = {'range_model' : ["unit", "base_range"]}
        if base is not None:
            self.base_range = base
        if coefficient is not None:
            self.coefficient = coefficient   

        super().__init__(name)
    
    @property
    def base_range(self) -> abstract_reference:
        return self._base_range

    
    @base_range.setter
    def base_range(self, value: abstract_reference ):
        error_proxy.check(value, abstract_reference)
        self._base_range = value
        
    
    @property    
    def coefficient(self) -> int:
        return self._coefficient
    
    @coefficient.setter
    def   coefficient(self, value:int):
        error_proxy.check(value, int)
        
        if(value <= 0):
            raise argument_exception("Coff >= 1!")
        
        self._coefficient = value  

    @staticmethod    
    def create_gram():
        item = range_model("грамм", None, 1)
        return item    
    
    @staticmethod
    def create_killogram():
        base = range_model.create_gram()
        item = range_model("киллограмм", base, 1000)
        return item

    @staticmethod
    def create_ting():
        return range_model("штука")
    
    @staticmethod
    def get(unit_name: str, units: dict):
        error_proxy.check(unit_name, str)
        
        keys = list(filter(lambda x: x == unit_name, units.keys() ))
        if len(keys) == 0:
            raise operation_exception(f"Некоректно передан список. Не найдена unit {unit_name}!")
                
        return units[keys[0]]
  