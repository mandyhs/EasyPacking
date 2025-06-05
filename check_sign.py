#!/usr/bin/env python

import argparse
import signal, pathlib, sys, os
import subprocess
import configparser
import collections
from tabulate import tabulate
import pandas as pd


PLATFORM_MAP: dict[str, list] = {
    'MTL':['Z:\\IPU6_MTL_x64\\','MTL'],
    'LNL':['Z:\\IPU7_LNL_x64\\','LNL'], 
    'master':['Z:\\master_IPU7_PTL_x64\\','PTL'],  
	'ADL':['Z:\\IPU6_ADL_x64\\','ADL'],
    #Z:\IPU7_LNL_x64\13942_1\Product   
}

CHECK_DRIVER: list[str] = [
    'iacamera64.cat',
    'ov02c10.cat'
]

CHECK_INF: list[str] = [
    'iacamera64.inf',
    'ov02c10.inf',
    'ov05c10.inf'
]

FOLDER_LIST: list[str] = [
    '',
    '_External',
    '_External_Product_Signed'
]

# Support parsing duplicated options in inf
# https://stackoverflow.com/a/15848928/1592410
class KeyCaseInsensitiveValueExtendedDict(collections.OrderedDict):
    def __setitem__(self, key: str, value: any):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
            return
        super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        k: str
        for k in self.keys():
            if k.lower() != key.lower():
                continue
            return super().__contains__(k)
        return False

    def __getitem__(self, key: str) -> any:
        k: str
        for k in self.keys():
            if k.lower() != key.lower():
                continue
            return super().__getitem__(k)

def get_version(inf_file) -> str:
    res: str = 'Unknown_Version'

    if os.path.exists(inf_file):
        config: configparser.ConfigParser = configparser.ConfigParser(
            allow_no_value=True, dict_type=KeyCaseInsensitiveValueExtendedDict, strict=False)
        config.optionxform = str
        config.read(inf_file, encoding='utf-16')
        #print(inf_file)
        #print(config.sections())
        res = '.'.join(config['version'].get('driverver').split(',')[1:]).strip()
    return res

def get_args() -> argparse.Namespace:
    p: pathlib.Path

    print('\n== get args ==\n')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='check_sign',
        description='...',
        epilog='''example:    ./check_sign.py -p MTL -cv 16990_5
               ''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-cv', '--check-version',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='version need to check ')
    
    parser.add_argument(
        '-p', '--platform',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            ''),
        type=pathlib.Path,
        help='platform ')
    
    parser.add_argument(
        '-t', '--signtool-path',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            '../vieddrv-github/w/camerasw/Tools/DigitalSigning/x64/'),
        type=pathlib.Path,
        help='Path contain signtool.exe')
    
    #return parser.parse_args()
    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])

def keyboard_interrupt_handler(signum: int, frame: object):
    print('WARNING: Interrupted with Ctrl-C', file=sys.stderr)
    sys.exit(1)

def main() -> int:
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    orig_dir: pathlib.Path = pathlib.Path.cwd()

    print(orig_dir)
    args: argparse.Namespace = get_args()       
    
    for k, v in vars(args).items():
        print(f'{k}: {v}')
    print('')

    ICE_driver_path = str(PLATFORM_MAP[str(args.platform)][0]) + str(args.check_version) + \
                    '''\\Product\\Camera_''' + str(PLATFORM_MAP[str(args.platform)][1])
    if not os.path.exists(ICE_driver_path): 
        print(f'[ERROR] driver path is not exist, please check the version num\n {ICE_driver_path}')
        exit(2)

    sign_result = {}
    for j in range(len(CHECK_DRIVER)):
        cer_result: dict = {}
        for i in range(len(FOLDER_LIST)):
            #/signtool.exe verify /v /kp
            cmd = '''signtool.exe verify /v /kp ''' + ICE_driver_path + str(FOLDER_LIST[i]) + '''\\''' + CHECK_DRIVER[j]

            # Trivial but horrible
            #print(cmd)
            results = subprocess.run(
                cmd, shell=True, universal_newlines=True, check=False, capture_output=True)
            
            Certificate_content = str(results.stdout)

            # check timestamp
            str_timestamp = 'The signature is timestamped'
            index_start = str(Certificate_content).find(str_timestamp)
            index_start += len(str_timestamp) 
            index_end = str(Certificate_content).find('\nTimestamp Verified by:') - 1
            #print(f'{Certificate_content[index_start:index_end]}')

            Verify_res = False
            folder_name = 'Camera'+ FOLDER_LIST[i]
            cer_item = {}
            
            if (Certificate_content.__contains__('Microsoft Windows Third Party Component CA')):
                if (i == 2): Verify_res = True 
                cer_item['TargetType'] = 'HLK sign'
                cer_item['Timestamp'] = Certificate_content[index_start:index_end]

            elif (Certificate_content.__contains__('Microsoft Windows PCA 2010')):
                if (i == 1): Verify_res = True 
                cer_item['TargetType'] = 'PreProd sign'
                cer_item['Timestamp'] = Certificate_content[index_start:index_end]

            elif (Certificate_content.__contains__('Sectigo Public Code Signing CA EV R36')):
                if (i == 0): Verify_res = True 
                cer_item['TargetType'] = 'Intel sign'
                cer_item['Timestamp'] = Certificate_content[index_start:index_end]

            else:
                cer_item['TargetType'] = 'null'
                cer_item['Timestamp'] = 'null'

            cer_item['VerifyResult'] = Verify_res
            cer_result[folder_name] = cer_item

        sign_result[CHECK_DRIVER[j]] = cer_result

    # check version
    print('\n== [check version] ==\n')
    version_result = {}
    for j in range(len(CHECK_INF)):
        ver_inf = {}
        for i in range(len(FOLDER_LIST)):
            target_inf = ICE_driver_path + FOLDER_LIST[i] + '''\\''' + CHECK_INF[j]
            ver_inf['Camera' + FOLDER_LIST[i]] = get_version(target_inf)
        version_result[CHECK_INF[j]] = ver_inf

    
    df = pd.DataFrame(version_result)
    print(tabulate(df.T, headers="keys"))   

    # print sign result
    print('\n== [check signature] ==')
    df = pd.DataFrame.from_dict({(i,j): sign_result[i][j] 
                           for i in sign_result.keys() 
                           for j in sign_result[i].keys()},
                       orient='index')
    #print(df)
    print(tabulate(df, headers='keys'))
    return 0


if __name__ == '__main__':
    sys.exit(main())