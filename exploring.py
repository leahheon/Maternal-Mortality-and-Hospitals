import pandas as pd 
import geopandas as gpd

deaths = pd.read_csv('deaths.txt')
deaths.rename(columns={'Unnamed: 0':'COUNTY'},inplace=True)

print(deaths.head())

#%%
hospitals = pd.read_csv('hospitals.csv')
print(hospitals['COUNTY'])
