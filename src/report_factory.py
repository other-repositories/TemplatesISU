from src.abstract_report import abstract_report
from src.markdown_report import markdown_report
from src.csv_report import csv_report
from src.json_report import json_report
from src.xml_report import xml_report
from src.rtf_report import rtf_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.settings import settings
#
# Фабрика для отчетов
#
class report_factory:
    __maps = {}
    __format_default = "csv"
    __settings: settings = None

    def __init__(self, sett: settings) -> None:
       self.__settings = sett
      
    def create(self, format = None, data: str = None) -> abstract_report:
        if format is None: 
            if self.__settings is None:
               raise argument_exception("format or report_mode in settings must be not None")
            format = self.__settings.report_mode

        error_proxy.check(format, str)
        error_proxy.check(data, dict)
        
        if len(data) == 0:
            raise argument_exception("Empty data")
       
        #if format not in self.__maps.keys():
        #    raise operation_exception(f"No impl") 
        # Получаем тип связанный с форматом
        report_type = self.__settings.get_convert_types()[format]
        # Получаем объект 
        result = report_type(data)
        
        return result 