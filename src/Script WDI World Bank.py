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

# TESTE 1
# Criar a pasta 'resultados' na raiz do projeto (se não existir)
pasta_resultados = 'resultados'
os.makedirs(pasta_resultados, exist_ok=True)

# Salvar o gráfico gerado dentro da pasta 'resultados'
caminho_imagem = os.path.join(pasta_resultados, 'prevalencia_diabetes.png')
plt.savefig(caminho_imagem, bbox_inches='tight')
plt.close() # Fecha a figura da memória

# Coletar os caminhos absolutos
caminho_pasta_abs = os.path.abspath(pasta_resultados)
caminho_imagem_abs = os.path.abspath(caminho_imagem)

# Detectar o ambiente usando o módulo platform
release = platform.release().lower()
sistema = platform.system().lower()

if 'microsoft' in release:
    # Detectado: WSL
    try:
        # Converter caminhos do Linux para caminhos nativos do Windows com wslpath -w
        win_folder_path = subprocess.check_output(['wslpath', '-w', caminho_pasta_abs]).decode('utf-8').strip()
        win_file_path = subprocess.check_output(['wslpath', '-w', caminho_imagem_abs]).decode('utf-8').strip()
        
        # Chamar o explorer.exe para abrir a pasta convertida
        subprocess.run(['explorer.exe', win_folder_path])
        
        # Chamar o powershell.exe para abrir automaticamente a imagem convertida
        comando_ps = f"Invoke-Item -LiteralPath '{win_file_path}'"
        subprocess.run(['powershell.exe', '-Command', comando_ps])
    except Exception as e:
        print(f"Erro ao tentar abrir os arquivos no Windows via WSL: {e}")

elif sistema == 'windows':
    # Suporte nativo para Windows (os.startfile)
    os.startfile(caminho_pasta_abs)
    os.startfile(caminho_imagem_abs)

elif sistema == 'darwin':
    # Suporte nativo para macOS (subprocess com open)
    subprocess.run(['open', caminho_pasta_abs])
    subprocess.run(['open', caminho_imagem_abs])

else:
    # Suporte genérico para Linux padrão
    subprocess.run(['xdg-open', caminho_pasta_abs])
    subprocess.run(['xdg-open', caminho_imagem_abs])

# %% END


# %% END
