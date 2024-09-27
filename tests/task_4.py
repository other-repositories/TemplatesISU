import pytest
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json 

#def test_check_report_factory_create_json():
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#    
#    report = factory.create("json", start.get_storage().get_data())
#    
#    assert report is not None
#    print ( report.create("recipes") )
#    assert False
#
#
#def test_check_report_factory_create_csv():
#
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory( manager.current_settings )
#    
#    report = factory.create("csv", start.get_storage().get_data())
#    
#    assert report is not None
#    print ( report.create("recipes") )
#    assert False
#
#def test_check_report_factory_create_markdown():
#
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#
#    report = factory.create("markdown", start.get_storage().get_data())
#    
#    assert report is not None
#    print ( report.create("recipes") )
#    assert False
#
#def test_check_report_factory_create_xml():
#
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#
#    report = factory.create("xml", start.get_storage().get_data())
#
#    assert report is not None
#    print ( report.create("recipes") )
#    assert False
#
#def test_check_report_factory_create_rtf():
#
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#    # Действие
#    report = factory.create("rtf", start.get_storage().get_data())
#    
#    # Проверки
#    assert report is not None
#    print ( report.create("recipes") )
#    assert False
#
#
#def test_check_report_factory_create_csv_nom():
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#    # Действие
#    report = factory.create("csv", start.get_storage().get_data())
#    
#    # Проверки
#    assert report is not None
#    print ( report.create("nomenclatures") )
#    assert False
#
#def test_check_report_factory_create_xml_units():
#    manager = settings_manager()
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#    # Действие
#    report = factory.create("xml", start.get_storage().get_data())
#
#    # Проверки
#    assert report is not None
#    print ( report.create("units") )
#    assert False   
#
#def test_check_report_factory_create_markdown_groups():
#    manager = settings_manager()
#    manager.current_settings.report_mode = "markdown"
#    start = start_service( manager.current_settings )
#
#    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
#        start.create(json.load(file))
#
#    factory = report_factory(manager.current_settings)
#    
#    # Действие
#    report = factory.create(None, start.get_storage().get_data())
#
#    # Проверки
#    assert report is not None
#    print ( report.create("groups") )
#    assert False 
#

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

def common_test_json(format, type, name_file):
    manager = settings_manager()
    manager.current_settings.report_mode = format
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create(type)
    with open(name_file, 'w' , encoding='utf-8') as f:
        f.write("[")
        for elem in data:
            parsed_data = json.loads(elem)
            corrected_data = prepare_json_out(parsed_data)   
            f.write(json.dumps(corrected_data, ensure_ascii=False, indent=4))
            f.write(",")
        f.write("]")
    assert False

def common_test_xml(format, type, name_file):
    manager = settings_manager()
    manager.current_settings.report_mode = format
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    data = report.create(type)
    with open(name_file, 'w' , encoding='utf-8') as f:
        f.write("[")
        for elem in data:
            f.write(data)
        f.write("]")
    assert False
   
def test_check_report_factory_create_1():
    common_test_json("json","nomenclatures","temp_data_task_4/test_1.json")

def test_check_report_factory_create_2():
    common_test_json("json","recipes","temp_data_task_4/test_2.json")