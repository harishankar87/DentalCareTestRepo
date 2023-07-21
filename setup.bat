@echo off

REM Check if Python is installed
python --version
IF %ERRORLEVEL% NEQ 0 (
    REM Python is not installed, so install it
    REM Download Python installer
    curl -o "%USERPROFILE%\Downloads\python_installer.msi" https://www.python.org/ftp/python/<python-version>/python-<python-version>-amd64.exe
    
    REM Wait until the download is complete
    :wait_for_python_download
    timeout /t 1 >nul
    IF NOT EXIST "%USERPROFILE%\Downloads\python_installer.msi" (
        goto wait_for_python_download
    )
    
    REM Install Python
    "%USERPROFILE%\Downloads\python_installer.msi" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)
PAUSE
REM Check if pip is installed
pip --version
IF %ERRORLEVEL% NEQ 0 (
    REM Pip is not installed, so install it
    REM Download get-pip.py
    curl -o "%USERPROFILE%\Downloads\get-pip.py" https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    
    REM Install pip
    python "%USERPROFILE%\Downloads\get-pip.py" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)
PAUSE
REM Check if Git is installed
git --version
IF %ERRORLEVEL% NEQ 0 (
    REM Git is not installed, so install it
    REM Download Git installer
    curl -o "%USERPROFILE%\Downloads\git.exe" https://github.com/git-for-windows/git.git
    
    REM Install Git
    "%USERPROFILE%\Downloads\git.exe" /SILENT
)
PAUSE
REM CREATE FOLDER
echo creating folder 'Dental-Software'...
@REM  IF NOT EXIST "C:\Dental-Software"(
mkdir C:\Dental-Software
echo 'Dental-Software' folder created...
PAUSE
cd C:\Dental-Software
echo Entered into 'D:/Dental-Software'...
PAUSE
REM Clone the repository
echo Cloning the requested repository...
git clone https://github.com/Adhithya-Pinghley/DentalCareTestRepo.git %/Dental-Software%
echo cloning complete...
PAUSE
REM Create a virtual environment
python -m venv .venv
PAUSE
echo Virtual environment created...
REM Activate the virtual environment
env\Scripts\activate.bat
workon .venv
PAUSE
echo working on virtual environment
REM Install dependencies
pip install -r requirements.txt
PAUSE

REM Configure the database
REM Update the database settings in settings.py as needed

REM Run database migrations
python manage.py migrate
PAUSE
REM Collect static files (if applicable)
python manage.py collectstatic --noinput
PAUSE
REM Start the Django development server
python manage.py runserver
PAUSE