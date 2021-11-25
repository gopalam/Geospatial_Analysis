# code to extract watershed boundary via USGS streamstats.
# lat/longs located on a stream is needed to extract watershed boundary
# required: earthlabs StreamsStats library

import json
import pytest
import geojson
from geojson import Feature, Point, FeatureCollection
from streamstats import Watershed
import geopandas as gpd
# from shapely.geometry import shape
import pandas as pd
import time

# import watershed points

df = pd.read_excel (r'D:\GIS\HydroSheds\StreamStats\Site Location Info.xlsx') # read input locations
cols=['Site', 'USGS_Site_id', 'Latitude', 'Longitude']

df.columns=cols
COLS=['geometry', 'DRNAREA','HUCID', 'HydroID', 'streamid', 'Shape_Area', 'CENTROIDY', 'OUTLETX',
        'OUTLETY', 'CONTOUR', 'FOREST','SLOPERATIO', 'OBJECTID','GlobalWshd',
        'DrainID', 'BSLOPCM','Shape_Leng', 'CENTROIDX', 'BFAREA','LENGTH', 'PRECIP' ]
cols=['Site','SiteId','geometry'] # shorter form of columns, use this or the above defined columns if you need more variables.
 
# for Index,row in df.iterrows():
for Index in range(70,96):
    st=df.Site[Index]
    print(f'Site{Index}:',st)
    stid=df.USGS_Site_id[Index]
    la=df.Latitude[Index]
    lo=df.Longitude[Index]
    start = time.time()
    wshed=Watershed.Watershed(lat=la, lon=lo)
    result=wshed.boundary;
    geojson_out = geojson.loads(json.dumps(result))
    collection = FeatureCollection(geojson_out.features)
    if (len(collection.features)>0):
        print('length:',len(collection.features))
        gd=gpd.GeoDataFrame.from_features(collection['features'])
    # gd= gd[COLS]   
        gd['Site']='';
        gd.at[0, 'Site'] = st
        # gd['SiteId']=np.nan;
        gd.at[0, 'SiteId'] = stid
        gd= gd[cols]   
        fpath=r'D:\GIS\HydroSheds\StreamStats\ShapeFiles';
        fname=fpath+'\Site_'+str(Index)+'.shp';
        gd.to_file(driver = 'ESRI Shapefile', filename= fname)
        end = time.time()
        print(f"Runtime for delination: {end - start} seconds")
        print("sleep 30 seconds")
        time.sleep(30)
        del gd, st, stid, la,lo,geojson_out,wshed,result;
        print("awake")
    else:
        pass
