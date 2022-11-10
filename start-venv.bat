@echo OFF
echo What is the input directory path ?:
set /p input_directory=
echo What is the output directory path ?:
set /p output_directory=

python src/udf/create_env_file.py %input_directory% %output_directory%

if not exist "%output_directory%"  mkdir "%output_directory%"
if not exist "%output_directory%/errors"  mkdir "%output_directory%/errors"
if not exist "%output_directory%/errors/null"  mkdir "%output_directory%/errors/null"
if not exist "%output_directory%/errors/wrong"  mkdir "%output_directory%/errors/wrong"
if not exist "%output_directory%/DOAJ"  mkdir "%output_directory%/DOAJ"
if not exist "%output_directory%/OC"  mkdir "%output_directory%/OC"
if not exist "%output_directory%/OC/filtered"  mkdir "%output_directory%/OC/filtered"
if not exist "%output_directory%/OC/group_by_year"  mkdir "%output_directory%/OC/group_by_year"
if not exist "%output_directory%/OC/group_by_year/normal"  mkdir "%output_directory%/OC/group_by_year/normal"
if not exist "%output_directory%/OC/group_by_year/by_journal"  mkdir "%output_directory%/OC/group_by_year/by_journal"


venv\Scripts\activate


