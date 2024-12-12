# Welcome to Audio Looping Station

## Setup Environment (Mac/Linux)
To setup the python virtual environment for Audio Looping Station, follow the 
following steps
1. Clone the repository `git clone <repo>`
2. Navigate to project root directory
3. Allow execution of setup_env.sh `chmod +x ./setup_env.sh`
4. Enter the following bash command (must be in a shell capable of bash commands): `./setup_env.sh`
5. Activate the virtual environment `. .venv/bin/activate`
6. Now you should see (loop-station) on the LHS of your command line prompt indicating
   that you are ready to begin working in the project

## Setup Environment (Windows)
To setup the python virtual environment for Audio Looping Station, follow the 
following steps:
1. Make sure you have Python 3.9 or 3.10. Some packages don't work for the higher versions. The
following setup was tested on Python 3.9.13
3. Clone the repository `git clone <repo>`
4. Navigate to project root directory `cd AudioLoopStation`
5. Create virtual environment folder `python -m venv .venv`
6. Activate virtual environment `.venv\Scripts\activate`
7. Install required packages `pip install -r requirements.txt`
8. Navigate to the location of controller.py file `cd AudioLoopStation`. Note that if you run the project 
from a different directory, it may fail. 
9. Start the app `python controller.py`

### Updating installed modules
If you need to install a new module/package, follow the following steps to ensure that everyone is
working with the same environment
1. Install the package `pip install <package name>`
2. Update requirements.txt `pip freeze > requirements.txt`
3. Make sure to include the new requirements.txt when you submit your next PR