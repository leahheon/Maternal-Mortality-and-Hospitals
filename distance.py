import geopandas as gpd
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

l1_shortest_line_CA = gpd.read_file('ca_l1_lines.shp')
distance_L1 = 'distance'
L1_avg_distance_CA = l1_shortest_line_CA[distance_L1].mean()

l1_shortest_line_AR = gpd.read_file('ar_l1_lines.shp',ignore_geometry=True)
distance_L1 = 'distance'
L1_avg_distance_AR = l1_shortest_line_AR[distance_L1].mean()

degrees_miles = 69
AR_decimal_degrees = 1.425574487041201
AR_avg_dist_L1 = degrees_miles*AR_decimal_degrees
AR_dist_final = round(AR_avg_dist_L1)
print("Arkansas average distance from county centroid to nearest Level 1 trauma center:",AR_dist_final,"miles")

CA_decimal_degrees = 1.5435713056074676
CA_avg_dist_L1 = degrees_miles*CA_decimal_degrees
CA_dist_final = round(CA_avg_dist_L1)
print("California average distance from county centroid to nearest Level 1 trauma center:",CA_dist_final,"miles")

#%%
california = l1_shortest_line_CA
arkansas = l1_shortest_line_AR

california['state'] = 'California'
arkansas['state'] = 'Arkansas'

data = pd.concat([california,arkansas])
data['distance'] *= 69
data = data.to_crs(epsg=5070)

counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})
counties = counties.to_crs(epsg=5070)
data_join = counties.merge(data,left_on='STATE_NAME', right_on='state',how='left')

plt.figure(figsize=(10,6))
sns.violinplot(data=data_join,x='state',y='distance',hue='state',palette='Set2',split=True)
plt.title('Average Distance to Nearest Level 1 Trauma Center')
plt.xlabel('State')
plt.ylabel('Distance (miles)')
plt.grid(True)
plt.tight_layout()

CA_median = data_join[data_join['state'] == 'California']['distance'].median()
AR_median = data_join[data_join['state'] == 'Arkansas']['distance'].median()
CA_mean = data_join[data_join['state'] == 'California']['distance'].mean()
AR_mean = data_join[data_join['state'] == 'Arkansas']['distance'].mean()

plt.axhline(y=CA_median,color='blue',linestyle='--',label='CA Median')
plt.axhline(y=AR_median,color='red',linestyle='--',label='AR Median')
plt.axhline(y=CA_mean,color='blue',linestyle='-',label='CA Mean')
plt.axhline(y=AR_mean,color='RED',linestyle='-',label='AR Mean')

plt.legend()
