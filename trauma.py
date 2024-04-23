import pandas as pd
import geopandas as gpd

hospitals_all = gpd.read_file('hospitals_all.shp',ignore_geometry=True)
trauma = hospitals_all['TRAUMA'].value_counts()
trauma['LEVEL I'] = trauma['LEVEL I']+trauma['TRH']+trauma['TRF']+trauma['CTH']+trauma['LEVEL I PEDIATRIC']+trauma['LEVEL I ADULT, LEVEL II PEDIATRIC']+trauma['LEVEL I ADULT, LEVEL I PEDIATRIC']+trauma['ATH']+trauma['LEVEL I ADULT']+trauma['RTC']+trauma['LEVEL I, LEVEL II PEDIATRIC']+trauma['LEVEL I PEDIATRIC REHAB']+trauma['LEVEL I, LEVEL I PEDIATRIC']+trauma['RTH']+trauma['PARC']+trauma['I-RPTC']+trauma['LEVEL I PEDIATRIC']+trauma['ATH']
trauma['LEVEL II'] = trauma['LEVEL II']+trauma['LEVEL II ADULT, LEVEL II PEDIATRIC']+trauma['LEVEL II PEDIATRIC']+trauma['LEVEL II, LEVEL II PEDIATRIC']+trauma['LEVEL II ADULT']+trauma['LEVEL II / PEDIATRIC']+trauma['LEVEL II REHAB']+trauma['LEVEL II, LEVEL III PEDIATRIC, LEVEL II REHAB']
trauma['LEVEL III'] = trauma['LEVEL III']+trauma['LEVEL III ADULT']

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

trauma_classes.to_csv('classes.csv')

trauma_classes = pd.read_csv('classes.csv')
joined = hospitals_all.merge(trauma_classes,on='TRAUMA',how='left')
joined = joined.fillna(0)

joined.to_csv('trauma_class.csv')

