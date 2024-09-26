import pytest
from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json 

def test_check_report_factory_create_json():
    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "json"
    
    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())
    
    assert report is not None
    print ( report.create("recipes") )
    assert False


def test_check_report_factory_create_csv():

    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "csv"
    
    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())
    
    assert report is not None
    print ( report.create("recipes") )
    assert False

def test_check_report_factory_create_markdown():

    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "markdown"
    

    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())
    

    assert report is not None
    print ( report.create("recipes") )
    assert False

def test_check_report_factory_create_xml():

    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "xml"
    

    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())

    assert report is not None
    print ( report.create("recipes") )
    assert False

def test_check_report_factory_create_rtf():

    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "rtf"
    
    # Действие
    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())
    
    # Проверки
    assert report is not None
    print ( report.create("recipes") )
    assert False


def test_check_report_factory_create_csv_nom():
    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "csv"
    
    # Действие
    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())
    
    # Проверки
    assert report is not None
    print ( report.create("nomenclatures") )
    assert False

def test_check_report_factory_create_xml_units():
    manager = settings_manager()
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory()
    manager.current_settings.report_mode = "xml"
    
    # Действие
    report = factory.create(manager.current_settings.report_mode, 
                            start.get_storage().get_data())

    # Проверки
    assert report is not None
    print ( report.create("units") )
    assert False   

def test_check_report_factory_create_markdown_groups():
    manager = settings_manager()
    manager.current_settings.report_mode = "markdown"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    factory = report_factory(manager.current_settings.report_mode)
    
    # Действие
    report = factory.create(None, start.get_storage().get_data())

    # Проверки
    assert report is not None
    print ( report.create("groups") )
    assert False 