# import modules
import pandas as pd 
import geopandas as gpd

# read in hospital and county file 
hospitals = pd.read_csv('hospitals.csv',dtype={'COUNTYFIPS':str})
hospitals = hospitals.rename(columns={'COUNTYFIPS':'COUNTYFP'})
counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})

# create variable for crs 
wgs84 = 4326

# create a GeoDataFrame 
geom = gpd.points_from_xy(hospitals['LONGITUDE'],hospitals['LATITUDE'])
geo = gpd.GeoDataFrame(data=hospitals,geometry=geom,crs=wgs84)

# group hospital data by county fips code and trauma level 
counts = hospitals.groupby(['COUNTYFP','TRAUMA']).size()
by_county = counts.unstack()
by_county = by_county.fillna(0)

by_county = by_county.rename(columns={'LEVEL I':'Level 1',
                          'LEVEL I ADULT':'Level 1 Adult',
                          'LEVEL I ADULT,LEVEL I PEDIATRIC':'Level 1 Adult1',
                          'LEVEL I ADULT,LEVEL II PEDIATRIC':'Level 1 Adult2',
                          'LEVEL I,LEVEL I PEDIATRIC':'Level 1 3',
                          'LEVEL I,LEVEL II PEDIATRIC':'Level 1 4',
                          'LEVEL II':'Level 2',
                          'LEVEL II / PEDIATRIC':'Level 2 3',
                          'LEVEL II ADULT':'Level 2 4',
                          'LEVEL II ADULT,LEVEL II PEDIATRIC':'Level 2 5',
                          'LEVEL II REHAB':'Level 2 6',
                          'LEVEL II,LEVEL II PEDIATRIC':'Level 2 7',
                          'LEVEL II,LEVEL III PEDIATRIC,LEVEL II REHAB':'Level 2 8',
                          'LEVEL III':'Level 3',
                          'LEVEL III ADULT':'Level 3 1',
                          'LEVEL IV':'Level 4',
                          'LEVEL V':'Level 5'})

level_1 = [col for col in by_county.columns if 'Level 1' in col]
by_county['level1sum'] = by_county[level_1].sum(axis=1)

level_2 = [col for col in by_county.columns if 'Level 2' in col]
by_county['level2sum'] = by_county[level_2].sum(axis=1)

level_3 = [col for col in by_county.columns if 'Level 3' in col]
by_county['level3sum'] = by_county[level_3].sum(axis=1)

level_4 = [col for col in by_county.columns if 'Level 4' in col]
by_county['level4sum'] = by_county[level_4].sum(axis=1)

level_5 = [col for col in by_county.columns if 'Level 5' in col]
by_county['level5sum'] = by_county[level_5].sum(axis=1)
 
merge = counties.merge(by_county,left_on='GEOID',right_on='COUNTYFP',how='left')
merge = merge.fillna(0)
print(merge)
merge.to_csv('trauma.csv')
merge.to_file('trauma.gpkg',layer='trauma')
