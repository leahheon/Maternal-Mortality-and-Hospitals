# import modules
import geopandas as gpd
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

# read in shortest line shapefiles for CA and AR
l1_shortest_line_CA = gpd.read_file('ca_l1_lines.shp')
l1_shortest_line_AR = gpd.read_file('ar_l1_lines.shp',ignore_geometry=True)

# rename files 
california = l1_shortest_line_CA
arkansas = l1_shortest_line_AR
california['state'] = 'California'
arkansas['state'] = 'Arkansas'

# concatenate two dataframes into one 
data = pd.concat([california,arkansas])

# change crs 
data = data.to_crs(epsg=5070)

# read in counties file and change crs to match data 
counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})
counties = counties.to_crs(epsg=5070)

# trimmed both dataframes to include only necessary columns
counties_trim = counties[['GEOID','geometry','STATE_NAME']]
data_trim = data[['GEOID','distance','TRAUMA']]

# merge data onto counties
data_join = counties_trim.merge(data_trim,how='right',on='GEOID')
# data_join = data_join.fillna(0)

# create a split violin plot showing distances to nearest level 1 trauma center
plt.figure(figsize=(10,6))
sns.violinplot(data=data_join,x='TRAUMA',y='distance',hue='STATE_NAME',palette='Set2',split=True)
plt.title('Average Distance to Nearest Level 1 Trauma Center')
plt.xlabel('State')
plt.ylabel('Distance (miles)')
plt.grid(True)
plt.tight_layout()
plt.savefig('avgdistance.png')
