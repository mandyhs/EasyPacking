import os, sys
import xml.etree.ElementTree as ET
import subprocess, signal
import argparse, pathlib

VTG_DAILYPATH = '\\\\ccr.corp.intel.com\\ec\\proj\\iag\\peg\\icgbj\\OSimages\\Artifacts\\Scheduled\\CameraSW\\stable_lnl_pv_20240416'

def keyboard_interrupt_handler(signum: int, frame: object):
    print('WARNING: Interrupted with Ctrl-C', file=sys.stderr)
    sys.exit(1)

def get_args() -> argparse.Namespace:
    p: pathlib.Path

    print('== get args ==\n')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog = os.path.basename(__file__),
        description = '...',
        epilog = '''example:   ''' +  os.path.basename(__file__) + '''''',
        formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-t', '--target-sha',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='target sha')
    
    parser.add_argument(
        '-s', '--search-dailybuild',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='path for dailybuild ')
    
    #return parser.parse_args()
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

def checkCommit(dailybuild_sha, target_sha):
    print('\n== checkCommit ==')

    isInclude = False
    # git checkout 1bebacf69626a45e93b8abe05bf8fcdd10def639 | git cat-file -t 1bbcc593

    print(f'{dailybuild_sha}, target {target_sha}')

    wd = os.getcwd()
    os.chdir("C:\\Users\\mandyhsi\\workspace\\vtg-windrv-sensors")

    cmd = 'git checkout ' + dailybuild_sha
    print(subprocess.run(cmd))

    #cmd = 'git cat-file -t ' + target_sha
    #if [ 0 -eq $(git merge-base --is-ancestor $COMMIT_ID HEAD) ]; then echo "true"; else echo "false"; fi
    cmd = 'if [ 0 -eq $(git merge-base --is-ancestor ' + target_sha + ') ]; then echo "true"; else echo "false"; fi'
    res = subprocess.run(cmd, shell=True, universal_newlines=True, check=False, capture_output=True)
    print(cmd, res.stdout)

    if (str(res.stdout).__contains__('commit')):
        print("!!!! include !!!!")
        isInclude = True

    print(subprocess.run("git checkout master"))
    print(subprocess.run("git branch -vv"))
    os.chdir(wd)

    return isInclude

def findManifestPath(version):
    wd = os.getcwd()
    os.chdir(VTG_DAILYPATH)
    #subprocess.run("ls")
    res = subprocess.run("ls", check=False, capture_output=True)
    #print(res.stdout)
    print(f'targer version {version}')

    idx_s = str(res.stdout).find(str(version))
    idx_e = str(res.stdout)[idx_s:].find('\\n')
    print(f'find path: {idx_s}, {idx_e}')
    targer_folder = str(res.stdout)[idx_s:idx_s + idx_e]
    print(targer_folder)
    os.chdir(wd)

    return VTG_DAILYPATH + '\\' + targer_folder + '\\manifest.xml'


def main():
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    args: argparse.Namespace = get_args()       
    
    for k, v in vars(args).items():
        print(f'[{k}]: {v}')
    print('')

    # find 
    manifast_path = findManifestPath(args.search_dailybuild)
    print(f'\n [manifast_path]: {manifast_path}')

    # pares manifest
    commit_list = parseManifest(manifast_path)
    for item in commit_list:
        print(f'{item} : \t{commit_list[item]['revision']}, {commit_list[item]['upstream']}')

    # git commit
    #isInclude = checkCommit(commit_list['vtg-windrv-sensors']['revision'], str(args.target_sha))
    #print(f'\n\n [IsInclude]: {isInclude}')

    

if __name__ == '__main__':
    sys.exit(main())
    

    
    
    