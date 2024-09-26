from src.abstract_report import abstract_report
from src.markdown_report import markdown_report
from src.csv_report import csv_report
from src.json_report import json_report
from src.xml_report import xml_report
from src.rtf_report import rtf_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.settings import ConvertTypes
#
# Фабрика для отчетов
#
class report_factory:
    __maps = {}
    __format_default = "csv"

    def __init__(self, format = None) -> None:
       self.__build_structure()
       if format is not None:
            self.__format_default = format

    def __build_structure(self):
        self.__maps[ConvertTypes.CSV.value]  = csv_report
        self.__maps[ConvertTypes.MD.value] = markdown_report
        self.__maps[ConvertTypes.JSON.value] = json_report #xml alternative
        self.__maps[ConvertTypes.XML.value] = xml_report
        self.__maps[ConvertTypes.RTF.value] = rtf_report
      
    def create(self, format = None, data: str = None) -> abstract_report:
        if format is None: 
            format = self.__format_default

        error_proxy.check(format, str)
        error_proxy.check(data, dict)
        
        if len(data) == 0:
            raise argument_exception("Empty data")
       
        if format not in self.__maps.keys():
            raise operation_exception(f"No impl") 
        
        print(data)
        # Получаем тип связанный с форматом
        report_type = self.__maps[format]
        # Получаем объект 
        result = report_type(data)
        
        return result 