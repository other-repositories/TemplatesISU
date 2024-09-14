# test_models.py
import pytest
from src.abstract_reference import abstract_reference
from src.errors.error_utils import argument_exception
from src.models.company_model import company_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.nom_group_model import nom_group_model
from src.models.storage_model import storage_model
from src.settings import settings

def test_company_model_valid():
    sett = settings()
    company = company_model(name="Test Company", sett=sett, bill="1234567890")
    assert company.inn == "0" * 12
    assert company.bik == "0" * 9
    assert company.bill == "1234567890"
    assert company.ownership_type == "0" * 5

def test_company_model_invalid_inn():
    sett = settings()
    with pytest.raises(argument_exception):
        company = company_model(name="Test Company", sett=sett, bill="1234567890")
        company.inn = "12345"

def test_company_model_invalid_bik():
    sett = settings()
    with pytest.raises(argument_exception):
        company = company_model(name="Test Company", sett=sett, bill="1234567890")
        company.bik = "12345678"

def test_company_model_invalid_ownership_type():
    sett = settings()
    with pytest.raises(argument_exception):
        company = company_model(name="Test Company", sett=sett, bill="1234567890")
        company.ownership_type = "1234"

def test_settings_valid():
    sett = settings()
    assert sett.inn == "0" * 12
    assert sett.account_number == "0" * 11
    assert sett.correspondent_account == "0" * 11
    assert sett.bik == "0" * 9
    assert sett.ownership_type == "0" * 5

def test_settings_invalid_inn():
    sett = settings()
    with pytest.raises(argument_exception):
        sett.inn = "12345"

def test_settings_invalid_account_number():
    sett = settings()
    with pytest.raises(argument_exception):
        sett.account_number = "123456789"

def test_nomenclature_model_valid():
    nom_group = nom_group_model(name="Nom Group")
    range = range_model(name="Range")
    nomenclature = nomenclature_model(full_name="Full Name", name="Nomenclature", nom_group=nom_group, range=range)
    assert nomenclature.full_name == "Full Name"
    assert nomenclature.nom_group == nom_group
    assert nomenclature.range == range

def test_nomenclature_model_invalid_nom_group():
    with pytest.raises(argument_exception):
        nomenclature = nomenclature_model(full_name="Full Name", name="Nomenclature", nom_group="Invalid Group")

def test_nomenclature_model_invalid_range():
    with pytest.raises(argument_exception):
        nomenclature = nomenclature_model(full_name="Full Name", name="Nomenclature", range="Invalid Range")

def test_range_model_create_gram():
    item = range_model.create_gram()
    assert item.name == "грамм"
    assert item.base_range is None
    assert item.coefficient == 1

def test_range_model_create_kilogram():
    item = range_model.create_killogram()
    assert item.name == "киллограмм"
    assert item.base_range.name == "грамм"
    assert item.coefficient == 1000

def test_range_model_invalid_coefficient():
    with pytest.raises(argument_exception):
        item = range_model(name="Test", coefficient=0)

def test_nom_group_model_valid():
    nom_group = nom_group_model(name="Nom Group")
    assert nom_group.name == "Nom Group"

def test_storage_model_valid():
    storage = storage_model(name="Storage")
    assert storage.name == "Storage"
