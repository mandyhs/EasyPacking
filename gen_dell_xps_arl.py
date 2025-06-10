#!/usr/bin/env python
import argparse
import os
import sys
from gen_driver_package_by_project import gen_process

import pathlib

project_name = "Dell Xps Arl"
project_config = "Dell-Xps-ARL-2nd"
sensor = "ov02e10"
platform = "MTL"
module_name = ["2BG203N3BD", "CJFME322D","2BG203N3B", "CJFME322", "CBG202N3", "CJFPE27"]

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
        module_name=module_name
    )  

if __name__ == '__main__':
    sys.exit(main())  
