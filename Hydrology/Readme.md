
Code posted here covers parts of worksflow to (a) delineate a watershed basins through a call to the  USGS StreamStats API (b) the basin shape files are used to clip NLCD Land Use data (2016) (done in QGIS) (c) Land use stats from the data clipped to the watersheds is done to produce -percentage of watershed with, developed, agriculture, forest, wetlands, and water. Percent "human" (percent developed + percent ag) is also reported. 