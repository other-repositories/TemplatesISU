from src.abstract_report import abstract_report
from src.markdown_report import markdown_report
from src.csv_report import csv_report
from src.json_report import json_report
from src.xml_report import xml_report
from src.rtf_report import rtf_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception

#
# Фабрика для отчетов
#
class report_factory:
    __maps = {}
    
    def __init__(self) -> None:
       self.__build_structure()

    def __build_structure(self):
        self.__maps["csv"]  = csv_report
        self.__maps["markdown"] = markdown_report
        self.__maps["json"] = json_report #xml alternative
        self.__maps["xml"] = xml_report
        self.__maps["rtf"] = rtf_report
      
    def create(self, format: str, data:dict) -> abstract_report:
        error_proxy.check(format, str)
        error_proxy.check(data, dict)
        
        if len(data) == 0:
            raise argument_exception("Empty data")
        
        if format not in self.__maps.keys():
            raise operation_exception(f"No impl") 
        
        # Получаем тип связанный с форматом
        report_type = self.__maps[format]
        # Получаем объект 
        result = report_type(data)
        
        return result 