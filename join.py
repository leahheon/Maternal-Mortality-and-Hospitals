# import modules
import pandas as pd 
import geopandas as gpd

# 
mortality = pd.read_csv('mortality.csv')
mortality['COUNTYFP'] = mortality['COUNTYFP'].str.strip('"')
counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})
merge = counties.merge(mortality,left_on='GEOID',right_on='COUNTYFP',how='left')
merge = merge.fillna(0)
merge.to_file('mortality.gpkg',layer='mortality')
