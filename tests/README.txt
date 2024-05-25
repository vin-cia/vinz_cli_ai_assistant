Steps to Set Up and Run Tests
---------

    Navigate to the Project Directory:

    Open your terminal and navigate to the root directory of the project:

    * cd /path/to/vinz-cli-ai-assistant


Create a Virtual Environment:
---------

Create a virtual environment in the project directory:

    * python3 -m venv venv


Activate the Virtual Environment:
---------

    On macOS and Linux:

    * source venv/bin/activate


Install Dependencies:
---------

With the virtual environment activated, install the required dependencies:

    * pip install pytest openai


Run the Tests:
---------

Use pytest to run the tests. Ensure you are in the root directory of the project:

    * pytest

Alternatively, you can set the PYTHONPATH to the current directory and run pytest:
    
    * PYTHONPATH=./ pytest
