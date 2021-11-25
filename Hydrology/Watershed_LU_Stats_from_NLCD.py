# this code reads in raster format (tif ) Land use data from NLCD (2016), that is clipped for each watershed boundary, and calculates the land use stats.
# land use stats are percent Ag, percent forest, percent developed, percent water, and percent wetland. 
#percent human= percent ag + percent developed.
import rasterio
import numpy as np
from rasterio.plot import show
import glob
import pandas as pd
import ntpath

# watershed land use stats calculated from the tif files extracted NLCD data
#cycle through all the tif files in this folder.

# fp=r"D:\GIS\HydroSheds\StreamStats\NLCD\Watershed_LU\LU_Site_1.tif"

fi=(glob.glob(r"D:\GIS\HydroSheds\StreamStats\NLCD\Watershed_LU2\*.tif"))


df = pd.read_excel (r'D:\GIS\HydroSheds\StreamStats\Site Location Info.xlsx')
cols = ['Site_code', 'Area_km2', 
        'Forest_Cells','Developed_Cells','Ag_cells','Wetland_cells','Water_cells','Human_cells','Total_Cells',
        'Forest_km2','Developed_km2','Ag_km2','Wetland_km2','Water_km2','Human_km2','Total_km2',
        'Forest_percent','Developed_percent','Ag_percent','Wetland_perecent','Water_percent','Human_percent','Total_percent']

LU_stats = pd.DataFrame(columns = cols)


ag=[81,82]
forest=[31,41,42,43,51,52,71,72,73,74]
developed=[21,22,23,24]
water=[11,12]
wetland=[90,95]
human=developed+ag


fp='D:\\GIS\\HydroSheds\\StreamStats\\NLCD\\Watershed_LU2\\LU_'

for num,fpath in enumerate(fi):
    # print(file)
    raster = rasterio.open(fi[num])
    sitepath = fi[num]
    sitename=sitepath.replace(fp,'')
    print(sitename)    
    show(raster)
    LU=raster.read()
    unique, frequency = np.unique(LU,return_counts = True)
    
    Total_cells=sum(frequency)-frequency[0]
    Area_km2=Total_cells*(30/1000)*(30/1000)
    
    Ag_id=np.where(np.in1d(unique, ag))
    forest_id=np.where(np.in1d(unique, forest))
    dev_id=np.where(np.in1d(unique, developed))
    water_id=np.where(np.in1d(unique, water))
    wetland_id=np.where(np.in1d(unique, wetland))
    human_id=np.where(np.in1d(unique, human))
    
    #
    Forest_cells=sum(frequency[forest_id])
    Developed_cells=sum(frequency[dev_id])
    Ag_cells=sum(frequency[Ag_id])
    Wetland_cells=sum(frequency[wetland_id])
    Water_cells=sum(frequency[water_id])
    Human_cells=sum(frequency[human_id])
    
    
    Forest_km2=Forest_cells*(30/1000)*(30/1000)
    Developed_km2=Developed_cells*(30/1000)*(30/1000)
    Ag_km2=Ag_cells*(30/1000)*(30/1000)
    Wetland_km2=Wetland_cells*(30/1000)*(30/1000)
    Water_km2=Water_cells*(30/1000)*(30/1000)
    Human_km2=Human_cells*(30/1000)*(30/1000)
    
    Total_km2=sum([Forest_km2,Developed_km2,Ag_km2,Wetland_km2,Water_km2])
    
    Forest_percent=(Forest_cells/Total_cells)*100
    Developed_percent=(Developed_cells/Total_cells)*100
    Ag_percent=(Ag_cells/Total_cells)*100
    Wetland_percent=(Wetland_cells/Total_cells)*100
    Water_percent=(Water_cells/Total_cells)*100
    Human_percent=(Human_cells/Total_cells)*100
    Total_percent=sum([Forest_percent,Developed_percent,Ag_percent,Wetland_percent,Water_percent])
    
    to_append = [sitename,Area_km2,Forest_cells,Developed_cells,Ag_cells, Wetland_cells,Water_cells,Human_cells,Total_cells,
                          Forest_km2, Developed_km2 ,Ag_km2,Wetland_km2,Water_km2,Human_km2, Total_km2,
                      Forest_percent,Developed_percent,Ag_percent,Wetland_percent,Water_percent,Human_percent,Total_percent];
    
    df_len = len(LU_stats)
    LU_stats.loc[df_len] = to_append
    

LU_stats.to_excel("Watershed_LU.xlsx") 
