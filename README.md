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
1. Clone this repository to your local machine.
2. Ensure the three required Excel files are placed inside the `data/` folder.
3. Run the main analysis script from the root directory:
```bash
python "src/Script WDI World Bank.py"
```