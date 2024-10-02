#from settings_manager import settings_manager
#
#s = settings_manager()
#print(s.convert({ "organization_name" : "123", "inn": "3466"}).__dict__)

from src.deserializer_json import json_deserializer
from src.models.receipt_model import receipt_model
from src.models.nomenclature_model import nomenclature_model
import json 
import pytest
import uuid
#
#def read_json_from_file(filename):
#    with open(filename, 'r', encoding='utf-8') as f:
#        return json.load(f)
#
#des = json_deserializer()
#receipt = des.deserialize(read_json_from_file("temp_data_task_4/test_2.json"), receipt_model)
#
#assert isinstance(receipt, receipt_model)
#assert receipt.full_desc == "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.Всыпьте муку, добавьте ванилин.Перемешайте массу венчиком до состояния гладкого однородного теста.Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно!Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке.Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."
#assert receipt.receipts_list[0].nomenclature.name == "Пшеничная мука"
#assert receipt.receipts_list[1].nomenclature.name == "Сахар"
#assert receipt.receipts_list[1].nomenclature.range.coefficient == 1000
#assert receipt.receipts_list[1].unit.name == "грамм"

def read_json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

des = json_deserializer()
receipt = des.deserialize(read_json_from_file("temp_data_task_4/test_1.json")[3], nomenclature_model)

assert isinstance(receipt, nomenclature_model)
assert receipt.full_name == ""
assert receipt.name == "Яйца"
assert receipt.nom_group.name == "Ингредиенты"
assert receipt.range.name == "штука"
assert receipt.range.coefficient == 1
