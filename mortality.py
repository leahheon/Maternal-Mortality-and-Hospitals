# import modules
import pandas as pd 
import geopandas as gpd 

# read in mortality file 
mortality = pd.read_csv('mortality.txt',sep='\t',names=['Notes','County','County Code','Deaths','Population','Crude Rate'])

# remove extra quotes 
mortality.columns = mortality.columns.str.strip('"')
print(mortality.head())

# replpace empty values with 0
mortality['Deaths'] = mortality['Deaths'].fillna(0)

# rename county fips column to match county data
mortality = mortality.rename(columns={'County Code':'COUNTYFP'})
mortality_with_quotes = pd.Series(['COUNTYFP'])

# keep only the columns with data
mortality = mortality[mortality['Deaths'].index < 785]
print(mortality['Deaths'])

# group mortality data by county fips code and deaths column
counts = mortality.groupby(['COUNTYFP','Deaths']).size()

# save mortality data to a csv
mortality.to_csv('mortality.csv')

# read in counties file containing Census cartographic boundary data
counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})

# merge mortality onto counties and save to a geopackage
merge = counties.merge(mortality,left_on='COUNTYFP',right_on='Deaths',how='left')
merge.to_file('mortality.gpkg',layer='mortality')
