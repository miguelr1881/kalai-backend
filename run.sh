#!/bin/bash
cd "$(dirname "$0")"
PYTHONPATH=$PWD venv/bin/uvicorn main:app --reload --port 8000 --loop asyncio
