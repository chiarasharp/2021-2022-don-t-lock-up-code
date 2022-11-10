@echo off
title OpenCitations-pipeline

python src/udf/read_env.py .env
cd run

::python -m filter_OC
python -m groupBy_run
python -m concat_run

cd ..
::venv\Scripts\deactivate.bat


