import pandas as pd 
import geopandas as gpd

# read in hospital and county file 
hospitals = pd.read_csv('hospitals.csv',dtype={'COUNTYFIPS':str})
hospitals = hospitals.rename(columns={'COUNTYFIPS':'COUNTYFP'})

counties = gpd.read_file('cb_2021_us_county_500k.zip')
counties = counties.to_crs(4326)
centroids = counties.copy()
centroids['geometry']=counties.centroid

# create variable for crs 
wgs84 = 4326

# create a GeoDataFrame 
geom = gpd.points_from_xy(hospitals['LONGITUDE'],hospitals['LATITUDE'])
geo = gpd.GeoDataFrame(data=hospitals,geometry=geom,crs=wgs84)
geo = geo.to_crs(4326)

merged = centroids.sjoin_nearest(geo,distance_col='distance')
counties['distance']=merged['distance']

merged_trimmed = merged[merged['STATEFP'].isin(['05','06'])]
merged_trimmed = merged_trimmed[merged_trimmed['TRAUMA'].isin(['LEVEL I','LEVEL II','LEVEL III'])]
AR_CA = merged_trimmed[['GEOID','geometry','TRAUMA','distance']]
file = AR_CA.to_file('AR_CA.gpkg',layer='AR_CA')
files = AR_CA.to_csv('ar_ca.csv')
