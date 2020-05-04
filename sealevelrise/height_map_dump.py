import os

import argparse
import numpy as np
import pandas as pd
import sealevelrise

from PIL import Image

HEIGHT_MAP_TO_M = 1 / 64

def preprocess():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-r',
        '--rcp',
        action='store',
        choices=['2.6', '4.5', '8.5'],
        default='2.6',
        dest='rcp',
        help='Set RCP scenario to use for the height map dump.',
    )
    return argparser.parse_args()

def raise_sea_level(height_map, change):
    height_map_m = np.multiply(height_map, HEIGHT_MAP_TO_M)
    change_m = change * 0.001 # Convert mm to m.
    df = pd.DataFrame(height_map_m)
    for indexi, Data in df.iterrows():
        for indexj, value in Data.items():
            lower_land = value - change
            if lower_land < 0:
                lower_land = 0
            df.at[indexi, indexj] = lower_land
    result = np.multiply(df.to_numpy(), 1 / HEIGHT_MAP_TO_M)
    return result

def execute(rcp):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    dump_dir = os.path.join(script_dir, '../target/height-map-2020-2090')
    os.makedirs(dump_dir, exist_ok=True) # Make dump dir if it doesn't exist.
    resource_dir = os.path.join(script_dir, 'resource')
    gmsl_df = pd.read_csv(os.path.join(resource_dir, 'gmsl-2020-2090.csv'))
    height_map_image = Image.open(os.path.join(resource_dir, 'Maldives.png'))
    height_map = np.array(height_map_image)
    for index, row in gmsl_df.iterrows():
        filename = "height-map-rcp{0}-{1:.0f}.png".format(rcp, row['year'])
        change = row['rcp' + rcp]
        print("Dump {0} with change {1}.".format(filename, change))
        height_map = raise_sea_level(height_map, change)
        height_map_image = Image.fromarray(height_map.astype(np.int32))
        height_map_image.save(os.path.join(dump_dir, filename))

def main():
    args = preprocess()
    execute(args.rcp)

if __name__ == '__main__':
    main()
