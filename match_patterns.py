from collections import defaultdict
import re
from time import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint


def find_pattern_regex(patterns, bin_file):
    res = defaultdict(list)
    for pattern in patterns:
        for regex in re.finditer(pattern, bin_file):
            res[pattern].append({'range': (hex(regex.start()), hex(regex.end())), 'regex': pattern, 'res': regex.group()})
    return res


def find_pattern_fixed(patterns, file):
    res = defaultdict(list)

    for pattern in patterns:
        bin_pattern = bytes.fromhex(pattern)
        idx = 0
        while idx > -1:
            idx = file.find(bin_pattern, idx)
            if idx == -1:
                break
            res[pattern].append(hex(idx))
            idx += 1
        return res


def find_patterns(file_path, patterns, *args, **kwargs):
    with open(file_path, 'rb') as f:
        file = f.read()

    res = []

    with ThreadPoolExecutor(2) as executor:
        future_result = [
            executor.submit(find_pattern_regex, patterns['regex'], file),
            executor.submit(find_pattern_fixed, patterns['fixed'], file),
        ]
        for future in futures.as_completed(future_result):
            result = future.result()
            res.append(result)

    return res


def main():
    path = '/home/moshen/debian-10.3.0-amd64-DVD-2.iso'
    data = {
        'regex': [
            b'00\w{8}',
            b'\x18\(o\x01',
        ],
        'fixed': {
            '5D00008000': 'lzma',
            '27051956': 'uImage',
            '18286F01': 'zImage',
            '1F8B0800': 'gzip',
            '303730373031': 'cpio',
            '303730373032': 'cpio',
            '303730373033': 'cpio',
            '894C5A4F000D0A1A0A': 'lzo',
            '5D00000004': 'lzma',
            'FD377A585A00': 'xz',
            '314159265359': 'bzip2',
            '425A6839314159265359': 'bzip2',
            '04224D18': 'lz4',
            '02214C18': 'lz4',
            '1F9E08': 'gzip',
            '71736873': 'squashfs',
            '68737173': 'squashfs',
            '51434454': 'dtb',
            'D00DFEED': 'fit',
            '7F454C46': 'elf'
        }
    }
    start = time()
    res = find_patterns(path, data)
    end = time()
    ellapsed = end - start
    pprint(res)
    print(ellapsed)


if __name__ == '__main__':
    main()
