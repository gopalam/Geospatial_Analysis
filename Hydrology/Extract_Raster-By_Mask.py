# -*- coding: utf-8 -*-
"""
Created on Sun May  2 08:48:55 2021
@author: gopal mulukutla
this is the python + geopandas+ rasterio equivalent of extracting a raster by a mask of a shape file
usage: a large land use raster file, need to extract a portion by a shapefile mask
This is for a single shape file. 
Not all the code is original, the def function is from a source that I am unable to track down
"""
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import geopandas as gpd
import pandas as pd
# example 

               
def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]
 
#path to raster
fp = r""
#path to output file
out_tif = r""

data = rasterio.open(fp)

#path to mask shape file
fps=r""

GEO=gpd.read_file(fps)
ind=GEO.shape[0]
for i in range(0,ind+1):
    print(i)
    geo=gpd.GeoDataFrame(GEO.iloc[i-1:i])
geo=gpd.read_file(fps)
geo = geo.to_crs(crs=data.crs.data)
coords = getFeatures(geo)

out_img, out_transform = mask(data, coords, crop=True)
out_meta = data.meta.copy()

out_meta.update({"driver": "GTiff", "height": out_img.shape[1],"width": out_img.shape[2],
                 "transform": out_transform,"crs": pycrs.parse.from_epsg_code(3035).to_proj4()} )   
with rasterio.open(out_tif, "w", **out_meta) as dest:dest.write(out_img)
clipped = rasterio.open(out_tif)
show(clipped)

