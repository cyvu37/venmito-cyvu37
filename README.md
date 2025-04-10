# Venmito Data Engineering Project

**Author**: Jared Hidalgo

**Email**: jaredhidalgo@gmail.com

## About the Program

This CLI program sets up the database from scratch and provides a wide variety of options for data analysis.

## The Process

### Used Technologies

- **OS**: Windows 11 Home 22631.5039
- **Language**: Python 3.13.2
    - Check the requirements.txt file for Python packages.
- **Software**
    - **IDE**: Visual Studio Code v1.98.2
    - **Server**: pgAdmin 4 v9.1
        - Username: postgres
        - Password: Space!3742

### Development Steps

1. The Server
    - Installed pgAdmin 4 and setup basic server.
1. The Python Script
    - Wrote routine to auto-check required packages on startup.
    - Wrote functions to run prefabricated SQL queries for views, aka "Hot-N-Ready Views", and to let the user run their own SQL queries.
    - Wrote menu for user options.

## How To Use The Program

### Before Running

1. Requirements
    - Run a pgAdmin 4 server
    - Start an empty database titled `postgres` with the following login:
        - User: postgres
        - Password: Space!3742
    - Connection to our customized DeepSeek LLM.
1. Optional Tasks 
    - Add a virtual environment.
    - Run `pip install -r requirements.txt`

### Running: Prerequisites

The program will first run two sets of prerequisites before entering the Main Menu:
1. Checking packages.
1. Checking the connection of the database as in the requirements.

### Running: The Main Menu

This software isn't finished, but the plan is the following:
- In the Main Menu, the user can...
    - Pick options to generate prefab reports with `[1] Hot-N-Ready Views`.
    - Write their own SQL query with `[2] DIY Report`.
    - Make an AI prompt for a customized DeepSeek LLM with `[3] Create DeepSeek Prompt`. (Experimental)
    - Export any results in a selected format from the OUTPUT MENU.
    - Start over once they successfully finish a task.
- [1] Hot-N-Ready Views
    - The user can choose from a selection of pre-written SQL queries. 
    - For example, the user can select `View Store Products` to view the name and number of products each store has sold.
- [2] Create SQL Report: The user can enter their own SQL queries and export results.
- [3] Create DeepSeek Prompt
    - Once the user selects this, the program will connect with our customized (local or online) DeepSeek LLM.
    - Then the user can enter in a prompt for the DeepSeek LLM.
    - Once the user's prompt is submitted, the program will send it to the DeepSeek LLM where the LLM will connect with the database, analyze it, and bring back a report based on the user's prompt.

## DISCLAIMER:

This project and its contents are the exclusive property of Xtillion, LLC and are intended solely for the evaluation of Jared Hidalgo. Any distribution, reproduction, or unauthorized use is strictly prohibited. By accessing and using this project, I agree to abide by these conditions. Failure to comply with these terms may result in legal action.

Please note that this project is provided "as is", without warranty of any kind, express or implied. Xtillion is not liable for any damages or claims that might arise from using or misusing this project.
