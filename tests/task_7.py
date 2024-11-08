
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

def test_check_create_turns():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service( manager.current_settings )
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))
        
    data = start.get_storage().get_data()["storage_row_model"]
    start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")

    transactions = start.get_storage().get_data()["storage_row_model"] 
    data = storage_service( transactions ).create_turns( start_date, stop_date )   

    assert len(data) > 0
  
def test_performance():
    manager = settings_manager()
    manager.current_settings.report_mode = "json"
    start = start_service(manager.current_settings)

    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        transaction_template = json.load(file)

    for _ in range(1000):
        start.create(transaction_template)

    transactions = start.get_storage().get_data()["storage_row_model"]

    lock_dates = [
        ("2024-01-01", "2024-01-10"),
        ("2024-01-05", "2024-01-15"),
        ("2024-01-10", "2024-01-20"),
    ]

    results = []

    for start_date_str, stop_date_str in lock_dates:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        stop_date = datetime.strptime(stop_date_str, "%Y-%m-%d")
        
        start_time = time.time()
        data = storage_service(transactions).create_turns(start_date, stop_date)
        end_time = time.time()

        elapsed_time = end_time - start_time
        results.append((start_date_str, stop_date_str, elapsed_time))

    with open("performance_results.md", "w") as f:
        f.write("| Start Date | Stop Date | Time (seconds) |\n")
        f.write("|------------|-----------|----------------|\n")
        for start_date, stop_date, time_taken in results:
            f.write(f"| {start_date} | {stop_date} | {time_taken:.4f} |\n")

    print("Тестирование завершено. Результаты сохранены в performance_results.md.")

        
    