import pathlib
import argparse
import re
from ast import literal_eval

def parse_aiqb_txt(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current = {}
    section = None
    for line in lines:
        line = line.strip()
        if line.startswith(">> aiqb name:"):
            if current:
                results.append(current)
            current = {'project': [], 'comment': []}
            match = re.search(r'\[(.*?)\]', line)
            if match:
                current['aiqb_name'] = match.group(1)
        elif line.startswith(">>>>> Project:"):
            section = 'project'
        elif line.startswith(">>>>> Comment:"):
            section = 'comment'
        elif line.startswith("[") and section:
            try:
                parsed = literal_eval(line)
                current[section].append(parsed)
            except:
                pass  # skip malformed lines

    if current:
        results.append(current)

    return results

def parse_aiqb_from_build(driver_path, output_dir, module_name=None, platform="MTL"):
    results = []    
    # parse AIQB.txt from driver path for project module
    # output in a txt file
    aiqb_path = driver_path / "AIQB.txt"
    iq_info_path = pathlib.Path(output_dir) / "IQ_info.txt"
    if not aiqb_path.exists():
        print(f"❌ AIQB.txt not found in {driver_path}. Please check the driver path.")
    else:
        print(f"Parsing AIQB.txt from {aiqb_path}...")
        parsed_data = parse_aiqb_txt(aiqb_path)
        target_names = set()
        for module in module_name:
            target_names.add(f'{module}_{platform}')

        print(f"Target module names: {target_names}")

        filtered_data = [
            item for item in parsed_data
            if any(module in item['aiqb_name'] for module in target_names)
        ]

        with open(iq_info_path, 'w', encoding='utf-8') as f:
            for item in filtered_data:
                f.write(f"AIQB Name: {item['aiqb_name']}\n")
                f.write(f"Project: {item['project']}\n")
                f.write(f"Comment: {item['comment']}\n\n")
        '''
        print(f"Filtered AIQB data for modules {module_name}:\n")
        for item in filtered_data:
            print(f"AIQB Name: {item['aiqb_name']}")
            print(f"Project: {item['project']}")
            print(f"Comment: {item['comment']}\n")
        '''
    return filtered_data
