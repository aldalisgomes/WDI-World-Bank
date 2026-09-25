# We will use a dataset of indicators on the development of countries
# Source: https://databank.worldbank.org/source/world-development-indicators

#%% Importing libraries
import os
import platform
import subprocess

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% Loading the datasets
# We use an argument to handle NAs in the WDI data
wdi_data = pd.read_excel('data/WDI World Bank.xlsx', na_values="..")
group_data = pd.read_excel('data/WDI Income Group.xlsx')
country_data = pd.read_excel('data/WDI Country.xlsx')

#%% Basic data information
wdi_data.info()

#%% Unique elements of the variables
wdi_data['Country Name'].unique()
wdi_data['Series Name'].unique()
wdi_data['Topic'].unique()

#%% Renaming columns for easier access
wdi_data.rename(columns={'Country Name':'country',
                          'Country Code':'country_code',
                          'Series Name':'series',
                          'Series Code':'series_code',
                          '2021 [YR2021]':'year_2021',
                          'Topic':'topic'}, inplace=True)

#%% Analyzing the last rows
wdi_data.tail(n=20) # The last rows are references and will not be used

#%% Excluding the final rows (we add 1 position in the sequence)
wdi_data= wdi_data.iloc[0:383572,]

# Reviewing the data
wdi_data['country'].tail(n=20)

#%% Selecting health topics (They start with 'Health')
health_data = wdi_data[wdi_data['topic'].str.startswith('Health')]

#%% Let's change the structure of health_data
# Variables: series /// Observations: countries
health_data = pd.pivot(health_data,
                       index=['country','country_code'],
                       columns=['series'],
                       values='year_2021')
# Returning to the numeric index
health_data.reset_index(inplace=True)

#%% Cleaning observations
# In country_data 'Country' shows the country code
# let's change the variable name to make merges using this key
country_data.rename(columns={'Country':'country_code'},
                    inplace=True)
# Merge: the variable goes to the end of the dataset
health_data= pd.merge(health_data, country_data,
                      how='left',
                      on='country_code')
# The 'nan' values are not countries, let's exclude them with a filter 
health_data=health_data[~health_data['Name'].isna()].reset_index(drop=True)
# Let's remove the column that will no longer be used
health_data.drop(columns=['Name'], inplace=True)
#%% Variable cleaning
# Many variables only present NAs
# axis=1 -> refers to the columns
# how='all' -> drop if all elements are nan
health_data.dropna(axis=1,how='all',inplace=True)
#%% Add the "income group" category to the final dataset
# Add a grouping variable that is in 'group_data'
# Selecting the variables of interest
group_data_select=group_data[['Code','Income Group']].copy()
# Changing the key name for the link between DataFrames
group_data_select.rename(columns={'Code':'country_code'},inplace=True)
# Performing the merge
health_data=pd.merge(health_data,group_data_select,how='left',on='country_code')

#%% Let's reorganize the column position 
# Removes the 'Income Group' column from health_data, then stores this column in "organize" [.pop()],
organize=health_data.pop('Income Group')
# Put the 'Income Group' column,
# with the new name 'Group',
# in position 2 of the dataset health_data
health_data.insert(2,'Group',organize)

#%% For example, if it is a study about diabetes
# Let's see in which position the variable of interest is:
col_pos=health_data.columns 
print(col_pos) ## It is in position 23
# Descriptive statistics of column 23
health_data.iloc[:,23].describe()

# Statistics by groups
group_stats=health_data.iloc[:,[2,23]].groupby('Group').mean().reset_index()


# %% Chart
plt.figure(figsize=(15,9), dpi = 600)
ax = sns.barplot(data=group_stats, x=group_stats.iloc[:,0], y=group_stats.iloc[:,1])
for container in ax.containers: ax.bar_label(container, fmt='%.2f', padding=3, fontsize=12)
plt.xlabel('Group',fontsize=15)
plt.ylabel('Diabetes prevalence (% of population ages 20 to 79)', fontsize=15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

#-------------------------
# Create the 'results' folder in the project root (if it doesn't exist)
results_folder = 'results'
os.makedirs(results_folder, exist_ok=True)

# Save the generated chart inside the 'results' folder
image_path = os.path.join(results_folder, 'diabetes_prevalence.png')
plt.savefig(image_path, bbox_inches='tight')
plt.close() # Close the figure from memory

# Collect absolute paths
folder_path_abs = os.path.abspath(results_folder)
image_path_abs = os.path.abspath(image_path)

# Detect the environment using the platform module
release = platform.release().lower()
system = platform.system().lower()

if 'microsoft' in release:
    # Detected: WSL
    try:
        # Convert Linux paths to native Windows paths using wslpath -w
        win_folder_path = subprocess.check_output(['wslpath', '-w', folder_path_abs]).decode('utf-8').strip()
        win_file_path = subprocess.check_output(['wslpath', '-w', image_path_abs]).decode('utf-8').strip()
        
        # Call explorer.exe to open the converted folder
        subprocess.run(['explorer.exe', win_folder_path])
        
        # Call powershell.exe to automatically open the converted image
        ps_command = f"Invoke-Item -LiteralPath '{win_file_path}'"
        subprocess.run(['powershell.exe', '-Command', ps_command])
    except Exception as e:
        print(f"Error trying to open files in Windows via WSL: {e}")

elif system == 'windows':
    # Native support for Windows (os.startfile)
    os.startfile(folder_path_abs)
    os.startfile(image_path_abs)

elif system == 'darwin':
    # Native support for macOS (subprocess with open)
    subprocess.run(['open', folder_path_abs])
    subprocess.run(['open', image_path_abs])

else:
    # Generic support for standard Linux
    subprocess.run(['xdg-open', folder_path_abs])
    subprocess.run(['xdg-open', image_path_abs])
# %% END
