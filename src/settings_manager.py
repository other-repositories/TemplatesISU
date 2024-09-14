from  src.abstract_logic import abstract_logic
from  src.settings import settings

import json
import os

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings:settings = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
     

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting() 

    """
    Открыть, конвертировать и загрузить настройки,
    """

    def open_from_dict(self, dict_value):  
        try:
            fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

            for field in fields:
                keys = list(filter(lambda x: x == field, dict_value.keys()))
                if len(keys) != 0:
                    value = dict_value[field]

                    if not isinstance(value, list) and not isinstance(value, dict):
                        setattr(self.__settings, field, value)
        except Exception as ex :
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False

    def open(self, file_name:str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            if not os.path.isabs(self.__file_name):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                full_name = os.path.abspath(os.path.join(current_dir, self.__file_name))
            else:
                full_name = self.__file_name

            current_path_info = os.path.split(__file__)
            current_path = current_path_info[0]
            full_name = f"{current_path}{os.sep}{self.__file_name}"
            stream = open(full_name)
            data = json.load(stream)


            # Список полей от типа назначения    
            fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

            # Заполняем свойства 
            for field in fields:
                keys = list(filter(lambda x: x == field, data.keys()))
                if len(keys) != 0:
                    value = data[field]

                    # Если обычное свойство - заполняем.
                    if not isinstance(value, list) and not isinstance(value, dict):
                        setattr(self.__settings, field, value)

            return True
        except Exception as ex :
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False

    def convert(self, dict_value) -> settings:
        self.open_from_dict(dict_value)
        return self.__settings
    
    """
    Загруженные настройки
    """
    @property
    def current_settings(self) -> settings:
        return self.__settings
    
    """
    Набор настроек по умолчанию
    """
    def __default_setting(self) -> settings:
        _settings = settings()
        _settings.inn = "380080920202"
        _settings.organization_name = "Рога и копыта (default)"
        return _settings
    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)