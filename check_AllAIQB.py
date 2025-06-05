#!/usr/bin/env python
import sys, os, pathlib,datetime
import argparse

def parse_section(input, start, end):
    ll = input[start:end].split("\\x00")
    return ll

def get_args() -> argparse.Namespace:
    p: pathlib.Path

    print('\n== args ==\n')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='check_sign',
        description='...',
        epilog='''example:    ./check_AIQB.py -f XXXX.aiqb''',
        formatter_class=argparse.RawTextHelpFormatter)

    
    parser.add_argument(
        '-f', '--aiqb_path',
        default=pathlib.Path(os.path.realpath(__file__)).parent / pathlib.Path(
            '.\OV02C10_2BG203N3_LNL.aiqb'),
        type=pathlib.Path,
        help='AIQB path')

    #return parser.parse_args()
    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def main():

    args = get_args()
    for k, v in vars(args).items():
        print(k,v)

    aiqb_list = []
    
    if pathlib.Path(args.aiqb_path).is_dir:
        print(f'this is a folder, scan all aiqb below')

        for file in os.listdir(args.aiqb_path):
            if file.endswith(".aiqb"):
                aiqb_list.append(os.path.join(args.aiqb_path, file))
    else:
        aiqb_list.append(args.aiqb_path)


    # parse aiqb comment 
    for aiqb_file in aiqb_list:
        with open(aiqb_file, 'rb') as f:
            data = f.read()

            # head 
            idx_s = str(data).find('Sensor')
            idx_prj = str(data).find('ProjectName')
            idx_m = str(data).find('Module')

            # comment
            strKey = 'Comment'
            idx_com = str(data).find(strKey)
            idx_time = str(data).find('time')
            #print(idx_com, idx_time)

            print(f'\n>> aiqb name: [{pathlib.Path(aiqb_file).name}]')
            print(f'\n>> timestamp: [{datetime.datetime.fromtimestamp(pathlib.Path(aiqb_file).stat().st_ctime)}]')
            print('>>>>> Project:')
            print(parse_section(str(data),idx_s,idx_prj))
            print(parse_section(str(data),idx_prj,idx_m))
            print(parse_section(str(data),idx_m,idx_com))

            print('>>>>> Comment:')
            # comment 
            comment_data = str(data)[idx_com+len(strKey)+4:idx_time]
            comment_list = comment_data.split("\\r\\n")
            #print(comment_list, len(comment_list))
            for i in range(len(comment_list)):
                c_list = comment_list[i].split("\"\"")
                print(c_list)


if __name__ == '__main__':
    sys.exit(main())    
