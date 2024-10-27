from  src.abstract_reference import abstract_reference
from  src.errors.error_utils import error_proxy, argument_exception, operation_exception
#
# Модель склада
#
class storage_model(abstract_reference):
    _address: str = ""
    
    @property
    def address(self) -> str:
        """
            Адрес

        Returns:
            _type_: _description_
        """
        return self._address
    
    @address.setter
    def address(self, value:str):
        """
            Адрес
        Args:
            value (str): _description_
        """
        error_proxy.check(value, str)
        self._address = value
        
         
    def load(self, source: dict):
        """
            Десериализовать свойства 
        Args:
            source (dict): исходный слова
        """
        if source is None:
            return None
        super().load(source)
        
        source_fields = ["address"]
        if set(source_fields).issubset(list(source.keys())) == False:
            raise operation_exception(f"Невозможно загрузить данные в объект {source}!")
        
        self._address = source["address"]
        return self
        
    # Фабричные методы
        
    @staticmethod    
    def create_default() -> abstract_reference:
        """
            Сформировать склад по умолчанию
        Returns:
            reference: _description_
        """
        storage = storage_model("default")
        storage.address = "г. Москва. ул. Тестовая д. 7"
        
        return storage    
   