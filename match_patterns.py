from time import time
from pprint import pprint
from patterns import find_patterns


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
