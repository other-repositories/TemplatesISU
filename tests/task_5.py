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
from src.common import common
import random

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

def common_test(type_conv, model_type, is_full_list):
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
    data = report.create(type_conv)
    with open('temp_data_task_4/temp.json', 'w' , encoding='utf-8') as f:
        f.write("[")
        i = 0
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = common.prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            if (i != len(data)-1):
                i+=1
                f.write(",")
        f.write("]")

    des = json_deserializer()
    data = read_json_from_file("temp_data_task_4/temp.json")

    if(not is_full_list):
        rand_data_index = random.randint(0, len(data)-1)
        receipt = des.deserialize(data[rand_data_index], model_type)
        diff = DeepDiff(receipt, start.get_storage().get_data()[type_conv][rand_data_index])
        assert(diff == {})
    else:
        for i in range(len(data)):
            receipt = des.deserialize(data[i], model_type)
            diff = DeepDiff(receipt, start.get_storage().get_data()[type_conv][i])
            assert(diff == {})

def test_nomenclatures_2():
    common_test("nomenclatures", nomenclature_model, False)

def test_receipts_2():
    common_test("recipes", receipt_model, False)

def test_nom_group():
    common_test("groups", nom_group_model, False)

def test_units():
    common_test("units",range_model, False)

def test_nomenclatures_2_full_list():
    common_test("nomenclatures", nomenclature_model, True)

def test_receipts_2_full_lis():
    common_test("recipes", receipt_model, True)

def test_nom_group_full_lis():
    common_test("groups", nom_group_model, True)

def test_units_full_lis():
    common_test("units",range_model, True)