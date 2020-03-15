import re
from collections import defaultdict
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor


def _find_pattern_regex(patterns, bin_file):
    res = defaultdict(list)
    for pattern in patterns:
        for regex in re.finditer(pattern, bin_file):
            res[pattern].append({
                'range': (hex(regex.start()), hex(regex.end())),
                'regex': pattern,
                'res': regex.group()
            })
    return res


def _find_pattern_fixed(patterns, file):
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
    if 'regex' not in patterns:
        raise ValueError('regex must be a key of a list of patterns (possibly empty list)')

    if 'fixed' not in patterns:
        raise ValueError('fixed must be a key of a list of fixed strings (possibly empty list)')

    with open(file_path, 'rb') as f:
        file = f.read()

    res = []

    with ThreadPoolExecutor(2) as executor:
        future_result = [
            executor.submit(_find_pattern_regex, patterns['regex'], file),
            executor.submit(_find_pattern_fixed, patterns['fixed'], file),
        ]
        for future in futures.as_completed(future_result):
            result = future.result()
            res.append(result)

    return res
