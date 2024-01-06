=============================
Python Project Setup Guide
=============================

This guide provides instructions on setting up a Python virtual environment, installing dependencies, and setting up the project in editable mode.

Requirements
-------------

- Python 3.x
- pip (Python package manager)

Creating a Virtual Environment
------------------------------

First, create a new virtual environment for the project. This ensures that the project dependencies do not interfere with other Python projects or the global Python installation.

.. code-block:: bash

    python -m venv /path/to/new/virtual/environment

Replace `/path/to/new/virtual/environment` with your desired directory.

Activating the Virtual Environment
----------------------------------

Activate the virtual environment. The activation command varies depending on your operating system.

**On Windows:**

.. code-block:: bash

    /path/to/new/virtual/environment/Scripts/activate.bat

**On Unix or MacOS:**

.. code-block:: bash

    source /path/to/new/virtual/environment/bin/activate

Your command prompt should now indicate that the virtual environment is active.

Installing Dependencies
-----------------------

Install the project dependencies using the provided `requirements.txt` file.

.. code-block:: bash

    pip install -r requirements.txt

Installing the Project in Editable Mode
---------------------------------------

To install the project in an editable mode, which allows you to modify the source code and see the changes without reinstalling, use the following command:

.. code-block:: bash

    pip install -e .

Ensure that you are in the project's root directory where the `setup.py` file is located.

Running Scripts
---------------

After completing the setup, you can run the project scripts as follows:

.. code-block:: bash

    python path/to/project/scripts/run_power_forecast_{le/grath}.py

Replace `path/to/project` with the path to the project directory and choose one of the two example scripts.

Deactivating the Virtual Environment
------------------------------------

When you are done, you can deactivate the virtual environment:

.. code-block:: bash

    deactivate

This will return you to your global Python environment.

Conclusion
----------

Following these steps will set up a Python virtual environment specific to this project, install all necessary dependencies, and prepare the environment for development and testing of the project.
