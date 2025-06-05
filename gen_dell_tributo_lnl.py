#!/usr/bin/env python
import argparse
import sys
from run_script_utils import run_python_script

import pathlib

def main():
    parser = argparse.ArgumentParser(description="gen dell tributo lnl")
    parser.add_argument('-v',"--version", type=str, required=True)
    args = parser.parse_args()

    if args.version == '00':
        # grep which version want to download
        print(f"👀 choose which do u want  {args.version}...\n\n")
        copy_worker_args = {
            "-v": 0,
            "-p": "LNL"
        }
        run_python_script("copy_cce_driver.py", copy_worker_args)
        print(f'👀 choose which do u want \n\n')
        exit(0)

    # get cce build
    print(f"-->  get cce build for Dell Tributo LNL {args.version}...")
    copy_worker_args = {
        "-v": args.version,
        "-p": "LNL"
    }
    run_python_script("copy_cce_driver.py", copy_worker_args)
    print(f'🙌🙌🙌  completed get cce build for Dell Tributo LNL {args.version}.\n\n')

    # pack drvier package
    driver_path = pathlib.Path(__file__).parent / f"../Drivers/ICE_build/LNL/{args.version}/"
    print(f"driver_path: {driver_path}")

    worker_args = {
        "-d": driver_path,
        "-v": "Dell-Tributo-LNL-2nd",
        "-s": "ov05c10"
    }

    run_python_script("pack_light", worker_args)

if __name__ == '__main__':
    sys.exit(main())  
