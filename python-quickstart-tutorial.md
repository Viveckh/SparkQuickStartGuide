## Install Python
Ensure its installation path is included in environment variables

## Install Pip
Download the get-pip.py script and run `python get-pip.py install`

## Install virtualenv: 
`pip install virtualenv`

## Go to project directory and set up a virtual environment for the project
`virtualenv .env`

## To select this virtualenv as the interpreter in VS Code
`Ctrl+Shift+P`
Select the 'Select Interpreter" option and select the local virtualenv which should be listed (as long as it is named .env, VS Code should pick it up. Otherwise try restarting VS Code) 

## Activate the virtual env to install dependencies for the project and work on the environment
`".env/Scripts/activate"` (Quotes are necessary)

## To install any packages
`pip install packagename`

## To export list of dependencies installed in the current virtual environment
`pip freeze > requirements.txt`

## To install all packages mentioned in requirements.txt
`pip install -r requirements.txt`

## To deactivate the environment at any time
`deactivate`

