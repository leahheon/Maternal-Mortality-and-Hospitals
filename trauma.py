# import modules
import pandas as pd
import geopandas as gpd

# read in county file 
counties = gpd.read_file('cb_2021_us_county_500k.zip',dtype={'COUNTYFP':str})

# read in hospital file 
hospitals_all = gpd.read_file('Hospitals.zip',ignore_geometry=True)
trauma = hospitals_all['TRAUMA'].value_counts()

# add all variations into three columns
trauma['LEVEL I'] = trauma['LEVEL I']+trauma['TRH']+trauma['TRF']+trauma['CTH']+trauma['LEVEL I PEDIATRIC']+trauma['LEVEL I ADULT, LEVEL II PEDIATRIC']+trauma['LEVEL I ADULT, LEVEL I PEDIATRIC']+trauma['ATH']+trauma['LEVEL I ADULT']+trauma['RTC']+trauma['LEVEL I, LEVEL II PEDIATRIC']+trauma['LEVEL I PEDIATRIC REHAB']+trauma['LEVEL I, LEVEL I PEDIATRIC']+trauma['RTH']+trauma['PARC']+trauma['I-RPTC']+trauma['LEVEL I PEDIATRIC']+trauma['ATH']
trauma['LEVEL II'] = trauma['LEVEL II']+trauma['LEVEL II ADULT, LEVEL II PEDIATRIC']+trauma['LEVEL II PEDIATRIC']+trauma['LEVEL II, LEVEL II PEDIATRIC']+trauma['LEVEL II ADULT']+trauma['LEVEL II / PEDIATRIC']+trauma['LEVEL II REHAB']+trauma['LEVEL II, LEVEL III PEDIATRIC, LEVEL II REHAB']
trauma['LEVEL III'] = trauma['LEVEL III']+trauma['LEVEL III ADULT']

# create dataframe with corresponding scores
trauma_classes = pd.DataFrame({
    'TRAUMA': ['LEVEL I', 'LEVEL II', 'LEVEL III', 'LEVEL IV', 'LEVEL V', 'NOT AVAILABLE'],
    'counts': ['426', '369', '551', '1008', '18', '5637']})
total = trauma_classes.groupby('TRAUMA')['counts'].sum()

scores = {'LEVEL I':'1',
         'LEVEL II':'2',
         'LEVEL III':'3',
         'LEVEL IV':'4',
         'LEVEL V':'5',
         'NOT AVAILABLE':'6'}

trauma_classes['score'] = trauma_classes['TRAUMA'].map(scores)

# save as csv to create a point file in QGIS
trauma_classes.to_csv('classes.csv')
trauma_classes = pd.read_csv('classes.csv')
joined = hospitals_all.merge(trauma_classes,on='TRAUMA',how='left')
joined = joined.fillna(0)
joined.to_csv('trauma_class.csv')

# calculate mean of average distance to nearest hospital
shortest_line_CA = gpd.read_file('shortest_line.shp')
distance = 'distance'
avg_distance_CA = shortest_line_CA[distance].mean()

shortest_line_AR = gpd.read_file('ARshortest_lines.shp',ignore_geometry=True)
distance='distance'
avg_distance_AR = shortest_line_AR[distance].mean()

arkansas_hospitals = hospitals_all[hospitals_all['STATE'] == 'AR']
ar_total = len(arkansas_hospitals)

california_hospitals = hospitals_all[hospitals_all['STATE'] == 'CA']
ca_total = len(california_hospitals)

ar_total_pop = hospitals_all[hospitals_all['STATE'] == 'AR']
ar_pop = ar_total_pop['POPULATION'].sum()

ca_total_pop = hospitals_all[hospitals_all['STATE'] == 'CA']
ca_pop = ca_total_pop['POPULATION'].sum()

# create dataframe for level 1 trauma centers 
counties.set_geometry('geometry',inplace=True)
level_1 = joined[joined['TRAUMA'] == 'LEVEL I']
L1 = gpd.GeoDataFrame(level_1)
L1.to_csv('L1.csv')

