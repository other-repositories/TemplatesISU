#!/bin/bash

python3 -m venv .venv

. .venv/bin/activate

pip install --upgrade pip

pip install typing-extensions --upgrade
pip install -U connexion[flask]
pip install -U connexion[swagger-ui]
pip install -U connexion[uvicorn]
pip install -U flask-restplus
pip install -U Flask
pip install flasgger
pip install pytest
pip install numpy
pip install uuid

echo "Все зависимости установлены!"
