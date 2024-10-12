# Пример вложенной модели

from src.deserializer_json import json_deserializer
from src.models.receipt_model import receipt_model
from src.models.nomenclature_model import nomenclature_model
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
from src.models.nom_group_model import nom_group_model
from src.models.range_model import range_model
import json 
import uuid

from src.dto_model import FilterDTO, FilterPrototype, FilterType

class BaseUnit:
    def __init__(self, name: str):
        self.name = name

class Unit:
    def __init__(self, name: str, unique_code: str, base_unit: BaseUnit):
        self.name = name
        self.unique_code = unique_code
        self.base_unit = base_unit  

unit_data = [
    Unit(name="Kilogram", unique_code="001", base_unit=BaseUnit("Gram")),
    Unit(name="Meter", unique_code="002", base_unit=BaseUnit("Centimeter")),
    Unit(name="Liter", unique_code="003", base_unit=BaseUnit("Milliliter")),
]

def read_json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def common_test(type_conv, model_type, is_full_list):
    manager = settings_manager()
    manager.current_settings.report_mode = "csv"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create(type_conv)

    filter_dto = FilterDTO(filter_type=FilterType.LIKE, name="ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ")

    # Применяем фильтр
    filter_prototype = FilterPrototype()
    if(isinstance(data, (list))):
        filtered_units = filter_prototype.filter(data, filter_dto)
    else:
        filtered_units = filter_prototype.filter([data], filter_dto)

    # Вывод результатов
    for unit in filtered_units:
        print(unit)

def test_nomenclatures_2():
    common_test("recipes", receipt_model, False)

test_nomenclatures_2()