#!/usr/bin/env python

import string
import random
import re


def get_random_hex_string():
    return ''.join(random.choice(string.hexdigits) for i in range(12))


placeholder = "%AUTO_GENERATED_PASSWORD%"
input_file = open(".env.defaults")
output_file = open(".env", 'w')

for envLine in input_file.readlines():
    for match_position in [match.start() for match in re.finditer(re.escape(placeholder), envLine)]:
        envLine = envLine.replace(placeholder, get_random_hex_string(), 1)
    output_file.write(envLine)

output_file.close()
input_file.close()
