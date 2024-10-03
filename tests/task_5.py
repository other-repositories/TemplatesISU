from src.deserializer_json import json_deserializer
from src.models.receipt_model import receipt_model
from src.models.nomenclature_model import nomenclature_model
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
from src.models.nom_group_model import nom_group_model
from src.models.range_model import range_model
import json 
import pytest
import uuid
from deepdiff import DeepDiff

def  prepare_json_out(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    nested_value = json.loads(value)
                    data[key] = prepare_json_out(nested_value)
                except json.JSONDecodeError:
                    pass
            elif isinstance(value, dict) or isinstance(value, list):
                data[key] = prepare_json_out(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str):
                try:
                    nested_value = json.loads(data[i])
                    data[i] = prepare_json_out(nested_value)
                except json.JSONDecodeError:
                    pass
            elif isinstance(data[i], dict) or isinstance(data[i], list):
                data[i] = prepare_json_out(data[i])
    
    return data

def read_json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_receipts():
    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/test_2.json"), receipt_model)

    assert isinstance(receipt, receipt_model)
    assert receipt.full_desc == "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.Всыпьте муку, добавьте ванилин.Перемешайте массу венчиком до состояния гладкого однородного теста.Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно!Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке.Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."
    assert receipt.receipts_list[0].nomenclature.name == "Пшеничная мука"
    assert receipt.receipts_list[1].nomenclature.name == "Сахар"
    assert receipt.receipts_list[1].nomenclature.range.coefficient == 1000
    assert receipt.receipts_list[1].unit.name == "грамм"

def test_nomenclatures_1():
    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/test_1.json")[3], nomenclature_model)

    assert isinstance(receipt, nomenclature_model)
    assert receipt.full_name == ""
    assert receipt.name == "Яйца"
    assert receipt.nom_group.name == "Ингредиенты"
    assert receipt.range.name == "штука"
    assert receipt.range.coefficient == 1

def test_nomenclatures_2():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create("nomenclatures")
    with open('temp_data_task_4/temp.json', 'w' , encoding='utf-8') as f:
        f.write("[")
        i = 0
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            if (i != len(data)-1):
                i+=1
                f.write(",")
        f.write("]")

    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/temp.json")[3], nomenclature_model)

    diff = DeepDiff(receipt, start.get_storage().get_data()['nomenclatures'][3])
    assert(diff == {})

def test_receipts_2():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create("recipes")
    with open('temp_data_task_4/temp.json', 'w' , encoding='utf-8') as f:
        f.write("[")
        i = 0
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            if (i != len(data)-1):
                i+=1
                f.write(",")
        f.write("]")

    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/temp.json")[0], receipt_model)
    diff = DeepDiff(receipt, start.get_storage().get_data()['recipes'][0])
    assert(diff == {})

def test_nom_group():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create("groups")
    with open('temp_data_task_4/temp.json', 'w' , encoding='utf-8') as f:
        f.write("[")
        i = 0
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            if (i != len(data)-1):
                i+=1
                f.write(",")
        f.write("]")

    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/temp.json")[0], nom_group_model)
    diff = DeepDiff(receipt, start.get_storage().get_data()['groups'][0])
    assert(diff == {})

def test_units():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create("units")
    with open('temp_data_task_4/temp.json', 'w' , encoding='utf-8') as f:
        f.write("[")
        i = 0
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            if (i != len(data)-1):
                i+=1
                f.write(",")
        f.write("]")

    des = json_deserializer()
    receipt = des.deserialize(read_json_from_file("temp_data_task_4/temp.json")[0], range_model)
    diff = DeepDiff(receipt, start.get_storage().get_data()['units'][0])
    assert(diff == {})
