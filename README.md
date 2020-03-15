# Patterns

## Using this as a module

This module helps to find regular expressions and fixed data in
binary files.

Assuming you want to find some patterns in a file, give the full
path to the file and the strings/bytes in hexadecimal strings in
a list or as the keys of a dictionary.

You must give all the data as dictionary with two keys, one is
"fixed" and the other is "regex", on fixed you should have only
hexadecimal binaries and on regex you should have the regex
expressions

### Example input for the function
file_path: '/home/username/file_to_check'  
patterns: {  
    'fixed': ['5D00008000', '27051956'],  
    'regex': [b'\x18\(o\x01']  
}  
or for patterns with dictionary  
patterns: {  
'fixed': {  
'5D00008000': 'lzma',  
'27051956': 'uImage',  
},  
'regex': {b'\x18\(o\x01'}  
}

So calling the function is (assuming the above variable names):  
from patterns import find_patterns
find_patterns(file_path, patterns)