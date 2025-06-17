#!/usr/bin/env python
import argparse
import os
import sys
from gen_driver_package_by_project import gen_process
from run_script_utils import run_python_script

import pathlib
import config_env

LOCAL_DST_ROOT = config_env.LOCAL_DST_ROOT
PACK_OUTPUT_ROOT = config_env.PACK_OUTPUT_ROOT

project_name = "Dell Tributo LNL"
project_config = "Dell-Tributo-LNL-2nd"
sensor = "ov02e10"
platform = "LNL"
module_name = ["2BG203N3", "CJFME32","CBG202N3", "CJFPE27"]

def main():
    parser = argparse.ArgumentParser(
        description=f'"gen {project_name} driver package"',
        epilog = '''example:   ''' +  os.path.basename(__file__) + ''' -v 00''',
        formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-v',"--version", type=str, required=True)
    args = parser.parse_args()

    gen_process(
        version=args.version,
        project_name=project_name,
        platform=platform,
        project_config=project_config,
        sensor=sensor,
        module_name=module_name,
        local_dst_root=LOCAL_DST_ROOT,
        pack_output_dir=PACK_OUTPUT_ROOT
    )  

if __name__ == '__main__':
    sys.exit(main())  
