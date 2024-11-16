
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
from src.chain.storage_service import storage_service
import time

def save_data():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    code = start.get_storage().get_data()["nomenclatures"][0].unique_code
    start.get_storage().save()
    start.get_storage().load()
    assert code == start.get_storage().get_data()["nomenclatures"][0].unique_code
                