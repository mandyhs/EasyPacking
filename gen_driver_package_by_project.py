#!/usr/bin/env python
import argparse
import os
import shutil
import sys
from run_script_utils import run_python_script
from parse_aiqb_for_project import parse_aiqb_from_build
import pathlib
import copy_cce_driver
import datetime

def gen_process(version: str, project_name: str, platform: str, project_config: str, sensor: str, module_name: list[str], local_dst_root: str, pack_output_dir: str = "./") -> None:

    if str(version) == '00000':
        # list the latest 1 version
        ICE_plt_path = copy_cce_driver.get_plt_path(platform)
        latest_files = copy_cce_driver.check_the_latest_n_version(ICE_plt_path, 1)
        if latest_files:
            full_path = os.path.join(ICE_plt_path, latest_files[0])
        ts = os.path.getmtime(full_path)
        mod_dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {latest_files[0]}    Last Modified: {mod_dt}")
        version = latest_files[0]  # update args.version to the latest one
    
    if version == '00':
        # grep which version want to download
        print(f"👀 choose which do u want  {version}...\n\n")
        copy_worker_args = {
            "-v": 0,
            "-p": platform
        }
        run_python_script("copy_cce_driver.py", copy_worker_args)
        print(f'👀 choose which do u want \n\n')
        exit(0)

    # get cce build
    print(f"-->  get cce build for {project_name} {version}...")
    copy_worker_args = {
        "-v": version,
        "-p": platform
    }
    run_python_script("copy_cce_driver.py", copy_worker_args)
    print(f'🙌🙌🙌  completed get cce build for {project_name} {version}.\n\n')

    # pack driver package
    driver_path = pathlib.Path(__file__).parent / f"{local_dst_root}/{platform}/{version}/"
    print(f"driver_path: {driver_path}")

    output_dir = f"{project_config}-{version}"

    worker_args = {
        "-d": driver_path,
        "-v": project_config,
        "-s": sensor,
        "-o": output_dir  # type: ignore
    }

    run_python_script("pack_light", worker_args)

    # parse AIQB.txt
    print(f"-->  parse AIQB.txt for {project_name} {version}...")
    parse_aiqb_from_build(driver_path, output_dir, module_name=module_name, platform=platform)
    print(f"Parsed AIQB.txt and saved to {output_dir}/IQ_info.txt")

    print(f'🙌🙌🙌  completed pack driver package for {project_name} {version}.\n\n')

    # move output to local destination
    pack_output_dir = pathlib.Path(pack_output_dir) / output_dir
    print(f"Moving output to local destination: {pack_output_dir}")
    shutil.move(output_dir, pack_output_dir)
    print(f'🙌🙌🙌  completed move output to local destination for {project_name} {version}.\n\n')
