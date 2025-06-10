#!/usr/bin/env python
import shutil
import signal
import sys, os, pathlib,datetime
import argparse
import zipfile

CCE_BUILD_ROOT = "\\\twsimglab005\camera_drivers"
LOCAL_DST_ROOT = "C:\\Users\\mandyhsi\\workspace\\Drivers\\ICE_build\\"

PLATFORM_MAP: dict[str, list] = {
    'MTL':['Z:\\IPU6_MTL_x64\\','MTL'],
    'LNL':['Z:\\IPU7_LNL_x64\\','LNL'], 
    'PTL':['Z:\\master_IPU7_PTL_x64\\','PTL'],  
	'ADL':['Z:\\IPU6_ADL_x64\\','ADL'],
    #Z:\IPU7_LNL_x64\13942_1\Product   
}

FOLDER_LIST: list[str] = [
    '',
    '_External',
    '_External_Product_Signed'
]

ZIP_substring = 'symbols.zip'

def copytree_with_prompt(src: str, dst: str):
    if os.path.exists(dst):
        print(f"⚠️ dst exist：{dst}")
        choice = input("overwrite it? (y/n): ").strip().lower()

        if choice != "y":
            print("❌ user chose not to overwrite. Exiting.")
            return

        # 確認覆蓋時，先刪掉目標資料夾
        print(f"🗑️ delete the old dir: {dst} ...")
        shutil.rmtree(dst)

    print(f"📁 copying ... {src} ➜ {dst}")
    shutil.copytree(src, dst, symlinks=False, ignore=None)
    print("✅ copy completed.")

def get_args() -> argparse.Namespace:
    p: pathlib.Path

    print('== get args == \n')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog = 'get ice driver',
        description = '...',
        epilog = '''example:    ./copy_cce_driver.py -v 17232 -p LNL 
               ''',
        formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-v', '--version',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='version need to copy, if like to check last 5, use -v 0')
    
    parser.add_argument(
        '-p', '--platform',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='platform ')
    
    parser.add_argument(
        '-o', '--only',
        default=int(3),
        type=int,
        help='zip name: 0 = internal, 1 = external_ES, 2 = external_QS')
    
    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])

def keyboard_interrupt_handler(signum: int, frame: object):
    print('WARNING: Interrupted with Ctrl-C', file=sys.stderr)
    sys.exit(1)

def already_extracted(path):
    """check the folder is already extracted and unzipped"""
    print(f'check if {path} is already extracted')
    return os.path.exists(path) and os.listdir(path)

def main():
    print(f'download driver from - {CCE_BUILD_ROOT}')

    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    args = get_args()
    orig_dir: pathlib.Path = pathlib.Path.cwd()

    for k, v in vars(args).items():
        print(f'{k}, {v}')

    # get platform and path 
    ICE_plt_path = str(PLATFORM_MAP[str(args.platform)][0]) 
    if not os.path.exists(ICE_plt_path): 
        print(f'[ERROR] driver path is not exist, please check the version num\n {ICE_plt_path}')
        exit(2)

    print(f'ICE_plt_path: {ICE_plt_path}\n')

    if str(args.version) == '0':
        # list the latest 3 version 
        items = os.listdir(ICE_plt_path)
        items.sort(key=lambda f: os.path.getmtime(os.path.join(ICE_plt_path, f)), reverse=True)
        latest_files = items[:5]
        for fname in latest_files:
            full_path = os.path.join(ICE_plt_path, fname)
            ts = os.path.getmtime(full_path)
            mod_dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  {fname}    Last Modified: {mod_dt}")
        exit(0)

    # find zips
    ICE_driver_path = str(ICE_plt_path + str(args.version) + '''\\''') 

    if not os.path.exists(ICE_driver_path): 
        print(f'[ERROR] driver path is not exist, please check the version num\n {ICE_plt_path}')
        exit(2)

    print(FOLDER_LIST[0])

    # filter by option 
    if args.only < 3:
        ZipName = 'Camera_' + str(args.platform) + '_' + FOLDER_LIST[args.only] + ZIP_substring
        print(f'only filer zip file with {ZipName}')
        zips = []
        zips.append(ZipName)

    else:
        zips = [
            f for f in os.listdir(ICE_driver_path)
            if os.path.isfile(os.path.join(ICE_driver_path, f)) and ZIP_substring in f
        ]
        
        print(zips)

    # define designation path
    LOCAL_dst = LOCAL_DST_ROOT + '''\\''' + str(PLATFORM_MAP[str(args.platform)][1]) + '''\\''' + str(args.version)
    print(f'copy driver zip into: {LOCAL_dst}')
    os.makedirs(LOCAL_dst,  exist_ok=True)

    # download debug zip
    if os.path.exists(pathlib.Path(ICE_driver_path, 'Debug_Camera_' + str(args.platform) + '.zip')):
            shutil.copy2(
                pathlib.Path(ICE_driver_path, 'Debug_Camera_' + str(args.platform) + '.zip'),
                pathlib.Path(LOCAL_dst, 'Debug_Camera_' + str(args.platform) + '.zip')
            )
        
    '''
    for z in zips:
        if not os.path.exists(pathlib.Path(LOCAL_dst,z)) :
        
            print(f'copying... {pathlib.Path(LOCAL_dst,z)}')
            shutil.copy2(pathlib.Path(ICE_driver_path,z), pathlib.Path(LOCAL_dst,z))
    '''

    # unzip to des folder
    for z in zips:
        if os.path.exists(pathlib.Path(ICE_driver_path,z)):
            if already_extracted(pathlib.Path(LOCAL_dst,z.replace('_symbols.zip', ''))):
                # if already extracted, skip it
                print(f"⏩ Skipped (already extracted): {z}")
                continue

            with zipfile.ZipFile(pathlib.Path(ICE_driver_path,z), 'r') as zip_ref:
                zip_ref.extractall(LOCAL_dst)

    # return des path 



if __name__ == '__main__':
    sys.exit(main())    