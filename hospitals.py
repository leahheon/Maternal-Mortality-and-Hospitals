# import modules
import pandas as pd 
import geopandas as gpd

# read in hospital and county file 
hospitals = pd.read_csv('hospitals.csv',dtype={'COUNTYFIPS':str})
hospitals = hospitals.rename(columns={'COUNTYFIPS':'COUNTYFP'})
counties = gpd.read_file('cb_2021_us_county_500k.zip')

# create variable for crs 
wgs84 = 4326

# create a GeoDataFrame 
geom = gpd.points_from_xy(hospitals['LONGITUDE'],hospitals['LATITUDE'])
geo = gpd.GeoDataFrame(data=hospitals,geometry=geom,crs=wgs84)

# change crs and save as a geopackage
geo = geo.set_crs(5070,allow_override=True)
geo.to_file('geo.gpkg',layer='geo')

# group hospital data by county fips code and trauma level 
counts = hospitals.groupby(['COUNTYFP','TRAUMA']).size().reset_index('count')
counts_frame = counts.to_frame(name='TRAUMA')

counts['TRAUMA'] = counts['TRAUMA'].replace({'LEVEL I':'Level 1',
                          'LEVEL I ADULT':'Level 1 Adult',
                          'LEVEL I ADULT,LEVEL I PEDIATRIC':'Level 1 Adult_1',
                          'LEVEL I ADULT,LEVEL II PEDIATRIC':'Level 1 Adult_2',
                          'LEVEL I,LEVEL I PEDIATRIC':'Level 1_3',
                          'LEVEL I,LEVEL II PEDIATRIC':'Level 1_4',
                          'LEVEL II':'Level 2',
                          'LEVEL II / PEDIATRIC':'Level 2_3',
                          'LEVEL II ADULT':'Level 2_4',
                          'LEVEL II ADULT,LEVEL II PEDIATRIC':'Level 2_5',
                          'LEVEL II REHAB':'Level 2_6',
                          'LEVEL II,LEVEL II PEDIATRIC':'Level 2_7',
                          'LEVEL II,LEVEL III PEDIATRIC,LEVEL II REHAB':'Level 2_8',
                          'LEVEL III':'Level 3',
                          'LEVEL III ADULT':'Level 3_1',
                          'LEVEL IV':'Level 4',
                          'LEVEL V':'Level 5'})

# loop through each trauma level name to place all into only five columns
level_1 = [col for col in counts.columns if 'Level 1' in col]
counts['level1sum'] = counts[level_1].sum(axis=1)

level_2 = [col for col in counts.columns if 'Level 2' in col]
counts['level2sum'] = counts[level_2].sum(axis=1)

level_3 = [col for col in counts.columns if 'Level 3' in col]
counts['level3sum'] = counts[level_3].sum(axis=1)

level_4 = [col for col in counts.columns if 'Level 4' in col]
counts['level4sum'] = counts[level_4].sum(axis=1)

level_5 = [col for col in counts.columns if 'Level 5' in col]
counts['level5sum'] = counts[level_5].sum(axis=1)

# create dataframe containing only trauma column
by_county = counts.unstack()
by_county = by_county.fillna(0)
by_county = by_county.to_frame(name='TRAUMA')
#%%
# rename trauma columns to avoid inconsistency
by_county['TRAUMA'] = by_county['TRAUMA'].replace({'LEVEL I':'Level 1',
                          'LEVEL I ADULT':'Level 1 Adult',
                          'LEVEL I ADULT,LEVEL I PEDIATRIC':'Level 1 Adult_1',
                          'LEVEL I ADULT,LEVEL II PEDIATRIC':'Level 1 Adult_2',
                          'LEVEL I,LEVEL I PEDIATRIC':'Level 1_3',
                          'LEVEL I,LEVEL II PEDIATRIC':'Level 1_4',
                          'LEVEL II':'Level 2',
                          'LEVEL II / PEDIATRIC':'Level 2_3',
                          'LEVEL II ADULT':'Level 2_4',
                          'LEVEL II ADULT,LEVEL II PEDIATRIC':'Level 2_5',
                          'LEVEL II REHAB':'Level 2_6',
                          'LEVEL II,LEVEL II PEDIATRIC':'Level 2_7',
                          'LEVEL II,LEVEL III PEDIATRIC,LEVEL II REHAB':'Level 2_8',
                          'LEVEL III':'Level 3',
                          'LEVEL III ADULT':'Level 3_1',
                          'LEVEL IV':'Level 4',
                          'LEVEL V':'Level 5'})

# loop through each trauma level name to place all into only five columns
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
#%%
# merge by_county onto counties on GEOID
merge = counties.merge(by_county,on='GEOID',how='left')
merge = merge.fillna(0)
print(merge)

# save as csv and geopackage 
merge.to_csv('trauma.csv')
merge.to_file('trauma.gpkg',layer='trauma')
