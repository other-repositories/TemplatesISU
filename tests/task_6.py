
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json 
import pytest
import uuid
from src.common import common  
from datetime import datetime
from src.errors.error_utils import error_proxy, argument_exception, operation_exception

from src.process_factory import process_factory
from src.storage_prototype import storage_prototype
from src.models.storage_row_turn_model import storage_row_turn_model
from src.models.storage_model import storage_model
from src.models.range_model import range_model as unit_model

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

def test_check_serialize_transaction():
        manager = settings_manager()
        manager.current_settings.report_mode = "json"
        start = start_service( manager.current_settings )

        with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))

        factory = report_factory(manager.current_settings)

        report = factory.create(None, start.get_storage().get_data())

        assert report is not None
        data = report.create("storage_row_model")
        with open("temp_data_task_4/storage_row_model_test.json", 'w' , encoding='utf-8') as f:
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

def test_check_filter_by_period():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))
        
    data = start.get_storage().get_data()["storage_row_model"]
    
    start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")
    prototype = storage_prototype(data)
    
    result = prototype.filter_by_period( start_date, stop_date ) 
    
    factory = report_factory(manager.current_settings)
    out = json.loads(factory.create(None, {"storage_row_model" : result.data[0]}).create("storage_row_model"))

    assert isinstance(result, storage_prototype)
    assert prototype.is_empty == True
    assert len(result.data) > 0
    assert out["name"] == "sample_credit_transaction"
        
def test_check_filter_by_nomenclature():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))
        
    data = start.get_storage().get_data()["storage_row_model"]
    
    element = data[0]
    nomenclature = element.nomenclature
    prototype = storage_prototype( data)
    
    result = prototype.filter_by_nomenclature( nomenclature )

    assert isinstance(result, storage_prototype)
    assert prototype.is_empty == True   
    assert len(result.data) > 0           


def test_check_process_factory():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))
    factory = process_factory()

    result = factory.create( process_factory.turn_key() )
    assert result is not None
     
def test_check_process_turns():
    # Подготовка
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))
    factory = process_factory()
    key = "storage_row_model"
    transactions = start.get_storage().get_data()["storage_row_model"]
    processing = factory.create( process_factory.turn_key() )
    
    result = processing().process(transactions)
    
    assert result is not None
    assert len(result) > 0   
    turn = list(filter(lambda x: x.nomenclature.name == "Сыр Пармезан", result ))
    assert turn[0].value == 0.2
    
def test_check_aggregate_turns():
    # Подготовка
    default_storage = storage_model.create_default()
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))

    nomenclatures = start.get_storage().get_data()["nomenclatures"]
    if len(nomenclatures) == 0:
        raise operation_exception("Список номенклатуры пуст!")
    
    #   Создаем тестовый оборот и добавляем его в хранилище
    turn = storage_row_turn_model()
    turn.nomenclature = nomenclatures[0]
    turn.storage = default_storage
    turn.unit = unit_model.create_killogram()
    turn.value = 1
    
    start.get_storage().get_data()[ "storage_row_turn_model"  ] = []
    start.get_storage().get_data()[ "storage_row_turn_model"  ].append( turn)
    
    factory = process_factory()
    aggregate_processing = factory.create( process_factory.aggregate_key() )
    turn_processing = factory.create( process_factory.turn_key() )
    calculated_turns = turn_processing().process( start.get_storage().get_data()[ "storage_row_model"  ]    )   
    calculated_len = len(calculated_turns) 
    
    # Действие
    result = aggregate_processing().process( calculated_turns  )
    # Проверки
    assert result is not None    
    assert calculated_len == len(result)
               