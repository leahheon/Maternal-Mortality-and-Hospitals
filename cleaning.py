import pandas as pd 
import geopandas as gpd

deaths = pd.read_csv('deaths.txt')
deaths.rename(columns={'Unnamed: 0':'COUNTY'},inplace=True)
print(deaths['COUNTY'].str.lower())

#%%
hospitals = gpd.read_file('hospitals.zip')
print(hospitals['COUNTY'])
hospitals.to_csv('hospitals.csv')

#%%
counties = gpd.read_file('tl_2021_us_county.zip')
print(counties['NAME'])
counties.rename(columns={'NAME':'COUNTY'},inplace=True)
print(counties['COUNTY'].str.upper())
counties.rename(columns={'INTPLTON':'LONGITUDE'},inplace=True)
counties.to_file('counties.gpkg',layer='counties')

#%%
both = pd.merge(counties,hospitals,on='COUNTY',how='left',indicator=True)
print('\nMerge check:\n',both['_merge'].value_counts())
both.to_csv('merged.csv')
