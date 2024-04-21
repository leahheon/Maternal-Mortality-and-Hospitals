# import modules
import pandas as pd 
import geopandas as gpd

#%%
# read in hosptial file 
hospitals = gpd.read_file('hospitals.zip')
print(hospitals['COUNTY'])
hospitals.to_csv('hospitals.csv')

#%%
# read in county shape file
counties = gpd.read_file('cb_2021_us_county_500k.zip')
print(counties['NAME'])

# rename column to match 
counties.rename(columns={'NAME':'COUNTY'},inplace=True)
print(counties['COUNTY'].str.upper())

# save counties to geopackage 
counties.to_file('counties.gpkg',layer='counties')

#%%
# merge hospital data on county data 
both = counties.merge(hospitals,on='COUNTY',how='left',indicator=True)
print('\nMerge check:\n',both['_merge'].value_counts())
both.to_csv('merged.csv')
