"""

Script to create an hdf5 version of our data (more efficient).

"""
import h5py
import os
import rasterio
import argparse
import numpy as np
import json
import sys

sys.path.insert(0, '../')
import util

def get_grid_num(filename, ext, group_name):
    if ext == 'json' and group_name in ['s1_dates', 's2_dates']:
        grid_num = filename.split('_')[-1]
    elif ext == 'json' and group_name in ['planet_dates']:
        grid_num = filename.split('_')[-2]
    elif ext == 'npy' and group_name in ['s1', 's2', 'labels', 'planet'] and 'mask' not in filename:
        grid_num = filename.split('_')[-1] if group_name not in ['labels', 'planet'] else filename.split('_')[-2]
    elif ext == 'npy' and group_name == 'cloudmasks' and 'mask' in filename:
        grid_num = filename.split('_')[-2]
    else:
        grid_num = None
    return grid_num

def create_hdf5(args, groups=None):
    """ Creates a hdf5 representation of the data.

    Args:
        data_dir - (string) path to directory containing data which has three subdirectories: s1, s2, masks
        output_dir - (string) path to output directory
    """

    data_dir = args.data_dir
    output_dir = args.output_dir
    country = args.country
    use_planet = args.use_planet
    out_fname = args.out_fname

    if groups is None:
        if country in ['germany']:
            groups = ['s2', 'labels', 's2_dates']
        else:
            groups = ['s1', 's2', 'labels', 'cloudmasks', 's1_dates', 's2_dates']
        if use_planet:
            groups += ['planet', 'planet_dates']

    hdf5_file = h5py.File(os.path.join(output_dir, out_fname), 'a')
    # subdivide the hdf5 directory into grids and masks
    for group_name in groups:
        if group_name not in hdf5_file:
            hdf5_file.create_group(f'/{group_name}')

        actual_dir_name = None
        if group_name in ['s1', 's1_dates']:
            actual_dir_name = "s1_npy"
        elif group_name in ['s2', 's2_dates', 'cloudmasks']:
            actual_dir_name = "s2_npy"
        elif group_name in ['planet', 'planet_dates']:
            actual_dir_name = "planet_npy"
        elif group_name == 'labels':
            actual_dir_name = "raster_npy"

        for filepath in os.listdir(os.path.join(data_dir, actual_dir_name)):
            print('filepath: ', filepath)
            filename, ext = filepath.split('.')
            # get grid num to use as the object's file name
            grid_num = get_grid_num(filename, ext, group_name)
            if grid_num is None: continue
            # load in data
            if ext == 'npy':
                data = np.load(os.path.join(data_dir, actual_dir_name, filepath))
            elif ext == 'json':
                # open json of dates
                with open(os.path.join(data_dir, actual_dir_name, filepath)) as f:
                    dates = json.load(f)['dates']
                data = util.dates2doy(dates)
 
            # create file name
            hdf5_filename = f'/{group_name}/{grid_num}'
            hdf5_file.create_dataset(hdf5_filename, data=data, dtype='i2', chunks=True)
            print(f"Processed {os.path.join(group_name, filepath)} as {hdf5_filename}")

    hdf5_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str,
                        help='Path to directory containing data.',
                        default='/home/roserustowicz/croptype_data_local/data/tanzania/')
    parser.add_argument('--output_dir', type=str,
                        help='Path to directory to output the hdf5 file.',
                        default='/home/roserustowicz/croptype_data_local/data/tanzania/')
    parser.add_argument('--country', type=str,
                        help='Country to output the hdf5 file for.',
                        default='tanzania')
    parser.add_argument('--use_planet', type=util.str2bool, default=True,
                        help='Include Planet in hdf5 file')
    parser.add_argument('--out_fname', type=str, default='data.hdf5')
    args = parser.parse_args()

    groups = None #['planet', 'planet_dates', 'labels']

    create_hdf5(args, groups)

