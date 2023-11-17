from osgeo import gdal, ogr, gdal_array
import numpy as np
import pandas as pd


def zonal_data(raster_path, shp_path, field_name):
    # Open the raster file
    raster = gdal.Open(raster_path)
    # Read as array
    raster_array = raster.GetRasterBand(1).ReadAsArray()
    NoData_value = -9999
    
    # Open the data source and read in the extent
    source_ds = ogr.Open(shp_path)
    source_layer = source_ds.GetLayer()
    source_srs = source_layer.GetSpatialRef()
    
    # create an in-memory dataset with the same dimensions and resolution as the raster
    driver = gdal.GetDriverByName('MEM')
    target_ds = driver.Create('', int(raster.RasterXSize), int(raster.RasterYSize), 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(raster.GetGeoTransform())
    target_ds.SetProjection(raster.GetProjection())
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    # Set all pixels in the target raster band to 0
    band.WriteArray(np.zeros((int(raster.RasterYSize), int(raster.RasterXSize))))
    # Create an empty dataframe with the desired columns
    df = []
    # Loop through each feature in the shapefile
    for feature in source_layer:
        # Create a new layer for each feature
        mem_driver = ogr.GetDriverByName('Memory')
        mem_ds = mem_driver.CreateDataSource('')
        mem_layer = mem_ds.CreateLayer('mem_layer', srs=source_srs)
        mem_layer.CreateFeature(feature)
        # Create a copy of the target dataset
        target_ds_copy = driver.Create('', int(raster.RasterXSize), int(raster.RasterYSize), 1, gdal.GDT_Byte)
        target_ds_copy.SetGeoTransform(raster.GetGeoTransform())
        target_ds_copy.SetProjection(raster.GetProjection())
        band_copy = target_ds_copy.GetRasterBand(1)
        band_copy.SetNoDataValue(NoData_value)
        # Rasterize the new layer into the copy
        gdal.RasterizeLayer(target_ds_copy, [1], mem_layer, burn_values=[1])
        # Read the array after rasterization
        array = band_copy.ReadAsArray()
        # Create a binary mask for the pixels within the polygon
        mask = (array == 1)
        # Apply the mask to the NDVI array to extract only the values within the polygon
        out_values = raster_array[mask]
        # Extract the raw values within the polygon
        #masked_ndvi = np.ma.masked_array(raster_array, mask=~mask)
        df.append({"Feature": feature.GetField(field_name), "value": out_values})
    data_frame = pd.DataFrame(df)
    
    data = []
    for h in range(data_frame[{"value"}].shape[1]):
        for j in range(data_frame[{"Feature"}].shape[0]):
            name = data_frame.iloc[j, 0]
            value = data_frame[{"value"}].iloc[j, h]
            for item in value:              
                data.append({"{}".format(field_name): name, "value": item})
        df = pd.DataFrame(data)
        df.index += 1
        return df  
    # Close the copy of the target dataset
    target_ds_copy = None


def groupby_agg(df, group_cols, value_col, funcs):
    funcs_dict = {
            'count': pd.Series.count,
            'min': pd.Series.min,
            'max': pd.Series.max,
            'mean': pd.Series.mean,
            'sum': pd.Series.sum,
            'std': pd.Series.std,
            'median': pd.Series.median,
            'majority': lambda x: x.mode().iloc[0] if not x.empty else np.nan,
            'minority': lambda x: x.value_counts().index[-1] if not x.empty else np.nan,
            'unique': pd.Series.nunique,
            'range': lambda x: x.max() - x.min(),
            'nodata': lambda x: x.isnull().sum(),
            'nan': lambda x: x.isna().sum(),
        }
    agg_funcs = [funcs_dict[func] for func in funcs]
    agg_func_names = [func for func in funcs]
    result_df = df.groupby(group_cols)[value_col].agg(agg_funcs)
    result_df.columns = [f"{func}" for func in agg_func_names]
    out_df = result_df.reset_index()
    out_df.index += 1
    return out_df