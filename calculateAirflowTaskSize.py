import glob
import re

def import_file():
    log = glob.glob("resources/*")[0]
    with open(log, "r") as f:
        return f.read().splitlines()


def parse_lines(lines):
    filtered_lines = [k for k in lines if 'model' in k and 'processed' in k]
    return [re.search(r'\((.*?)\)', line).group(1) if re.search(r'\((.*?)\)', line) else '' for line in filtered_lines]


def convert_to_gb(value, unit):
    if unit == 'MiB':
        return value / 1024  # 1 MiB = 1 / 1024 GB
    elif unit == 'GiB':
        return value * 1.024  # 1 GiB = 1.024 GB
    elif unit == 'kB':
        return value / 1_000_000  # 1 kB = 1 / 1,000,000 GB
    elif unit == 'MB':
        return value / 1000  # 1 MB = 1 / 1000 GB
    elif unit == 'GB':
        return value  # 1 GB = 1 GB
    else:
        return 0


def calculate_total_size(extracted_lines):
    total_gb = 0

    for line in extracted_lines:
        match = re.search(r'(\d+(\.\d+)?)\s*(\w+)\s*processed', line)
        if match:
            value = float(match.group(1))
            unit = match.group(3)
            total_gb += convert_to_gb(value, unit)
    return total_gb


def main():
    lines = import_file()
    extracted_lines = parse_lines(lines)
    total_size = calculate_total_size(extracted_lines)
    print(str(round(total_size,2)) + "GB")

    with open('output.txt', 'w') as f:
        for line in extracted_lines:
            f.write(line + '\n')


main()