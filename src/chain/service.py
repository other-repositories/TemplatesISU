from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from src.settings import settings
from src.settings_manager import settings_manager
from src.json_report import json_report

from abc import ABC
import json

class service(ABC):
    # Набор данных для работы
    __data = []
    # Текущие настройки
    __settings: settings = None
    
    def __init__(self, data: list = None) -> None:
        self.__data = data
        options = settings_manager()
        self.__settings = options.current_settings

    @property
    def data(self):
        return self.__data
    
    @property
    def settings(self) -> settings:
        return self.__settings
    

    
