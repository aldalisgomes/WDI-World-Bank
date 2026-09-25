# World Bank Health Indicators Analysis

## Overview
This repository contains a data analysis project focused on the development indicators of various countries, using the [World Bank's World Development Indicators (WDI) dataset](https://databank.worldbank.org/source/world-development-indicators). 

The main goal of this script is to load raw data, clean and pivot the health-related indicators, and visualize the **diabetes prevalence** across different country income groups.

## Project Structure
Based on the repository organization:
* `data/`: Contains the raw dataset files (ignored in Git to prevent uploading large Excel files).
    * `WDI World Bank.xlsx`
    * `WDI Income Group.xlsx`
    * `WDI Country.xlsx`
* `outputs/`: Directory intended for saving generated visualizations (e.g., plots and charts).
* `src/`: Contains the main Python source code.
    * `Script WDI World Bank.py`: The main data processing and visualization script.
* `requirements.txt`: List of Python dependencies required to run the code.

## Prerequisites
Ensure you have Python installed. You can install the required libraries by running:
```bash
pip install -r requirements.txt
```
*(Note: `pandas`, `seaborn`, `matplotlib`, and `openpyxl` are required).*

## How to Run

**Note for Windows Users:** The Makefile commands are designed for Unix environments (Linux/macOS). If you are on Windows, please use Git Bash or WSL to run the pipeline. The script is fully configured to automatically open the generated visualization on your Windows screen even if running from WSL.

### 1. Clone the repository and access the folder
```bash
git clone https://github.com/aldalisgomes/WDI-World-Bank.git
cd WDI-World-Bank
```

### 2. Create and activate the virtual environment (Required on newer Debian/Ubuntu-based systems, such as WSL)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies and run the pipeline
```bash
make setup
make run
```
*(Note: To clean the environment, cache, and the generated `resultados` folder, you can run `make clean`)*

### Alternative for Windows (Or No Make Installed)
If you are using standard Git Bash, PowerShell, or Command Prompt without make installed, you can simply run the Python script directly after activating your virtual environment:

```bash
pip install -r requirements.txt
python "src/Script WDI World Bank.py"
```