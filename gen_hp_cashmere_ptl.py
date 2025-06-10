#!/usr/bin/env python
import argparse
import os
import sys
from gen_driver_package_by_project import gen_process


project_name = "Hp-Cashmere-PTL"
project_config = "Hp-Cashmere-PTL"
sensor = "ov05c10"
platform = "PTL"

module_name = ["CJFPE50", "CBG502N3"]


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
