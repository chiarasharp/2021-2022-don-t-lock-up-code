@echo OFF
if not exist .env (

python src/udf/create_env_and_directories.py

) else (

echo .env file already exist. If you want to recreate it, delete it

)


echo start the Virtual Environment...

