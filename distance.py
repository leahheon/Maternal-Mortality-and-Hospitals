import geopandas as gpd

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
