'''
Write a function that aggregates pixel values within a prescribed ROI.
Let the user choose between mean, sum, or variance aggregators.

Note: ROI, Raster and Aggregator are specified as inputs in the master config.yaml file

Reference:
https://pythonhosted.org/rasterstats/
'''

import sys
import fiona
import rasterio
import geopandas as gpd
import numpy as np
import yaml
from rasterstats import zonal_stats


def main():
    # load configuration parameters from file
    cfg = None
    try:
        with open("../config.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except Exception as e:
        print('Configuration file not found: %s',e)
        sys.exit()

    # Assign input vector and raster from config.yaml
    input_zone_polygon = cfg["zonal_input_vector"]
    input_value_raster = cfg["zonal_input_raster"]
    stats = cfg["zonal_aggregator"]

    try:
        #open raster using rasterio
        raster = rasterio.open(input_value_raster)

        #open vector as a geopandas dataframe
        vector = roi_to_gpd(input_zone_polygon)

        #project vector to raster format if both are different
        projected_vector = reproject(vector, raster)

        #aggregate pixel values of input raster by specified vector (geojson or shapefile)
        zs = calculate_zonal(projected_vector, input_value_raster, stats)
        print(zs)
    except Exception as e:
        print('Error calculating zonal stats for the given inputs: %s', e)
        sys.exit()

# Convert vector ROI to geopandas dataframe
def roi_to_gpd(shp):
    data = gpd.read_file(shp)
    return data

# Reproject input vector to raster using rasterio
def reproject(fcgpd, raster):
    reproj = None
    try:
        proj = raster.crs.to_proj4()
        print("Original vector layer projection: ", fcgpd.crs)
        reproj = fcgpd.to_crs(proj)
        print("New vector layer projection (PROJ4): ", reproj.crs)
    except Exception as e:
        print('Unable to re-project vector: %s', e)
        sys.exit()
    return reproj

def variance(x):
    return np.ma.var(x)

# Calculate zonal statistics
def calculate_zonal(vector, raster, stats):
    geostats = None
    try:
        #variance is not handled by rasterstats library, so handle it specially
        if stats.strip() == "variance":
            result = zonal_stats(vector, raster, add_stats={'variance':variance}, geojson_out=True)
        else:
            result = zonal_stats(vector, raster, stats=stats, geojson_out=True)

        # Store result in geopandas dataframe
        geostats = gpd.GeoDataFrame.from_features(result)
    except Exception as e:
        print('Error calculating zonal statistics: %s', e)
        sys.exit()
    return geostats

# if __name__ == '__main__':
#     main()