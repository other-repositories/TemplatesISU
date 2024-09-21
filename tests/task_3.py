import pytest
import json
from src.settings import settings
from src.errors.error_utils import argument_exception, operation_exception
from src.start_service import start_service
from src.storage import storage_repository
from contextlib import redirect_stdout
import io

@pytest.fixture
def service():
    options = settings()
    return start_service(options)


@pytest.fixture
def json_data():
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def test_create_units():
    units = start_service.create_units()
    assert len(units) == 3, "Должно быть создано 3 единицы измерения"


def test_create_nomenclatures():
    nomenclatures = start_service.create_nomenclatures()
    assert len(nomenclatures) > 0, "Номенклатура должна быть создана"


def test_create_receipt(service, json_data):
    name = json_data["title"]
    ingredients = [(ingredient["name"], int(ingredient["amount"].split()[0])) for ingredient in json_data["ingredients"]]
    extra = f"Время приготовления: {json_data['cooking_time']}"
    instructions = json_data["instructions"]

    nomenclatures = start_service.create_nomenclatures()
    
    receipt = start_service.create_receipt(name, ingredients, extra, instructions, nomenclatures)
    
    assert receipt._name == name, "Название рецепта должно совпадать"
    assert len(receipt.receipts_list()) == len(ingredients), "Количество ингредиентов должно совпадать"

def test_invalid_units(service, json_data):
    json_data["ingredients"][0]["name"] = "несуществующий рецепт!"
    with pytest.raises(operation_exception):
        service.create(json_data)


def test_empty_ingredients(service, json_data):
    json_data["ingredients"] = []
    with pytest.raises(argument_exception):
        service.create(json_data)

@pytest.fixture
def mock_storage():
    return storage_repository()

def test_create_receipt(mock_storage, capsys):
    service = start_service(None, mock_storage)

    receipt_dict = {
        "title": "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ",
        "ingredients": [
            {"name": "Пшеничная мука", "amount": "100 гр"},
            {"name": "Сахар", "amount": "80 гр"},
            {"name": "Сливочное масло", "amount": "70 гр"},
            {"name": "Яйца", "amount": "1 шт"},
            {"name": "Ванилин", "amount": "5 гр"}
        ],
        "cooking_time": "20 мин",
        "instructions": [
            "Подготовьте необходимые продукты.",
            "Растопите масло на маленьком огне.",
            "Добавьте сахар и перемешайте до полного растворения.",
            "Добавьте яйцо и перемешайте до однородности.",
            "Всыпьте муку и ванилин, перемешайте.",
            "Разогрейте вафельницу и выпекайте вафли до золотистого цвета."
        ]
    }
    
    service.create(receipt_dict)

    captured = capsys.readouterr()
    f = io.StringIO()
    with redirect_stdout(f):
        mock_storage.dump()

    output = f.getvalue()

    assert "Название: ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ" in output
    assert "Ингредиенты:" in output
    assert "  - Пшеничная мука: 100" in output
    assert "  - Сахар: 80" in output
    assert "  - Сливочное масло: 70" in output
    assert "  - Яйца: 1" in output
    assert "  - Ванилин: 5" in output
    assert "Время приготовления: 20 мин" in output
    assert "Подготовьте необходимые продукты." in output
    assert "Растопите масло на маленьком огне." in output
    assert "Добавьте сахар и перемешайте до полного растворения." in output
    assert "Добавьте яйцо и перемешайте до однородности." in output
    assert "Всыпьте муку и ванилин, перемешайте." in output
    assert "Разогрейте вафельницу и выпекайте вафли до золотистого цвета." in output