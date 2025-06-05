#!/usr/bin/env python
import sys, pathlib, os
import argparse
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import subprocess, signal

VTGBUILD_ROOT = "\\\ccr.corp.intel.com\ec\proj\iag\peg\icgbj\OSimages\Artifacts\Scheduled\CameraSW"
CI_FILE = 'CI-scheduled.txt'
MANIFEST_FILE = 'manifest.xml'
CITAG_FILE = 'CI_tag.txt'
CI_PATH = ''

BRANCH_MAP: dict[str, str] = {
    'MTL':'stable_mtl_20221221',
    'LNL':'stable_lnl_pv_20240416', 
    'master':'master',
    'ADL_24H2':'stable_adlp_pv_24h2_20240206',
    'ADL':'stable_adlp_pv_cobalt_20210914',
    'JSL':'stable_jslppv_20h1_20200901'
}

def keyboard_interrupt_handler(signum: int, frame: object):
    print('WARNING: Interrupted with Ctrl-C', file=sys.stderr)
    sys.exit(1)

def get_args() -> argparse.Namespace:
    p: pathlib.Path

    print('== get args == \n')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog = 'check_tag',
        description = '...',
        epilog = '''example:    ./check_tag.py -v 17232 -b LNL 
               ''',
        formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-v', '--version',
        default = '',
        type = str,
        help = 'Path to the folder that contains source drivers. ')
    
    parser.add_argument(
        '-b', '--branch',
        default = '',
        type = str,
        help = 'branch ')
    
    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])

def parseManifest(xmlfile):
    tree = ET.parse(xmlfile) 
    root = tree.getroot()

    projs = {} 
  
    for item in root.findall('project'): 
        p = {}
        if item.attrib['name'] == 'vtg-windrv-sensors' or \
           item.attrib['name'] == 'imaging/ia-imaging-control' or \
           item.attrib['name'] == 'vied-vieddrv-camerasw_src' or \
           item.attrib['name'] == 'vtg-windrv-flash' :
            
            p['revision'] = item.attrib['revision']
            p['upstream'] = item.attrib['upstream']
            # print(f'{p}')
            projs[item.attrib['name']] = p
    
    return projs

def findManifestPath(prebuild_branch, version):
    wd = os.getcwd()
    os.chdir(prebuild_branch)
    #subprocess.run("ls")
    res = subprocess.run("ls", check=False, capture_output=True)
    #print(res.stdout)
    print(f'targer version {version}')

    idx_s = str(res.stdout).find(str(version))
    idx_e = str(res.stdout)[idx_s:].find('\\n')
    #print(f'find path: {idx_s}, {idx_e}')
    targer_folder = str(res.stdout)[idx_s:idx_s + idx_e]
    print(targer_folder)
    os.chdir(wd)

    return prebuild_branch + '\\' + targer_folder + '\\' + MANIFEST_FILE

def main():
    print(f'check sw tag {VTGBUILD_ROOT}')

    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    args = get_args()
    orig_dir: pathlib.Path = pathlib.Path.cwd()

    for k, v in vars(args).items():
        print(f'{k}, {v}')

    # matching and find branch
    if args.branch in BRANCH_MAP:
        print(f'branch: {BRANCH_MAP[args.branch]}')
    else:
        print(f'[ERROR] branch path not in BRANCH_MAP')
        exit('2')
        

    prebuild_branch =  VTGBUILD_ROOT + '\\' + BRANCH_MAP[args.branch]
    if not os.path.exists(prebuild_branch):
        print(f'[ERROR] prebuild path not exist: {prebuild_branch}')
        exit('2')
    
    os.chdir(prebuild_branch)
    prebuild_CI = ''
    for folder in glob.glob(args.version+'*'):
        #print(f'{folder}')
        prebuild_CI = prebuild_branch + '\\' + folder + '\\' + CI_FILE
        print(f'[CI_path]: {prebuild_CI}')

    # find 
    manifast_path = findManifestPath(prebuild_branch, args.version)
    print(f'[manifast_path]: {manifast_path}\n')

    # pares manifest
    commit_list = parseManifest(manifast_path)
    for item in commit_list:
        print(f'{item} : \t{commit_list[item]['revision']}, {commit_list[item]['upstream']}')

    #parse CI_PATH
    if os.path.exists(prebuild_CI):
        print(f'\nversion: {args.version}')
        multi_cols = [i for i in range(5)] # create some col names
        df = pd.read_csv(prebuild_CI, sep = ": ", engine='python', header=None, names=multi_cols)
        #print(df.shape)
        print(f'tag: {df.at[1,1]}')
        CI_PATH = df[1][1]
    
    if CI_PATH:
        TAG_Path = str(orig_dir) + '\\' + CITAG_FILE
        print(f'save tag : {TAG_Path}')
        f = open(TAG_Path, "w")
        f.write(CI_PATH)
        f.close()
    


if __name__ == '__main__':
    sys.exit(main())