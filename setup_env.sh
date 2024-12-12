#!/bin/bash

python3 -m venv .venv --prompt loop-station
. .venv/bin/activate && \
  pip install -r requirements.txt
