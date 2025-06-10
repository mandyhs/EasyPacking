#!/usr/bin/env python
import argparse
import os
import sys
from run_script_utils import run_python_script

import pathlib

project_name = "Hp-Cashmere-PTL"
project_config = "Hp-Cashmere-PTL"
sensor = "ov05c10"
platform = "PTL"

def main():
    parser = argparse.ArgumentParser(
        description=f'"gen {project_name} driver package"',
        prog = 'gen_dell_tributo_lnl',
        epilog = '''example:   ''' +  os.path.basename(__file__) + ''' -v 00''',
        formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-v',"--version", type=str, required=True)
    args = parser.parse_args()

    if args.version == '00':
        # grep which version want to download
        print(f"👀 choose which do u want  {args.version}...\n\n")
        copy_worker_args = {
            "-v": 0,
            "-p": platform
        }
        run_python_script("copy_cce_driver.py", copy_worker_args)
        print(f'👀 choose which do u want \n\n')
        exit(0)

    # get cce build
    print(f"-->  get cce build for {project_name} {args.version}...")
    copy_worker_args = {
        "-v": args.version,
        "-p": platform
    }
    run_python_script("copy_cce_driver.py", copy_worker_args)
    print(f'🙌🙌🙌  completed get cce build for {project_name} {args.version}.\n\n')

    # pack drvier package
    driver_path = pathlib.Path(__file__).parent / f"../Drivers/ICE_build/{platform}/{args.version}/"
    print(f"driver_path: {driver_path}")

    worker_args = {
        "-d": driver_path,
        "-v": project_config,
        "-s": sensor,
        "-o": f"{project_config}-{args.version}"  # type: ignore
    }

    run_python_script("pack_light", worker_args)

if __name__ == '__main__':
    sys.exit(main())  
