#!/bin/bash

# Install Python dependencies
pip install -r .devcontainer/requirements.txt

python schema.py
python train.py
python app.py

