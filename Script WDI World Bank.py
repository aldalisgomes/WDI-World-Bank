# We will use a dataset of indicators on the development of countries
# Source: https://databank.worldbank.org/source/world-development-indicators

#%% Importing libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% Loading the datasets
# We use an argument to handle NAs in the WDI data
dados_wdi = pd.read_excel('WDI World Bank.xlsx', na_values="..")
dados_grupo = pd.read_excel('WDI Income Group.xlsx')
dados_paises = pd.read_excel('WDI Country.xlsx')

#%% Basic data information
dados_wdi.info()

#%% Unique elements of the variables
dados_wdi['Country Name'].unique()
dados_wdi['Series Name'].unique()
dados_wdi['Topic'].unique()

#%% Renaming columns for easier access
dados_wdi.rename(columns={'Country Name':'pais',
                          'Country Code':'cod_pais',
                          'Series Name':'serie',
                          'Series Code':'cod_serie',
                          '2021 [YR2021]':'ano_2021',
                          'Topic':'topico'}, inplace=True)

#%% Analyzing the last rows
dados_wdi.tail(n=20) # The last rows are references and will not be used

#%% Excluding the final rows (we add 1 position in the sequence)
dados_wdi= dados_wdi.iloc[0:383572,]

# Reviewing the data
dados_wdi['pais'].tail(n=20)

#%% Selecting health topics (They start with 'Health')
dados_saude = dados_wdi[dados_wdi['topico'].str.startswith('Health')]

#%% Let's change the structure of health_data
# Variables: series /// Observations: countries
dados_saude = pd.pivot(dados_saude,
                       index=['pais','cod_pais'],
                       columns=['serie'],
                       values='ano_2021')
# Returning to the numeric index
dados_saude.reset_index(inplace=True)

#%% Cleaning observations
# In country_data 'Country' shows the country code
# let's change the variable name to make merges using this key
dados_paises.rename(columns={'Country':'cod_pais'},
                    inplace=True)
# Merge: the variable goes to the end of the dataset
dados_saude= pd.merge(dados_saude, dados_paises,
                      how='left',
                      on='cod_pais')
# The 'nan' values are not countries, let's exclude them with a filter 
dados_saude=dados_saude[~dados_saude['Name'].isna()].reset_index(drop=True)
# Let's remove the column that will no longer be used
dados_saude.drop(columns=['Name'], inplace=True)
#%% Variable cleaning
# Many variables only present NAs
# axis=1 -> refers to the columns
# how='all' -> drop if all elements are nan
dados_saude.dropna(axis=1,how='all',inplace=True)
#%% Add the "income group" category to the final dataset
# Add a grouping variable that is in 'group_data'
# Selecting the variables of interest
dados_grupo_select=dados_grupo[['Code','Income Group']].copy()
# Changing the key name for the link between DataFrames
dados_grupo_select.rename(columns={'Code':'cod_pais'},inplace=True)
# Performing the merge
dados_saude=pd.merge(dados_saude,dados_grupo_select,how='left',on='cod_pais')

#%% Let's reorganize the column position 
# Removes the 'Income Group' column from health_data, then stores this column in "organize" [.pop()],
organizar=dados_saude.pop('Income Group')
# Put the 'Income Group' column,
# with the new name 'Group',
# in position 2 of the dataset health_data
dados_saude.insert(2,'Group',organizar)

#%% For example, if it is a study about diabetes
# Let's see in which position the variable of interest is:
col_pos=dados_saude.columns 
print(col_pos) ## It is in position 23
# Descriptive statistics of column 23
dados_saude.iloc[:,23].describe()

# Statistics by groups
estat_grupo=dados_saude.iloc[:,[2,23]].groupby('Group').mean().reset_index()


# %% Chart
plt.figure(figsize=(15,9), dpi = 600)
ax = sns.barplot(data=estat_grupo, x=estat_grupo.iloc[:,0], y=estat_grupo.iloc[:,1])
for container in ax.containers: ax.bar_label(container, fmt='%.2f', padding=3, fontsize=12)
plt.xlabel('Grupo',fontsize=15)
plt.ylabel('Diabetes prevalence (% of population ages 20 to 79)', fontsize=15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()


# %% END
