#!/bin/bash

curl -X GET http://localhost:8001/api/report_types

curl -X POST http://localhost:8000/api/set_block_period \
     -d '{"period": "2024-12-31"}' \
     -H "Content-Type: application/json"
